# documents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from .models import Document
from .forms import DocumentUploadForm
import os

# R-2.1: Upload documents
@login_required(login_url='accounts:login')
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploader = request.user
            document.save()
            messages.success(request, f'Document "{document.title}" uploaded successfully!')
            return redirect('documents:my_documents')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/upload.html', {
        'form': form,
        'supported_formats': ['PDF', 'DOCX', 'XLSX', 'TXT', 'JPG', 'PNG']
    })

# R-2.3: View user's documents
@login_required(login_url='accounts:login')
def my_documents(request):
    documents = Document.objects.filter(uploader=request.user)
    return render(request, 'documents/my_documents.html', {
        'documents': documents
    })

# R-3.2: View document preview
@login_required(login_url='accounts:login')
def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    
    # Check if user has permission to view (R-5)
    if document.uploader != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this document.")
        return redirect('documents:my_documents')
    
    return render(request, 'documents/document_detail.html', {
        'document': document
    })

# R-3.2.1: Download document
@login_required(login_url='accounts:login')
def download_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    
    # Check permissions
    if document.uploader != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to download this document.")
        return redirect('documents:my_documents')
    
    response = HttpResponse(document.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.filename()}"'
    return response

# R-2.3: Delete document
@login_required(login_url='accounts:login')
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    
    # Only uploader or admin can delete
    if document.uploader != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this document.")
        return redirect('documents:my_documents')
    
    if request.method == 'POST':
        title = document.title
        document.file.delete()  # Delete the actual file
        document.delete()       # Delete the database record
        messages.success(request, f'Document "{title}" deleted successfully.')
        return redirect('documents:my_documents')
    
    return render(request, 'documents/confirm_delete.html', {
        'document': document
    })
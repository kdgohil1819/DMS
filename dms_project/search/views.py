# search/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from documents.models import Document
import datetime
from django.core.paginator import Paginator

@login_required(login_url='accounts:login')
def search_documents(request):
    """R-3.1: Search documents by title, author, date, or category"""
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    file_type = request.GET.get('file_type', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '-uploaded_at')  # Default: newest first
    
    # Base queryset - only show user's own documents
    documents = Document.objects.filter(uploader=request.user)
    
    # Apply search filters
    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if date_from:
        try:
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
            documents = documents.filter(uploaded_at__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
            documents = documents.filter(uploaded_at__date__lte=date_to)
        except ValueError:
            pass
    
    if file_type:
        documents = documents.filter(file_type=file_type)
    
    if category:
        documents = documents.filter(category__icontains=category)
    
    # Apply sorting (R-3.4)
    if sort_by in ['title', '-title', 'uploaded_at', '-uploaded_at', 'file_size', '-file_size']:
        documents = documents.order_by(sort_by)
    
    # Get unique file types and categories for filter dropdowns
    file_types = Document.objects.filter(uploader=request.user).values_list('file_type', flat=True).distinct()
    categories = Document.objects.filter(uploader=request.user).values_list('category', flat=True).distinct()
    
    # Paginate results
    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documents': documents,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'selected_file_type': file_type,
        'selected_category': category,
        'sort_by': sort_by,
        'file_types': file_types,
        'categories': [c for c in categories if c],  # Remove empty categories
        'total_results': documents.count(),
    }
    return render(request, 'search/search.html', context)

@login_required(login_url='accounts:login')
def recent_documents(request):
    """Show recent documents for dashboard"""
    recent = Document.objects.filter(uploader=request.user).order_by('-uploaded_at')[:5]
    return render(request, 'search/recent.html', {'recent_documents': recent})
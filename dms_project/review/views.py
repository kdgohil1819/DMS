# review/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from documents.models import Document
from .models import Review, ReviewAssignment
from .forms import ReviewForm, AssignmentForm, ResubmissionForm

# Helper function to check if user is staff/admin
def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

# R-4.1: Review Dashboard for staff
@login_required(login_url='accounts:login')
@user_passes_test(is_staff_or_admin)
def review_dashboard(request):
    """Dashboard for reviewers to see pending documents"""
    
    # Documents pending review (not reviewed yet)
    pending_docs = Document.objects.filter(
        status__in=['pending', 'under_review']
    ).exclude(
        reviews__isnull=False
    ).order_by('-uploaded_at')
    
    # Documents assigned to current reviewer
    my_assignments = ReviewAssignment.objects.filter(
        assigned_to=request.user,
        is_active=True,
        document__status__in=['pending', 'under_review']
    ).select_related('document')
    
    # Recently reviewed
    recent_reviews = Review.objects.filter(
        reviewer=request.user
    ).select_related('document')[:10]
    
    # Statistics
    stats = {
        'pending': Document.objects.filter(status='pending').count(),
        'under_review': Document.objects.filter(status='under_review').count(),
        'approved_today': Review.objects.filter(
            status='approved',
            created_at__date=timezone.now().date()
        ).count(),
        'my_pending': my_assignments.count(),
    }
    
    context = {
        'pending_documents': pending_docs[:20],
        'my_assignments': my_assignments,
        'recent_reviews': recent_reviews,
        'stats': stats,
    }
    return render(request, 'review/dashboard.html', context)

# R-4.1: Review a specific document
@login_required(login_url='accounts:login')
@user_passes_test(is_staff_or_admin)
def review_document(request, doc_id):
    """Submit review for a document"""
    document = get_object_or_404(Document, id=doc_id)
    
    # Check if already reviewed
    existing_review = Review.objects.filter(document=document).first()
    if existing_review and existing_review.status in ['approved', 'rejected']:
        messages.warning(request, "This document has already been reviewed.")
        return redirect('review:dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.document = document
            review.reviewer = request.user
            
            # Update document status (R-4.1)
            document.status = review.status
            document.save()
            
            review.save()
            
            # Deactivate assignment if exists
            ReviewAssignment.objects.filter(
                document=document, 
                is_active=True
            ).update(is_active=False)
            
            messages.success(
                request, 
                f'Document "{document.title}" has been {review.status}.'
            )
            return redirect('review:dashboard')
    else:
        form = ReviewForm()
    
    # Get review history (R-4.3)
    review_history = document.reviews.all()
    
    context = {
        'document': document,
        'form': form,
        'review_history': review_history,
    }
    return render(request, 'review/review_document.html', context)

# R-4.2: Resubmit rejected document
@login_required(login_url='accounts:login')
def resubmit_document(request, doc_id):
    """Allow user to resubmit a rejected document"""
    document = get_object_or_404(Document, id=doc_id, uploader=request.user)
    
    # Check if document is rejected
    if document.status != 'rejected':
        messages.error(request, "Only rejected documents can be resubmitted.")
        return redirect('documents:detail', doc_id=document.id)
    
    if request.method == 'POST':
        form = ResubmissionForm(request.POST, instance=document)
        if form.is_valid():
            # Update document
            document = form.save(commit=False)
            document.status = 'pending'  # Reset to pending (R-4.2)
            document.save()
            
            # Create review record for resubmission
            Review.objects.create(
                document=document,
                reviewer=request.user,
                status='resubmitted',
                comments=f"Resubmitted with note: {form.cleaned_data['resubmission_note']}"
            )
            
            messages.success(request, "Document resubmitted successfully!")
            return redirect('documents:detail', doc_id=document.id)
    else:
        form = ResubmissionForm(instance=document)
        # Get last rejection comment
        last_rejection = document.reviews.filter(status='rejected').first()
    
    context = {
        'document': document,
        'form': form,
        'last_rejection': last_rejection,
    }
    return render(request, 'review/resubmit.html', context)

# R-4.3: View review history for a document
@login_required(login_url='accounts:login')
def review_history(request, doc_id):
    """View complete review history"""
    document = get_object_or_404(Document, id=doc_id)
    
    # Check permissions
    if document.uploader != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this history.")
        return redirect('documents:my_documents')
    
    reviews = document.reviews.all()
    
    context = {
        'document': document,
        'reviews': reviews,
    }
    return render(request, 'review/history.html', context)

# Assign document to reviewer (admin only)
@login_required(login_url='accounts:login')
@user_passes_test(lambda u: u.is_superuser)
def assign_reviewer(request, doc_id):
    """Assign a document to a specific reviewer"""
    document = get_object_or_404(Document, id=doc_id)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.document = document
            assignment.assigned_by = request.user
            assignment.save()
            
            # Update document status
            document.status = 'under_review'
            document.save()
            
            messages.success(
                request, 
                f"Document assigned to {assignment.assigned_to.username}"
            )
            return redirect('review:dashboard')
    else:
        form = AssignmentForm()
    
    context = {
        'document': document,
        'form': form,
    }
    return render(request, 'review/assign.html', context)
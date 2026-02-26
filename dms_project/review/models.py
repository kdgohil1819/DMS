# review/models.py
from django.db import models
from django.contrib.auth.models import User
from documents.models import Document
from django.utils import timezone

class Review(models.Model):
    """R-4.3: Review history"""
    REVIEW_STATUS = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('resubmitted', 'Resubmitted'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews_done')
    status = models.CharField(max_length=20, choices=REVIEW_STATUS)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document.title} - {self.status} - {self.created_at.date()}"

class ReviewAssignment(models.Model):
    """Assign documents to specific reviewers"""
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='assignment')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reviews')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_by')
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.document.title} → {self.assigned_to.username}"
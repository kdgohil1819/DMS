# documents/models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    # This is like a dropdown menu for status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # These are like columns in an Excel sheet
    title = models.CharField(max_length=200)           # Document title
    file = models.FileField(upload_to='documents/')    # The actual file
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)  # Who uploaded
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Search fields
    author = models.CharField(max_length=100, blank=True)     # Document author
    category = models.CharField(max_length=100, blank=True)   # Document category
    description = models.TextField(blank=True)                # Document description
    
    # Auto-filled dates
    uploaded_at = models.DateTimeField(auto_now_add=True)     # Upload date
    updated_at = models.DateTimeField(auto_now=True)          # Last update
    
    def __str__(self):
        return self.title
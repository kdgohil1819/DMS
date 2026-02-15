# documents/models.py
from django.db import models
from django.contrib.auth.models import User
import os

def document_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/documents/user_<id>/<filename>
    return f'documents/user_{instance.uploader.id}/{filename}'

class Document(models.Model):
    # R-2.1 Supported formats
    SUPPORTED_FORMATS = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('xlsx', 'XLSX'),
        ('txt', 'TXT'),
        ('jpg', 'JPG'),
        ('png', 'PNG'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic document info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=document_upload_path)
    file_type = models.CharField(max_length=10, choices=SUPPORTED_FORMATS)
    file_size = models.IntegerField(help_text="File size in bytes", editable=False)
    
    # Metadata for search (R-3.1)
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Relationships
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    
    # Status for workflow (R-4.1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-set file size and type
        if self.file and not self.file_size:
            self.file_size = self.file.size
        if self.file and not self.file_type:
            ext = os.path.splitext(self.file.name)[1][1:].lower()
            self.file_type = ext if ext in dict(self.SUPPORTED_FORMATS) else 'other'
        super().save(*args, **kwargs)
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-uploaded_at']
# review/models.py
from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class Review(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # approved or rejected
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reviewed_at']  # Show newest first
    
    def __str__(self):
        return f"{self.document.title} - {self.status}"
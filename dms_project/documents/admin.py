# documents/admin.py
from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploader', 'status', 'uploaded_at']
    list_filter = ['status', 'category']
    search_fields = ['title', 'author', 'description']
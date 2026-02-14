# review/admin.py
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['document', 'reviewer', 'status', 'reviewed_at']
    list_filter = ['status']
    search_fields = ['document__title', 'comments']
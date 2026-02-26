# review/admin.py
from django.contrib import admin
from .models import Review, ReviewAssignment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'reviewer', 'status', 'created_at']  # Changed reviewed_at → created_at
    list_filter = ['status', 'created_at']
    search_fields = ['document__title', 'reviewer__username', 'comments']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('document', 'reviewer')

@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'assigned_to', 'assigned_by', 'assigned_at', 'due_date', 'is_active']
    list_filter = ['is_active', 'assigned_at']
    search_fields = ['document__title', 'assigned_to__username']
    readonly_fields = ['assigned_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('document', 'assigned_to', 'assigned_by')
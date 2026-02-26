# review/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Review, ReviewAssignment
from documents.models import Document

class ReviewForm(forms.ModelForm):
    """Form for reviewers to submit their decision"""
    class Meta:
        model = Review
        fields = ['status', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter review comments...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=[
            ('approved', '✅ Approve'),
            ('rejected', '❌ Reject'),
        ])

class AssignmentForm(forms.ModelForm):
    """Form for assigning documents to reviewers"""
    class Meta:
        model = ReviewAssignment
        fields = ['assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)
        self.fields['assigned_to'].label = "Assign to Reviewer"
        self.fields['due_date'].required = False

class ResubmissionForm(forms.ModelForm):
    """R-4.2: Form for resubmitting rejected documents"""
    class Meta:
        model = Document
        fields = ['description', 'tags']  # Allow updating metadata
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    resubmission_note = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Explain what you changed...'}),
        required=True,
        label="Resubmission Note"
    )
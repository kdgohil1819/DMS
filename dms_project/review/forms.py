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
    """Form for resubmitting rejected documents with NEW file option"""
    
    # Add a file field for new upload
    new_file = forms.FileField(
        required=False,
        label="Upload Corrected File (Optional)",
        help_text="Upload a new version of your document if needed"
    )
    
    resubmission_note = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'placeholder': 'Explain what changes you made...'
        }),
        required=True,
        label="Resubmission Note"
    )
    
    class Meta:
        model = Document
        fields = ['title', 'description', 'author', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., report, confidential, draft'
            }),
        }
    
    def clean_new_file(self):
        """Validate the new file if uploaded"""
        new_file = self.cleaned_data.get('new_file')
        if new_file:
            # Check file size (max 10MB)
            if new_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB")
            
            # Check file extension
            ext = new_file.name.split('.')[-1].lower()
            valid_extensions = ['pdf', 'docx', 'xlsx', 'txt', 'jpg', 'png']
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file format. Please upload: {', '.join(valid_extensions)}"
                )
        return new_file
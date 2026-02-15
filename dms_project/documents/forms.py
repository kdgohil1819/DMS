# documents/forms.py
from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'author', 'category', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g., report, confidential, draft'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB")
            
            # Check file extension
            ext = file.name.split('.')[-1].lower()
            valid_extensions = ['pdf', 'docx', 'xlsx', 'txt', 'jpg', 'png']
            if ext not in valid_extensions:
                raise forms.ValidationError(f"Unsupported file format. Please upload: {', '.join(valid_extensions)}")
        return file
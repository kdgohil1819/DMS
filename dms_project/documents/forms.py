# documents/forms.py
from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    # Add a multiple choice field for tags
    selected_tags = forms.MultipleChoiceField(
        choices=Document.TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'}),
        required=False,
        label="Tags"
    )
    
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'author', 'category', 'selected_tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document author'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document title'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing document, pre-select tags
        if self.instance and self.instance.pk and self.instance.tags:
            existing_tags = [tag.strip() for tag in self.instance.tags.split(',') if tag.strip()]
            self.initial['selected_tags'] = existing_tags
    
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
    
    def save(self, commit=True):
        # Convert selected tags to comma-separated string
        instance = super().save(commit=False)
        selected_tags = self.cleaned_data.get('selected_tags', [])
        instance.tags = ','.join(selected_tags)
        
        if commit:
            instance.save()
        return instance
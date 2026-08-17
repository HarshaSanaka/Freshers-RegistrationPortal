from django import forms
from django.core.exceptions import ValidationError
from .models import StudentDocument

def validate_file_size(file):
    max_mb = 2
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {max_mb} MB.")
    
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError("Only PDF, JPG, JPEG, and PNG files are supported.")

class DocumentUploadForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file_size], widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = StudentDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
        }
from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StudentProfile
        fields = [
            'admission_number', 'phone_number', 'gender', 'date_of_birth',
            'address', 'department', 'tenth_percentage', 'twelfth_percentage',
            'marksheet_10th', 'marksheet_12th', 'id_proof'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
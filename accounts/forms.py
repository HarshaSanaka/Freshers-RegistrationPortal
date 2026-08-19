from django import forms
from django.contrib.auth.models import User
from students.models import StudentProfile, AcademicInformation

class AdmissionNumberForm(forms.Form):
    admission_number = forms.CharField(
        max_length=20,
        label='Admission Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'autocomplete': 'username',
            'placeholder': 'Enter your admission number',
        }),
    )

    def clean_admission_number(self):
        return self.cleaned_data['admission_number'].strip()


class StudentLoginForm(AdmissionNumberForm):
    date_of_birth = forms.DateField(
        label='Password (Date of Birth)',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg',
            'autocomplete': 'current-password',
        }),
    )


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    admission_number = forms.CharField(max_length=20, required=True, label="Admission Number")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    department = forms.ChoiceField(choices=AcademicInformation.BRANCH_CHOICES, required=True, label="Enrolled Department")
    tenth_percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=True, label="10th Percentage (%)")
    twelfth_percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=True, label="12th Percentage (%)")

    marksheet_10th = forms.FileField(required=True, label="10th Marksheet")
    marksheet_12th = forms.FileField(required=True, label="12th Marksheet")
    id_proof = forms.FileField(required=True, label="Government ID Proof")

    class Meta:
        model = StudentProfile
        fields = ['gender', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
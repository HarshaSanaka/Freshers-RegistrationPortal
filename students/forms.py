from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, AcademicInformation

class PersonalInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = StudentProfile
        fields = ['date_of_birth', 'gender', 'phone', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
            self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        profile = super().save(commit=commit)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class AcademicInfoForm(forms.ModelForm):
    class Meta:
        model = AcademicInformation
        fields = [
            'tenth_school', 'tenth_percentage', 'tenth_passing_year',
            'intermediate_college', 'intermediate_percentage', 'intermediate_passing_year',
            'course', 'branch', 'admission_year'
        ]
        widgets = {
            'tenth_school': forms.TextInput(attrs={'class': 'form-control'}),
            'tenth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tenth_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'intermediate_college': forms.TextInput(attrs={'class': 'form-control'}),
            'intermediate_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'intermediate_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'admission_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Doctor

class DoctorApplicationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'specification', 'experience', 'certificate_file']

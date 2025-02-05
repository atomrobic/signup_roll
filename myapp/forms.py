from django import forms
from .models import DoctorCertificate



class DoctorCertificateForm(forms.ModelForm):
    class Meta:
        model = DoctorCertificate
        fields = ['doctor_name', 'certificate_file']

from django import forms
from .models import Members

class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['studentNumber', 'firstName', 'middleName', 'lastName', 'program_and_year', 'college', 'scholarshipType', 'cpNum', 'personalEmail', 'cspcEmail', 'address', 'position']
        labels = {
            'studentNumber': 'Student No.',
            'firstName': 'First Name',
            'middleName': 'Middle Name',
            'lastName': 'Last Name',
            'program_and_year': 'Degree, Program & Year Level',
            'college': 'College/Unit',
            'scholarshipType': 'Scholarship Type',
            'cpNum': 'Contact No.',
            'personalEmail': 'Personal Email',
            'cspcEmail': 'CSPC Email',
            'address': 'Home Address',
            'position': 'Position',
        }
        widgets = {
            'studentNumber': forms.NumberInput(attrs={'class': 'form-control'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'middleName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'program_and_year': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={'class': 'form-control'}),
            'scholarshipType': forms.Select(attrs={'class': 'form-control'}),
            'cpNum': forms.TextInput(attrs={'class': 'form-control'}),
            'personalEmail': forms.EmailInput(attrs={'class': 'form-control'}),
            'cspcEmail': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }
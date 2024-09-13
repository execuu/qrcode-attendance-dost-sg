from django import forms
from .models import Event

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        labels = {
            'eventName': 'Events/Activities/Initiatives',
            'created_at': 'Time and Date',
        }

        widgets = {
            'eventName': forms.TextInput(attrs={'class': 'form-control'}),
            'created_at': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model= Trip
        exclude= []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            #'guests': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'generated': forms.Select(attrs={'class': 'form-select'}),
            'agent': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'trip_status': forms.Select(attrs={'class': 'form-select'}),
            'no_consultant': forms.Select(attrs={'class': 'form-select'}),
            'sa_consultant': forms.Select(attrs={'class': 'form-select'}),
        }



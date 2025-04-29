from django import forms
from .models import Trip, Guest

class TripForm(forms.ModelForm):
    class Meta:
        model= Trip
        exclude= ["guests"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={ 
                    'class': 'form-control',
                    'rows': 2,  # You can try 2, 3, or 4 — adjust as needed
                    'style': 'resize: vertical;'  # Optional: lets user resize only vertically
}),
            'generated': forms.Select(attrs={'class': 'form-select'}),
            'agent': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'trip_status': forms.Select(attrs={'class': 'form-select'}),
            'no_consultant': forms.Select(attrs={'class': 'form-select'}),
            'sa_consultant': forms.Select(attrs={'class': 'form-select'}),
        }


class GuestSelectionForm(forms.Form):
    existing_guest = forms.ModelChoiceField(
        queryset=Guest.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Existing Guest"
    )

    first_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

from django.forms import formset_factory

GuestFormSet = formset_factory(GuestSelectionForm, extra=0)  # We'll set extra dynamically



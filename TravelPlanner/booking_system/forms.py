from django import forms
from .models import Trip, Guest, Flight, Accommodation, Supplier

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
                    'rows': 2,  
                    'style': 'resize: vertical;'  
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


class CreateGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'mobile']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'email',
            'mobile',
            'emergency_contact'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.Select(attrs={'class': 'form-select'}),
        }


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        exclude = ['trip']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'arrival_airport': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'departure_airport': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'booked_by': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        currency = cleaned_data.get("currency")

        if price and not currency:
            self.add_error('currency', "Please select a currency")

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        exclude = ['trip']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'units': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'basis': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'reservation_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'tax_invoice': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'paid_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 1}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        currency = cleaned_data.get("currency")

        if price and not currency:
            self.add_error('currency', "Please select a currency")

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']



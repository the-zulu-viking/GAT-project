from django.db import models
from django.contrib.auth.models import User 
from phonenumber_field.modelfields import PhoneNumberField
import datetime as date
from django.core.exceptions import ValidationError
# Create your models here.

class Consultant(models.Model):
    types = {
        "NOR": "Norwegian",
        "ZAR": "South African",
        "Other": "Other",
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shirt_size = models.CharField(max_length=1, choices=types)
    

class Agent(models.Model):
    company = models.CharField(max_length=255)  
    email = models.EmailField()
    phone_number = PhoneNumberField(region="NO")
    website = models.URLField(blank=True) 
    note = models.TextField(blank=True)

    def __str__(self):
        return self.company


class Generated(models.Model):
    title = title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class TripStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    class Meta: 
        verbose_name_plural = "TripStatuses"

    def __str__(self):
        return self.title


class PaymentStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    class Meta: 
        verbose_name_plural = "PaymentStatuses"

    def __str__(self):
        return self.title
    
class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField(region='NO')
    emergency_contact = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="emergency_contact"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        """Returns the age of the guest."""
        if self.date_of_birth:
            today = date.date.today()
            dob = self.date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None

    def clean(self):
        """Ensure a guest cannot be their own emergency contact."""
        if self.emergency_contact and self.emergency_contact == self:
            raise ValidationError("A guest cannot be their own emergency contact.")


class Trip(models.Model):
    name = models.CharField(max_length=64)
    number_of_guests = models.IntegerField()
    guests = models.ManyToManyField(Guest, related_name="guests")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_status = models.ForeignKey(PaymentStatus)
    trip_status = models.ForeignKey(TripStatus)
    no_consultant = models.ForeignKey(Consultant)
    sa_consultant = models.ForeignKey(Consultant)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["start_date"]

    def duration(self):
        """Returns the number of nights for the trip."""
        if self.start_date and self.end_date:
            return (self.end_date.date() - self.start_date.date()).days
        return None
    
    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=3)

    class Meta: 
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.code

class Basis(models.Model):
    code = models.CharField(max_length=3)
    description  = models.TextField()

    def __str__(self):
        return self.code

    
class Stay(models.Model):  
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    units = models.IntegerField()
    basis = models.ForeignKey(Basis, on_delete=models.PROTECT) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    note = models.TextField(blank=True)


class Supplier(models.Model):
    name = models.CharField(max_length=64)


class Flight():
    trip = models.ForeignKey()
    number = models.CharField(max_length=16)
    depature_date = models.DateField()
    depature_time = models.TimeField()
    depature_airport = models

    def __str__(self):
        return self.number




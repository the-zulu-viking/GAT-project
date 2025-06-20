from django.db import models
from django.contrib.auth.models import User 
from phonenumber_field.modelfields import PhoneNumberField
import datetime as date
from django.core.exceptions import ValidationError
# Create your models here.

class Consultant(models.Model):
    types = [
    ("NOR", "Norwegian"),
    ("ZAR", "South African"),
    ("OTHER", "Other"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=types)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    
class Agent(models.Model):
    company = models.CharField(max_length=255)  
    email = models.EmailField()
    phone_number = PhoneNumberField(region="NO", blank=True, null= True)
    website = models.URLField(blank=True, null=True) 
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company

class Generated(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class TripStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank= True, null=True)

    class Meta: 
        verbose_name_plural = "TripStatuses"

    def __str__(self):
        return self.title

class PaymentStatus(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank= True, null=True)

    class Meta: 
        verbose_name_plural = "PaymentStatuses"

    def __str__(self):
        return self.title
    
class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    mobile = PhoneNumberField(region='NO')
    emergency_contact = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="emergency_for"
    )

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else: 
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
    guests = models.ManyToManyField(Guest, related_name="trips", blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    generated = models.ForeignKey(Generated, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)

    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, blank=True, null=True)
    trip_status = models.ForeignKey(TripStatus, on_delete=models.PROTECT, blank=True, null=True)

    no_consultant = models.ForeignKey(
        Consultant, on_delete=models.PROTECT, null=True, blank=True, related_name="no_consultant_trips", verbose_name='Norwegian consultant')
    sa_consultant = models.ForeignKey(
        Consultant, on_delete=models.PROTECT, null=True, blank=True, related_name="sa_consultant_trips", verbose_name='South African consultant')

    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["start_date"]

    def duration(self):
        '''calculates number of nights of a trip '''
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def clean(self):
        '''Validate that if generated is "Agent", an agent must be selected'''
        if self.generated and self.generated.title.lower() == "agent" and not self.agent:
            raise ValidationError("An agent must be selected if the trip was generated by an agent.")
        if self.generated and self.generated.title.lower() != "agent" and self.agent:
            raise ValidationError("Agent should only be set if the trip was generated by an agent.")
        # make sure start is before end
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError("Trip end date must be after the start date.")

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

class Supplier(models.Model):
    name = models.CharField(max_length=64)

    def accommodation_trips(self):
        """Returns all trips where this supplier is used for accommodation."""
        return Trip.objects.filter(accommodation__supplier=self).distinct()
    
    def acc_bed_nights(self):
        """Returns total bed nights"""
        total_bed_nights = 0
        for accom in Accommodation.objects.filter(supplier=self):
            nights = accom.duration()
            if nights and accom.units:
                total_bed_nights += nights * accom.units
        return total_bed_nights

    def __str__(self):
        return self.name
    
    
class Accommodation(models.Model):  
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    units = models.IntegerField(blank=True, null=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    basis = models.ForeignKey(Basis, on_delete=models.PROTECT, blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    reservation_number = models.CharField(max_length=256,blank=True, null=True )
    paid= models.BooleanField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically update 'paid' based on 'paid_date'
        self.paid = bool(self.paid_date)
        super().save(*args, **kwargs)

    def duration(self):
        '''calculates number of nights of a stay '''
        if self.arrival_date and self.departure_date:
            return (self.departure_date - self.arrival_date).days
        return None

    def __str__(self):
        return f"{self.trip} -- {self.supplier}"
    
    
    def clean(self):
        """Ensure accommodation dates are correct order."""
        if self.arrival_date and self.departure_date:
            if self.arrival_date >= self.departure_date:
                raise ValidationError("Arrival date must be before departure date.")
    
            



class Flight(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    number = models.CharField(max_length=16) 
    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    arrival_airport = models.CharField(max_length=64, blank=True, null=True) 
    departure_date = models.DateField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    departure_airport = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    booked_by = models.CharField(max_length=16) 
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.number
    
    def clean(self):
        """Ensure dates are in correct order."""
        if self.arrival_date and self.departure_date:
            if self.departure_date > self.arrival_date:
                raise ValidationError("Arrival date must be after departure date.")
    
    
class ServiceType(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank = True, null=True)

    class Meta: 
        verbose_name_plural = "ServiceTypes"

    def __str__(self):
            return self.title

class Service(models.Model): 
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    service = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    reservation_number = models.CharField(max_length=256,blank=True, null=True )
    tax_invoice= models.BooleanField(blank=True, null=True)
    paid= models.BooleanField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically update 'paid' based on 'paid_date'
        self.paid = bool(self.paid_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trip} -- {self.supplier}"




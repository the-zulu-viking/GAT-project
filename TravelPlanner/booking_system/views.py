from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import datetime 
from django.urls import include, path
from .models import *
from .forms import TripForm


# Create your views here.

def home(request):
    return render(request,"home.html")

def trips_overview(request):
    trips = Trip.objects.order_by()[:10]

    context = {
        'trips' : trips 
        }
    return render(request,"booking_system/trip/trips_overview.html", context=context)

def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trips_overview')  # Update this to your actual trip list view name
    else:
        form = TripForm()

    return render(request, 'booking_system//trip/trip_form.html', {'form': form})

def trip_view(request,trip_id):
    trip = get_object_or_404(Trip,id=trip_id)
    return render(request, 'booking_system//trip/trip_view.html', {'trip': trip})


def guest_overview(request):
    guests = Guest.objects.order_by()[:10]

    context = {
        'guests':guests
        }
    return render(request,"booking_system/guest/guest_overview.html", context=context)


def guest_view(request,guest_id):
    guest = get_object_or_404(Guest,id=guest_id)
    return render(request, 'booking_system/guest/guest_view.html', {'guest': guest})
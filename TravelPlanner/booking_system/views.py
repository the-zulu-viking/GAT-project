from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import datetime 
from django.forms import formset_factory
from django.urls import include, path
from .models import *
from .forms import *


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
            trip = form.save()
            return redirect('trip_add_guests', trip_id=trip.id)  # Redirect to Step 2
    else:
        form = TripForm()

    return render(request, 'booking_system/trip/trip_form.html', {'form': form})


def trip_guest_search(request, trip_id, slot_index):
    trip = get_object_or_404(Trip, id=trip_id)
    query = request.GET.get("q", "")
    guests = Guest.objects.filter(
        models.Q(first_name__icontains=query) |
        models.Q(last_name__icontains=query) |
        models.Q(email__icontains=query)
    ) if query else []

    return render(request, "booking_system/trip/trip_guest_search.html", {
        "trip": trip,
        "slot_index": slot_index,
        "guests": guests,
        "query": query
    })


def trip_add_guests(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    GuestFormSet = formset_factory(GuestSelectionForm, extra=trip.number_of_guests)

    if request.method == "POST":
        formset = GuestFormSet(request.POST)
        if formset.is_valid():
            trip.guests.clear()  # Clear existing guests

            for form in formset:
                existing_guest = form.cleaned_data.get('existing_guest')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                date_of_birth = form.cleaned_data.get('date_of_birth')
                email = form.cleaned_data.get('email')
                mobile = form.cleaned_data.get('mobile')

                if existing_guest:
                    trip.guests.add(existing_guest)
                elif first_name and last_name and email and mobile:
                    # Create a new guest
                    guest = Guest.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        email=email,
                        mobile=mobile
                    )
                    trip.guests.add(guest)
                else:
                    # No guest selected or created, ignore this slot
                    pass

            return redirect('trip_add_accommodations', trip_id=trip.id)
    else:
        formset = GuestFormSet()

    return render(request, "booking_system/trip/trip_guests.html", {"trip": trip, "formset": formset})



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
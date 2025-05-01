from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import datetime 
from django.urls import include, path
from .utils import search_guests
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

# Step 1: Creating a trip

def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            return redirect('trip_guest_search', trip_id=trip.id, slot_index=0) # Redirect to Step 2
    else:
        form = TripForm()

    return render(request, 'booking_system/trip/trip_form.html', {'form': form})

def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_guest_search', trip_id=trip.id, slot_index=0)
    else:
        form = TripForm(instance=trip)

    return render(request, 'booking_system/trip/trip_form.html', {
        'form': form,
        'editing': True,
        'trip': trip
    })

# Step 2: Adding Guests 

def trip_guest_search(request, trip_id, slot_index):
    trip = get_object_or_404(Trip, id=trip_id)
    query = request.GET.get("q", "")
    guests = search_guests(query) if query else []

    return render(request, "booking_system/trip/trip_guest_search.html", {
        "trip": trip,
        "slot_index": slot_index,
        "guests": guests,
        "query": query
    })


def trip_assign_guest(request, trip_id, slot_index, guest_id):
    trip = get_object_or_404(Trip, id=trip_id)
    guest = get_object_or_404(Guest, id=guest_id)

    # Save to session
    guest_slots = request.session.get('guest_slots', {})
    guest_slots[str(slot_index)] = guest_id
    request.session['guest_slots'] = guest_slots

    #assigns guest to the trip
    if guest not in trip.guests.all():
        trip.guests.add(guest)

    # Redirect to next step
    next_slot = slot_index + 1
    if next_slot < trip.number_of_guests:
        return redirect('trip_guest_search', trip_id=trip.id, slot_index=next_slot)
    else:
        return redirect('trip_add_flights', trip_id=trip.id)


def trip_create_guest(request, trip_id, slot_index):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == 'POST':
        form = CreateGuestForm(request.POST)
        if form.is_valid():
            guest = form.save()

            # Save to session
            guest_slots = request.session.get('guest_slots', {})
            guest_slots[str(slot_index)] = guest.id
            request.session['guest_slots'] = guest_slots

            # ✅ Immediately attach guest to the trip
            if guest not in trip.guests.all():
                trip.guests.add(guest)

            next_slot = slot_index + 1
            if next_slot < trip.number_of_guests:
                return redirect('trip_guest_search', trip_id=trip.id, slot_index=next_slot)
            else:
                return redirect('trip_add_flights', trip_id=trip.id)

    else:
        form = CreateGuestForm()

    return render(request, 'booking_system/trip/trip_create_guest.html', {
        'form': form,
        'trip': trip,
        'slot_index': slot_index,
    })

def trip_remove_guest(request, trip_id, guest_id):
    trip = get_object_or_404(Trip, id=trip_id)
    guest = get_object_or_404(Guest, id=guest_id)

    # Remove from trip.guest list
    trip.guests.remove(guest)

    # Remove from session guest_slots
    guest_slots = request.session.get("guest_slots", {})
    slot_to_remove = None

    for slot, gid in guest_slots.items():
        if str(gid) == str(guest_id):
            slot_to_remove = slot
            break

    if slot_to_remove is not None:
        del guest_slots[slot_to_remove]
        request.session["guest_slots"] = guest_slots

    # Redirect to next open slot
    filled_slots = set(int(k) for k in guest_slots.keys())
    total_slots = trip.number_of_guests
    open_slots = [i for i in range(total_slots) if i not in filled_slots]

    if open_slots:
        next_slot = min(open_slots)
        return redirect("trip_guest_search", trip_id=trip.id, slot_index=next_slot)
    else:
        # All slots filled — fallback (e.g., trip view or accommodation step)
        return redirect("trip_view", trip_id=trip.id)

# Step 3 Adding flights
from django.forms import modelformset_factory

def trip_add_flights(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    FlightFormSet = modelformset_factory(Flight, form=FlightForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = FlightFormSet(request.POST, queryset=Flight.objects.filter(trip=trip))
        if formset.is_valid():
            flights = formset.save(commit=False)

            # Save new/edited flights
            for flight in flights:
                flight.trip = trip
                flight.save()

            # Delete marked-for-deletion flights
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('trip_add_flights', trip_id=trip.id)
    else:
        formset = FlightFormSet(queryset=Flight.objects.filter(trip=trip))

    return render(request, 'booking_system/trip/add_flights.html', {
        'trip': trip,
        'formset': formset,
    })


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
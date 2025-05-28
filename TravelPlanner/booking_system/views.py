from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import datetime 
from django.urls import include, path
from django.db.models import Q
from .utils import search_guests
from .models import *
from .forms import *


# Create your views here.

def home(request):
    return render(request,"home.html")


def trips_overview(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    trips = Trip.objects.all()
    statuses = TripStatus.objects.all()

    if search_query:
        trips = trips.filter(name__icontains=search_query)

    if status_filter:
        trips = trips.filter(trip_status=status_filter)

    if start_date:
        trips = trips.filter(start_date__gte=start_date)

    if end_date:
        trips = trips.filter(end_date__lte=end_date)


    context = {
        'trips': trips,
        'statuses': statuses,
        'search_query': search_query,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'booking_system/trip/trips_overview.html', context)

# Step 1: Creating a trip or editting 

def trip_form(request, trip_id=None):
    editing = trip_id is not None
    trip = get_object_or_404(Trip, id=trip_id) if editing else None

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save()
            action = request.POST.get('action')
            if action == 'save_next':
                return redirect('trip_guest_search', trip_id=trip.id, slot_index=0)
            else:
                return redirect('edit_trip', trip_id=trip.id)  # stays on same form
    else:
        form = TripForm(instance=trip)

    return render(request, 'booking_system/trip/trip_form.html', {
        'form': form,
        'editing': editing,
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
    if trip.guests.filter(id=guest.id).exists():
        messages.warning(request, f"{guest} is already assigned to this trip.")
        return redirect('trip_guest_search', trip_id=trip.id, slot_index=slot_index)

    else:
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

            # attach guest to the trip
            if not trip.guests.filter(id=guest.id).exists():
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


def trip_add_flights(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    flights = Flight.objects.filter(trip=trip)
    currencies = Currency.objects.all()

    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.trip = trip
            flight.save()
            return redirect('trip_add_flights', trip_id=trip.id)
    else:
        form = FlightForm()

    return render(request, 'booking_system/trip/add_flights.html', {
        'trip': trip,
        'form': form,
        'flights': flights,
        'currencies':currencies
    })

def trip_edit_flight(request, trip_id, flight_id):
    trip = get_object_or_404(Trip, id=trip_id)
    flight = get_object_or_404(Flight, id=flight_id, trip=trip)

    if request.method == "POST":
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
    return redirect('trip_add_flights', trip_id=trip.id)

def trip_delete_flight(request, trip_id, flight_id):
    trip = get_object_or_404(Trip, id=trip_id)
    flight = get_object_or_404(Flight, id=flight_id, trip=trip)

    if request.method == 'POST':
        flight.delete()

    return redirect('trip_add_flights', trip_id=trip.id)

def trip_add_accommodations(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    accommodations = Accommodation.objects.filter(trip=trip)

    if request.method == "POST":
        form = AccommodationForm(request.POST)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.trip = trip
            accommodation.save()
            return redirect("trip_add_accommodations", trip_id=trip.id)
    else:
        form = AccommodationForm()

    return render(request, "booking_system/trip/add_accommodations.html", {
        "trip": trip,
        "form": form,
        "accommodations": accommodations,
    })

def trip_delete_accommodation(request, trip_id, acc_id):
    trip = get_object_or_404(Trip, id=trip_id)
    accommodation = get_object_or_404(Accommodation, id=acc_id, trip=trip)

    if request.method == "POST":
        accommodation.delete()
    return redirect("trip_add_accommodations", trip_id=trip.id)




def create_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next", "trips_overview"))
    else:
        form = SupplierForm()
    
    return render(request, "booking_system/accommodation/supplier_form.html", {
        "form": form
    })

def trip_view(request,trip_id):
    trip = get_object_or_404(Trip,id=trip_id)
    flights = Flight.objects.filter(trip=trip)
    print(flights)
    return render(request, 'booking_system//trip/trip_view.html', {'trip': trip, 'flights':flights})


def guest_overview(request):
    
    search_query = request.GET.get('search', '')
    if search_query:
        guests = Guest.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        guests = Guest.objects.order_by()

    context = {
        'guests':guests
        }
    return render(request,"booking_system/guest/guest_overview.html", context=context)


def guest_view(request,guest_id):
    guest = get_object_or_404(Guest,id=guest_id)
    trips = guest.trips.all()
    print(guest,trips)
    return render(request, 'booking_system/guest/guest_view.html', 
                  {'guest': guest,
                   'trips':trips,})

def guest_edit(request,guest_id):
    guest = get_object_or_404(Guest,id=guest_id)

    if request.method == 'POST':
        form = EditGuestForm(request.POST, instance=guest)
        if form.is_valid():
            guest = form.save()

            return redirect('guest_view', guest_id=guest.id)

    else:
        form = EditGuestForm(instance=guest)

    return render(request, 'booking_system/guest/guest_edit.html', 
                  {'guest': guest,
                   "form": form})
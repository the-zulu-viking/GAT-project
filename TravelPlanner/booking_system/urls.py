"""
URL configuration for TravelPlanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from booking_system import views

urlpatterns = [
    path("", 
         views.home, 
         name='home'),

    # Trip URLs
    path("trips", 
         views.trips_overview, 
         name='trips_overview'),
    path("trips/<int:trip_id>", 
        views.trip_view, 
        name='view_trip'),

    # Step 1: Trip Details

    path("trips/create/", 
        views.trip_form, 
        name='create_trip'),
    path("trips/<int:trip_id>/edit",
        views.trip_form, 
        name="edit_trip"),
  
    # Step 2: Guests

    path("trips/create/<int:trip_id>/guest-slot/<int:slot_index>/search", 
        views.trip_guest_search, 
        name='trip_guest_search'),  # Search guest for a slot
    path("trips/create/<int:trip_id>/guest-slot/<int:slot_index>/assign/<int:guest_id>",
        views.trip_assign_guest,
        name="trip_assign_guest"),
    path("trips/create/<int:trip_id>/guest-slot/<int:slot_index>/create",
        views.trip_create_guest,
        name="trip_create_guest"),
    path("trips/create/<int:trip_id>/guest/<int:guest_id>/remove",
        views.trip_remove_guest,
        name="trip_remove_guest"),

    # Step 3: Flights

    path("trips/create/<int:trip_id>/flights",
        views.trip_add_flights,
        name="trip_add_flights"),


    # Guest URLs
    path("guest/", views.guest_overview, name='guest_overview'),
    path("guest/<int:guest_id>", views.guest_view, name='guest_view'),
    path("guest/<int:guest_id>/edit", views.guest_edit, name='guest_edit'),
]

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
    path("", views.home, name='home'),

    # Trip URLs
    path("trips", views.trips_overview, name='trips_overview'),
    path("trips/<int:trip_id>", views.trip_view, name='view_trip'),  # View trip
    path("trips/create/", views.create_trip, name='create_trip'),  # Step 1
    path("trips/create/<int:trip_id>/guests", views.trip_add_guests, name='trip_add_guests'),  # Step 2
    #path("trips/create/<int:trip_id>/accommodations", views.trip_add_accommodations, name='trip_add_accommodations'),  # Step 3

    # Guest URLs
    path("guest/", views.guest_overview, name='guest_overview'),
    path("guest/<int:guest_id>", views.guest_view, name='guest_view'),
]

from .models import Guest
from django.db.models import Q

def search_guests(query):
    """
    Search for guests by first name, last name, or email (case insensitive).
    Returns a queryset of matching guests.
    """
    if not query:
        return Guest.objects.none()  # Empty queryset if no query

    return Guest.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    ).distinct()


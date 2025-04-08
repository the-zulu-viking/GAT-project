from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Consultant)
admin.site.register(Agent)
admin.site.register(Guest)
admin.site.register(Generated)
admin.site.register(Trip)
admin.site.register(Currency)
admin.site.register(Basis)
admin.site.register(Supplier)
admin.site.register(Accommodation)
admin.site.register(Flight)
admin.site.register(ServiceType)
admin.site.register(Service)

# statuses
admin.site.register(TripStatus)
admin.site.register(PaymentStatus)

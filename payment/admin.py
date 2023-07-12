from django.contrib import admin

from .models import Appointment,Prescription

admin.site.register(Prescription)
admin.site.register(Appointment)

from django.contrib import admin
from . models import Doctors,Appointment,Slots,Department

# Register your models here.

admin.site.register(Doctors)
admin.site.register(Appointment)
admin.site.register(Slots)
admin.site.register(Department)
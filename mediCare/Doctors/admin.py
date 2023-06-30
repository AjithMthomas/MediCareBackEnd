from django.contrib import admin
from . models import Doctors,Slots,Department,Blogs

# Register your models here.

admin.site.register(Doctors)
admin.site.register(Slots)
admin.site.register(Department)
admin.site.register(Blogs)
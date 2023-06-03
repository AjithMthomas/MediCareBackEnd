from rest_framework import serializers
from . models import TimeSlot,Slots,Department,Doctors,Appointment
from accounts . serializers import UserSerializer



class DepartmentSerializers(serializers.ModelSerializer):
     class Meta:
          model = Department
          fields = '__all__'


class DoctorsSerializers(serializers.ModelSerializer):
     user = UserSerializer()
     specialization = DepartmentSerializers()
     class Meta:
          model = Doctors
          fields = '__all__'

class SlotSerializers(serializers.ModelSerializer):
     doctor = DoctorsSerializers()
     class Meta:
          model = Slots
          fields = "__all__"


class TimeslotSerializers(serializers.ModelSerializer):
     slot =  SlotSerializers()
     class Meta:
          model = TimeSlot
          fields ='__all__'




class Appointmentserializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Appointment
          fields = '__all__'






 
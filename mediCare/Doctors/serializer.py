from rest_framework import serializers
from . models import TimeSlot,Slots,Department,Doctors,Appointment
from accounts . serializers import UserSerializer


class TimeslotSerializers(serializers.ModelSerializer):
     class Meta:
          model = TimeSlot
          fields ='__all__'

class SlotSerializers(serializers.ModelSerializer):
     time_slot = TimeslotSerializers()
     class Meta:
          model = Slots
          fields = "__all__"



class DepartmentSerializers(serializers.ModelSerializer):
     class Meta:
          model = Department
          fields = '__all__'

class DoctorsSerializers(serializers.ModelSerializer):
     user = UserSerializer()
     specialization = DepartmentSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Doctors
          fields = '__all__'



class Appointmentserializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Appointment
          fields = '__all__'






 
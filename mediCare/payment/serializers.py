from rest_framework import serializers
from accounts. serializers import UserSerializer
from Doctors.serializer import DoctorsSerializers,SlotSerializers
from . models import Appointment,Prescription



class Appointmentserializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Appointment
          fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    doctor = DoctorsSerializers()
    class Meta:
        model = Prescription
        fields = '__all__'

class  PostPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

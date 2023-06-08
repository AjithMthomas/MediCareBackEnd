from rest_framework import serializers
from . models import Slots,Department,Doctors,Appointment,Blogs
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

class PostDoctorSerializers(serializers.ModelSerializer):
     class Meta:
          model = Doctors
          fields = '__all__'

class SlotSerializers(serializers.ModelSerializer):
     doctor = UserSerializer()
     class Meta:
          model = Slots
          fields = "__all__"


class  PostSlotSerializers(serializers.ModelSerializer):
     class Meta:
          model = Slots
          fields = "__all__"



class Appointmentserializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Appointment
          fields = '__all__'

class Blogsserializer(serializers.ModelSerializer):
     doctors = DoctorsSerializers()
     class Meta:
          model = Blogs
          fields ='__all__'

class PostBlogserializer(serializers.ModelSerializer):
     class Meta:
          model = Blogs
          field = '__all__'


 
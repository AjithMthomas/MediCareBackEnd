from rest_framework import serializers
from . models import Slots,Department,Doctors,Blogs
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




class Blogsserializer(serializers.ModelSerializer):
     doctor = DoctorsSerializers()
     class Meta:
          model = Blogs
          fields ='__all__'


class PostBlogserializer(serializers.ModelSerializer):
     class Meta:
          model = Blogs
          fields = '__all__'


 
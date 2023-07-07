from django.shortcuts import render
from accounts . models import User
from accounts . serializers import UserSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializer import (DepartmentSerializers,PostDoctorSerializers,SlotSerializers,
PostSlotSerializers,DoctorsSerializers,Blogsserializer,PostBlogserializer)
from . models import Department
from rest_framework.decorators import api_view
from rest_framework import status
from . models import Doctors,Slots,Blogs
import datetime
from rest_framework import generics

# Create your views here.


class doctorsListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=True, is_superadmin=False)

class blockDoctors(APIView):
    def get(self,request,id):
        print(id)
        try:
            user = User.objects.get(id=id)
            user.is_active = not user.is_active
            user.save()
            return Response({'msg': "Doctor status updated successfully"})
        except User.DoesNotExist:
            print('no users')
            return Response({'msg': "doctor not found"})
        except Exception as e:
            print(e)
            return Response({'msg': str(e)})



class DepartmentListView(ListAPIView):
    serializer_class = DepartmentSerializers
    def get_queryset(self):
        return Department.objects.all()


@api_view(['POST'])
def createDepartment(request):
    serializer = DepartmentSerializers(data=request.data)
    print(serializer.is_valid())
    print(serializer.errors)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class DepartmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers


class DoctorsCreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = PostDoctorSerializers(data=request.data)
        print(serializer.is_valid(),'serializer')
        print(serializer.errors,'errors')
        if serializer.is_valid():
            serializer.save()
            return Response( status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class SlotCreateAPIView(APIView):
    def post(self, request):
        serializer = PostSlotSerializers(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            print(doctor)
            date = serializer.validated_data['date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            slot_duration = int(serializer.validated_data['slot_duration'])
            slot_count = (datetime.datetime.combine(date, end_time) - datetime.datetime.combine(date, start_time)) // datetime.timedelta(minutes=slot_duration)

            slots = []
            current_time = start_time
            for _ in range(slot_count):
                slot = Slots(
                    doctor=doctor,
                    date=date,
                    start_time=current_time,
                    end_time=(datetime.datetime.combine(date, current_time) + datetime.timedelta(minutes=slot_duration)).time(),
                    status=True,
                    slot_duration=slot_duration,
                )
                slots.append(slot)
                current_time = (datetime.datetime.combine(date, current_time) + datetime.timedelta(minutes=slot_duration)).time()

            Slots.objects.bulk_create(slots)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class viewDoctorRequestView(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)  #
            serializer = PostDoctorSerializers(doctor, many=False)
            return Response(serializer.data) 
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})


class UsersDoctorsView(ListAPIView):
    serializer_class = DoctorsSerializers
    # queryset = Doctors.objects.filter(is_approved=True)
    def get_queryset(self):
        return Doctors.objects.filter(is_approved=True)
    

class getDoctorInHome(APIView):
    def get(self,request, id):
        try:
            doctor = Doctors.objects.get(id=id)
            serializer = DoctorsSerializers(doctor, many=False)
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})



class getUser(APIView):
    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})




class GetSlotsInHome(APIView):
    def get(self,request,id):
        print(id)
        slot = Slots.objects.filter(doctor=id,is_booked=False)
        print(slot)
        serializer = SlotSerializers(slot,many=True)

        return Response(serializer.data)
        
       
       
class CreateBlogAPIView(APIView):
    def post(self,request):
        print(request.data)
        serializer = PostBlogserializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response( status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetDoctorsBlog(APIView):
    def get(self,request,id):
        print(id)
        blog = Blogs.objects.filter(doctor=id)
        serializer = Blogsserializer(blog,many=True)
        return Response(serializer.data)


class GetSingleBlog(APIView):
    def get(self,request,id):
        blog = Blogs.objects.get(id=id)
        serializer = Blogsserializer(blog,many=False)
        return Response(serializer.data)



class BLogsListView(ListAPIView):
    serializer_class = Blogsserializer
    def get_queryset(self):
        return Blogs.objects.all()
    

class getSingleDocterAPIView(APIView):
    def get(self, request,id):
        try:
            user=User.objects.get(id=id)
            doctor = Doctors.objects.get(user=user)
            serializer = DoctorsSerializers(doctor, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctors.DoesNotExist:
            return Response("Docter not found", status=status.HTTP_404_NOT_FOUND)




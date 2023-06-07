from django.shortcuts import render
from accounts . models import User
from accounts . serializers import UserSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializer import (Appointmentserializer,DepartmentSerializers,PostDoctorSerializers,SlotSerializers,
PostSlotSerializers,DoctorsSerializers,)
from . models import Appointment,Department
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta
from . models import Doctors
# Create your views here.


class doctorsListView(ListAPIView):
    serializer_class = UserSerializer
    # get_queryset overridden to customize the queryset.
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

class AppointmentListView(ListAPIView):
    serializer_class = Appointmentserializer
    def get_queryset(self):
        return Appointment.objects.all()

class DepartmentListView(ListAPIView):
    serializer_class = DepartmentSerializers
    def get_queryset(self):
        return Department.objects.all()


@api_view(['POST'])
def createDepartment(request):
    serializer = DepartmentSerializers(data=request.data)
    print(serializer,'gshiguiuhsuidh')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



class DoctorsCreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = PostDoctorSerializers(data=request.data)
        print(serializer.is_valid(),'guygguuyvuuuu')
        print(serializer.errors,'jsoifjsdiofjiosjfsajfdji')
        if serializer.is_valid():
            serializer.save()
            return Response( status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class ScheduleAppointmentView(APIView):
#     def post(self, request):
#         serializer = Appointmentserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime, timedelta

class SlotCreateAPIView(APIView):
    def post(self, request):
        serializer = PostSlotSerializers(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()  # Save the slot object  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    

class AppointmentListAPIView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = Appointmentserializer(appointments, many=True)
        return Response(serializer.data)


class viewDoctorRequestView(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)  #
            serializer = PostDoctorSerializers(doctor, many=False)  # Pass many=False for a single object
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
    def get(self,request,id):
        try:
            doctor = Doctors.objects.get(id=id)
            serializer = DoctorsSerializers(doctor, many=False)
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})
        

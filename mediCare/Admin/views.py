from django.shortcuts import render
from Doctors . models import Doctors
from accounts . serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Doctors . serializer import DoctorsSerializers
# Create your views here.

class DoctorsRequestsView(ListAPIView):
    serializer_class = DoctorsSerializers
    # get_queryset overridden to customize the queryset.
    def get_queryset(self):
        return Doctors.objects.filter(is_approved=False)


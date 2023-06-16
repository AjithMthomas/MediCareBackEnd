from django.shortcuts import render
from Doctors . models import Doctors
from accounts . serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Doctors . serializer import DoctorsSerializers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

class DoctorsRequestsView(ListAPIView):
    serializer_class = DoctorsSerializers
    # get_queryset overridden to customize the queryset.
    def get_queryset(self):
        return Doctors.objects.filter(is_approved=False)

class AcceptDoctor(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)
            email = doctor.user.email
            doctor.is_approved = True
            doctor.user.is_staff = True
            doctor.save()
            current_site=get_current_site(request)
            mail_subject = 'Doctor request Accepted'
            message=render_to_string('acceptDoctor.html',{
                'doctor':doctor,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(doctor.user.pk)),
                'token':default_token_generator.make_token(doctor.user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])

            send_email.send()

            return Response({'msg': "Request accecpted successfully"})
        except doctor.DoesNotExist:
            return Response({'msg': "User not found"})
        except Exception as e:
            return Response({'message': str(e)})


class RejectDoctor(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)
            email = doctor.user.email
            current_site=get_current_site(request)
            mail_subject = 'Doctor request Rejected'
            message=render_to_string('rejectDoctor.html',{
                'doctor':doctor,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(doctor.user.pk)),
                'token':default_token_generator.make_token(doctor.user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            print(send_email)
            send_email.send()

            return Response({'msg': "Request accecpted successfully"})
        except doctor.DoesNotExist:
            return Response({'msg': "User not found"})
        except Exception as e:
            return Response({'message': str(e)})





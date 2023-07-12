from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from payment . models import Appointment
from payment .serializers import Appointmentserializer

from .serializers import UserSerializer
from accounts.models import User


# request to retrieve a list of available routes in an API.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        '/token/refresh'
    ]
    return Response(routes)


# user registration  and sending activate email
class UserRegistration(APIView):
     def post(self, request, format=None):
        email = request.data.get('email')
        print(request.data)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            mail_subject = 'Please activate your account'
            
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'usename': urlsafe_base64_encode(force_bytes(user.username))
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            return Response({'msg':'Registration Success'})
        
        return Response({'msg':'Registration Failed'})
    


#for activating user  and directing to login page   
@api_view(['GET'])
def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print('saved')
        return HttpResponseRedirect('https://www.medicarehealth.site/login')
        


#for obtaining the default token making costomization to it
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_superadmin 

        return token


# it will generate  a token and  send as response 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



#for validating email and senting reseting  mail to the user
class ForgotPasswordView(APIView):
     def post(self, request:Response):
        email = request.data['email']
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)

            current_site=get_current_site(request)
            mail_subject = 'Reset your password'
            message=render_to_string('Reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return Response({'message':'Forgot password mail sented Success','user':user.id})
        else:
            return Response({"message": "failed to sent msg"}, status=status.HTTP_400_BAD_REQUEST)


#for check for the user and directing to password reseting page
@api_view(['GET'])
def ResetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        return HttpResponseRedirect('https://www.medicarehealth.site/ResetPassword')
    else:
        return Response({'message':'Forgot password mail sented Success'}) 


#for reseting the the password
class ResetPasswordView(APIView):
    def post(self, request: Response):
        password = request.data['password']
        user_data = request.data['storedData']
        user_id = user_data['user']
       
        if password :
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return HttpResponseRedirect('https://www.medicarehealth.site/ResetPassword')


# for getting all the normal users in the platform
class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False, is_superadmin=False)



# for blocking  a user 
class BlockUser(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            print(user,'user')
            user.is_active = not user.is_active
            user.save()
            return Response({'msg': "Blocked successfully"})
        except user.DoesNotExist:
            return Response({'msg': "User not found"})
        except Exception as e:
            print('hi')
            return Response({'msg': str(e)})
        

        
# for getting the indvidual user and their related data
class GetSingleUser(APIView):
    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, many=False)
            appointment = Appointment.objects.filter(patient=id)
            if appointment or user :
                appointment_serializer = Appointmentserializer(appointment,many=True)
                return Response({'appointment':appointment_serializer.data,'userDetails':serializer.data})
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})

      
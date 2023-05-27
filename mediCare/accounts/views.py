from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from accounts.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        '/token/refresh'
    ]
    return Response(routes)


class UserRegistration(APIView):
     def post(self, request, format=None):
        email = request.data.get('email')
        print(request.data)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            current_site = get_current_site(request)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = default_token_generator.make_token(user)
            
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
    
    
@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        # userdata = request.session.get('userdata')
        # print('userd',userdata)
        # url = reverse('http://localhost:3000/login')

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()
        print('saved')

        return HttpResponseRedirect('http://localhost:3000/login')
        # return Response({"msg": "activated"})
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_superadmin 

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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


@api_view(['GET'])
def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        return HttpResponseRedirect('http://localhost:3000/ResetPassword')
    else:
        return Response({'message':'Forgot password mail sented Success'}) 

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
            return HttpResponseRedirect('http://localhost:3000/ResetPassword')
        


      
from django.shortcuts import render
from accounts . models import User
from accounts . serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

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
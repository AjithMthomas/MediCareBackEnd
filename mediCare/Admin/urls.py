from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('doctorsRequest/',views.DoctorsRequestsView.as_view(),name='doctorsRequest'),
]
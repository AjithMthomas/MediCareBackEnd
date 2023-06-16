from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('doctorsRequest/',views.DoctorsRequestsView.as_view(),name='doctorsRequest'),
    path('accept_doctor/<int:id>',views.AcceptDoctor.as_view(),name='accept_doctor/'),
    path('reject_doctor/<int:id>',views.RejectDoctor.as_view(),name='reject_doctor/'),
    
    
]
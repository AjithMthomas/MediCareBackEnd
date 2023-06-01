from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('doctors/',views.doctorsListView.as_view(),name='doctorsList'),
    path('blockDoctor/<int:id>/',views.blockDoctors.as_view(),name='blockDoctors')
]
from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('doctors/',views.doctorsListView.as_view(),name='doctorsList'),
    path('blockDoctor/<int:id>/',views.blockDoctors.as_view(),name='blockDoctors'),
    path('appointments/',views.AppointmentListView.as_view(),name="appointments"),
    path('departments/',views.DepartmentListView.as_view(),name="departments"),
    path('createDepartment/',views.createDepartment,name='createDepartment'),
    path('createDoctors/',views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
    path('shedule/',views.SlotCreateAPIView.as_view(),name='shedule')
]
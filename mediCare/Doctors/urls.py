from django.urls import path
from . import views


urlpatterns = [
    path('doctors/',views.doctorsListView.as_view(),name='doctorsList'),
    path('blockDoctor/<int:id>/',views.blockDoctors.as_view(),name='blockDoctors'),
    path('appointments/',views.AppointmentListView.as_view(),name="appointments"),
    path('departments/',views.DepartmentListView.as_view(),name="departments"),
    path('createDepartment/',views.createDepartment,name='createDepartment'),
    path('createDoctors/',views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
    path('shedule/',views.SlotCreateAPIView.as_view(),name='shedule'),
    path('viewDoctorRequest/<int:id>/', views.viewDoctorRequestView.as_view(), name='viewDoctorRequest'),
    path('docorsInUserSide/',views.UsersDoctorsView.as_view(),name='docorsInUserSide'),
    path('getDoctorInHome/<int:id>/',views.getDoctorInHome.as_view(),name='getDoctorInHome'),

]
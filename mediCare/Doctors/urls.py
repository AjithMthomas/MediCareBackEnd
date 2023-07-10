from django.urls import path
from . import views


urlpatterns = [
    # adminsid
    path('doctors/',views.DoctorsListView.as_view(),name='doctorsList'),
    path('blockDoctor/<int:id>/',views.BlockDoctors.as_view(),name='blockDoctors'),
    path('departments/',views.DepartmentListView.as_view(),name="departments"),
    path('createDepartment/',views.CreateDepartment,name='createDepartment'),
    path('createDoctors/',views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
    path('shedule/',views.SlotCreateAPIView.as_view(),name='shedule'),
    path('viewDoctorRequest/<int:id>/', views.ViewDoctorRequestView.as_view(), name='viewDoctorRequest'),
    path('EditDepartment/<int:pk>/',views.DepartmentUpdateAPIView.as_view(), name='department-update'),



    # userside
    path('docorsInUserSide/',views.UsersDoctorsView.as_view(),name='docorsInUserSide'),
    path('getDoctorInHome/<int:id>/',views.GetDoctorInHome.as_view(),name='getDoctorInHome'),
    path('get_user/<int:id>/',views.GetUser.as_view(),name='getUser'),
    path('getSlotsInHome/<int:id>/',views.GetSlotsInHome.as_view(),name='getSlotsInHome'),
    path('getDoctorsBlog/<int:id>/',views.GetDoctorsBlog.as_view(),name='getDoctorsBlog'),
    path('blogsList/',views.BLogsListView.as_view(),name='blogsList'),
    path('singleBlog/<int:id>/',views.GetSingleBlog.as_view(),name='singleBlog'),

    # doctor dashboard
    path('create-blogs/',views.CreateBlogAPIView.as_view(),name='create-blogs'),
    path('getSingleDocter/<int:id>',views.GetSingleDocterAPIView.as_view(),name='getSingleDocter'),

    

    
    

]
from django.urls import path
from .views import UserRegistration
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('', views.getRoutes),
    path('register/',UserRegistration.as_view()),
    path('login/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('activate/<uidb64>/<token> ', views.activate, name='activate'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('resetPassword_validate/<uidb64>/<token>/',views.resetPassword_validate,name='resetPassword_validate'),
    path('resetPassword/',views.ResetPasswordView.as_view(), name='reset_password'),

    # admin side
    path('users/',views.UsersListView.as_view(), name='user-list'),
    path('blockUser/<int:id>/',views.BlockUser.as_view(),name="blockUser") 
]
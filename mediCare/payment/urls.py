from django.urls import path
from . import views

urlpatterns = [
    path('pay/',views.start_payment.as_view(), name="payment"),
    path('payment/success/',views.handle_payment_success.as_view(), name="payment_success"),
    path('appointments/',views.AppointmentListView.as_view(),name="appointments"),
    path('appointmentsDoctor/<int:id>/',views. DoctorAppointmentsAPIView.as_view(), name='doctor_appointments'),
]

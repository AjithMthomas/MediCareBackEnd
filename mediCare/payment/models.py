from django.db import models
from accounts.models import User
from Doctors . models import Doctors,Slots

# Create your models here.

class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product


class Appointment(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_active':True,'is_staff':False,'is_superadmin':False})
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE)
    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('complete', 'Complete'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    appointment_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    # conulting_fee = models. DecimalField(max_digits=8,decimal_places=2)
    # date = models.DateField()
    # timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.doctor

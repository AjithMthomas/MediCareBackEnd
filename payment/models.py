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
    patient = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_active':True})
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE)
    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('approved', 'Approved'),
         ('rejected', 'Rejected'),
        ('complete', 'Complete'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    appointment_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doctor.user.username
  

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    patient = models.ForeignKey(User,on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.patient.username

from django.db import models
from accounts.models import User

# Create your models here.
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False)


class Slots(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    slot_duration  = models.IntegerField()
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=150)
    image = models.ImageField(upload_to='department/', null=True,)


    def __str__(self):
        return self.name

class Doctors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    address = models.CharField(max_length=100)
    specialization = models.ForeignKey(Department,on_delete=models.CASCADE)
    experience = models.IntegerField()
    fee =  models.DecimalField(max_digits=8 ,decimal_places=2)
    certificate = models.ImageField(upload_to='certificates/', null=True)
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE)

    def __str__(self) :
        return self.user.username



class Appointment(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_active':True,'is_staff':False,'is_superadmin':False})
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('complete', 'Complete'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    conulting_fee = models. DecimalField(max_digits=8,decimal_places=2)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE)


    
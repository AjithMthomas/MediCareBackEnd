from django.db import models
from accounts.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=350)
    image = models.ImageField(upload_to='department/', null=True,)


    def __str__(self):
        return self.name

class Doctors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_active':True})
    address = models.CharField(max_length=100)
    specialization = models.ForeignKey(Department,on_delete=models.CASCADE)
    experience = models.IntegerField()
    fee =  models.IntegerField()
    certificate = models.ImageField(upload_to='certificates/')
    is_approved=models.BooleanField(default=False)

    def __str__(self) :
        return self.user.username

class Slots(models.Model):
    doctor = models. ForeignKey(User,on_delete=models.CASCADE  )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    slot_duration  = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self) :
        return self.doctor.username
    






class Blogs(models.Model):
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE,limit_choices_to={'is_approved':True})
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='blogs/')
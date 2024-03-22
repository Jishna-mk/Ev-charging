from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from station_app.models import Station

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    age = models.IntegerField()
    vehicle_no=models.CharField(max_length=200,null=True,blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)


    def __str__(self):
        return self.user.username


class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    station=models.ForeignKey(Station,on_delete=models.CASCADE,related_name='bookings_as_station',null=True)
    slots=models.ForeignKey(Station,on_delete=models.CASCADE,related_name='bookings_as_slots',null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    date = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
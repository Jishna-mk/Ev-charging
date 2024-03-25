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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='bookings', null=True)
    slot_number = models.IntegerField(null=True)  # Modified
    start_time = models.CharField(max_length=10,null=True)
    end_time = models.CharField(max_length=10,null=True)
    date = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_items', null=True)
    status = models.CharField(max_length=20, default='Pending')

from station_app.models import StationProfile
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    station=models.ForeignKey(StationProfile,on_delete=models.CASCADE,null=True,blank=True)
    added_Date = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=200,null=True,blank=True)
    reply = models.BooleanField(default=False)
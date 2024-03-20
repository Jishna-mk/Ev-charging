from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

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

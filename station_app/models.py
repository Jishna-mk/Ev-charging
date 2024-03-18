from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StationProfile(models.Model):
    Phone_Number=models.IntegerField()
    Address=models.CharField(max_length=250)
    Profile_Image=models.FileField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    

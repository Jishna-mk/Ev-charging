from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StationProfile(models.Model):
   
    Phone_Number=models.IntegerField()
    Address=models.CharField(max_length=250)
    Profile_Image=models.FileField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    




class Station(models.Model):
    station_ID=models.AutoField(primary_key=True)
    station_name=models.CharField(max_length=200)
    station_address=models.CharField(max_length=200)
    station_price=models.CharField(max_length=200)
    station_phone=models.CharField(max_length=200)
    station_email=models.EmailField(max_length=200)
    station_caption=models.CharField(max_length=200)
    
    station_image=models.ImageField(null=True ,blank=True,upload_to="simages")
    station_area=models.CharField(max_length=200)
    slots=models.IntegerField(null=True,blank=True)



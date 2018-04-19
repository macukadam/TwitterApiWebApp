from django.db import models
import datetime
from django.contrib.auth.models import User

class Location(models.Model):
    Country = models.CharField(max_length=25)
    City = models.CharField(max_length=40)
    Longitude = models.DecimalField(max_digits=10, decimal_places=7)
    Latitude = models.DecimalField(max_digits=10, decimal_places=7)
    Altitude = models.DecimalField(max_digits=5, decimal_places=1)

class Disaster_Type(models.Model):
    Disaster_name = models.TextField()

class Disaster_Record(models.Model):
    Disaster_type = models.ForeignKey(Disaster_Type, on_delete=models.CASCADE)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)
    Record_date = models.DateField(auto_now_add=True, blank=True)
    Recod_time = models.TimeField(auto_now_add=True, blank=True)
    
class Tweet_Info(models.Model):
    Tweet = models.TextField()
    User_name = models.TextField()
    Tweet_time = models.DateTimeField()
    Tweet_latitude = models.DecimalField(default=None, blank=True, null=True,max_digits=9, decimal_places=6)
    Tweet_longitude = models.DecimalField(default=None, blank=True, null=True,max_digits=9, decimal_places=6)
    Location = models.TextField(default=None, blank=True, null=True)
    def __str__(self):
        return self.Tweet + " from " + self.User_name

class Disaster_Record_Tweet_Info(models.Model):
    Disaster = models.ForeignKey(Disaster_Record, on_delete=models.CASCADE)
    Tweet = models.ForeignKey(Tweet_Info, on_delete=models.CASCADE)
    def __str__(self):
        return self.Disaster

class User_Location(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Disaster_Location(models.Model):
    Disaster_record = models.ForeignKey(Disaster_Record, on_delete=models.CASCADE)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)
from django.db import models
from datetime import datetime

# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=64)
    mobile = models.CharField(max_length=16, null=True, blank=True)
    gender = models.CharField(max_length=16)
    dob = models.CharField(max_length=16)
    token = models.CharField(max_length=128, unique=True)
    email = models.EmailField(null=True, blank=True)

    interests = models.ManyToManyField("Interest", blank=True)
    profile1 = models.URLField(blank=True, null=True)
    profile2 = models.URLField(blank=True, null=True)
    profile3 = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    facebook = models.CharField(max_length=128, null=True, blank=True)
    insta = models.CharField(max_length=128, null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True)
    linkedin = models.CharField(max_length=128, null=True, blank=True)

    facebook_public = models.BooleanField(default=False)
    insta_public = models.BooleanField(default=False)
    twitter_public = models.BooleanField(default=False)
    linkedin_public = models.BooleanField(default=False)

    facebook_active = models.BooleanField(default=False)
    insta_active = models.BooleanField(default=False)
    twitter_active = models.BooleanField(default=False)
    linkedin_active = models.BooleanField(default=False)

    saved_profiles = models.ManyToManyField("UserProfile", blank=True)
    last_lat = models.FloatField(null=True, blank=True)
    last_lon = models.FloatField(null=True, blank=True)
    distance = models.IntegerField(default=10)
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        day, month, year = self.dob.split("/")
        duration = datetime.now() - datetime(int(year), int(month), int(day))
        return int(duration.days / 365)

class InterestCategory(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey("InterestCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

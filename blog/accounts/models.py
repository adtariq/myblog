from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

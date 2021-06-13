from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    userpoint = models.IntegerField(max_length=100, default=0)
    korname = models.CharField(max_length=100)
    # otpdata = models.IntegerField(default=0)
    usenums = models.IntegerField(default=0)
    phonenum = models.CharField(max_length=100, default=0)
    auth = models.CharField(max_length=100)



class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()

    def __str__(self):
        return self.postname
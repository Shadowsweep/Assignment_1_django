from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
    ]
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES, blank=False, default='Patient')
    first_name = models.CharField(max_length=244,blank=False, default='')
    last_name = models.CharField(max_length=255,blank=False, default='')
    profile_picture = models.ImageField(upload_to='static/', blank=True)
    address_line1 = models.CharField(max_length=255,blank=False, default='')
    city = models.CharField(max_length=100,blank=False, default='')
    state = models.CharField(max_length=100,blank=False, default='')
    pincode = models.CharField(max_length=10,blank=False, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    

class Blog(models.Model):
    user_type = models.CharField(max_length=255, blank=False, default='Doctor')
    username = models.CharField(max_length=255,null=True,blank=True,default='')
    title = models.CharField(max_length=255,null=True,blank=True,default='')
    image = models.ImageField(upload_to='static/', blank=True)
    category = models.CharField(max_length=255,null=True,blank=True,default='')
    summary = models.CharField(max_length=2000,null=True,blank=True,default='')
    content = models.CharField(max_length=2000,null=True,blank=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True,blank=True, default='')

from django.db import models
from django.contrib.auth.models import User
import uuid

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,default="user.jpg")
    bio = models.TextField(max_length=500, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    pincode = models.CharField(max_length=6,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    user_uu = models.CharField(max_length=100, null = True, blank = True, unique = True)

    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if not self.user_uu:
            self.user_uu = str(uuid.uuid4())
        super(UserExtra,self).save(*args, **kwargs)
        
    @property
    def username(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        

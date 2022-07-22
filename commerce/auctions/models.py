from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField(auto_now_add=True, editable=False)
    end_date = models.DateField(null=True, blank=True)
    item_image = models.ImageField(upload_to ='uploads/', null=True, blank=True)
    
    def __str__(self):
        return self.title
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.db import models


class User(AbstractUser):
    pass

categories=[
    ('sport', 'Sport'),
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('cars', 'Cars'),
    ('art', 'Art'),
]

class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField(auto_now_add=True, editable=False)
    end_date = models.DateField()
    item_image = models.ImageField(upload_to ='uploads/', default="")
    
    def __str__(self):
        return self.title
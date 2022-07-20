from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.title
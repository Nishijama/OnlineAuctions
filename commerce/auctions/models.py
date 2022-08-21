from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
 
class User(AbstractUser):
    
    def __str__(self):
        return self.username

class Listing(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_auctions")
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=10, default="active", choices = [('active','active'), ('closed', 'closed')])
    category = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=1500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField(auto_now_add=True, editable=False)
    # end_date = models.DateField(null=True, blank=True)
    item_image = models.ImageField(upload_to ='uploads/', null=True, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_items")
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_bids", null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def snip_description(self):
        if len(self.description) < 60:
            snippet = self.description
        else:
            snippet = f"{self.description[:60]} ..."
        return snippet

    def snip_title(self):
        if len(self.title) < 80:
            snippet = self.title
        else:
            snippet = f"{self.title[:80]} ..."
        return snippet    

    def close_auction(self):
        self.state = 'closed'

class Comment(models.Model):

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.CharField(max_length=200, default="Anonymous")
    body = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.body[:50]  

class Bid(models.Model):
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=2)


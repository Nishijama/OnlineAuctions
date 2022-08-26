from statistics import mode
from termios import TIOCPKT_DOSTOP
from tkinter import CASCADE
from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
 
class User(AbstractUser):
    
    def __str__(self):
        return self.username

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_auctions")
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=10, default="active", choices = [('active','active'), ('closed', 'closed')])
    category = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=1500)
    initial_price = models.DecimalField(max_digits=8, decimal_places=2, default = 0.00)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    start_date = models.DateField(auto_now_add=True, editable=False)
    item_image = models.ImageField(upload_to ='uploads/', null=True, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_items")
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
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
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placed_bids')
    value = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.listing} | {self.bidder} | {self.value}"

@receiver(pre_save, sender=Bid)
def bid_save_handler(instance, *args, **kwargs):
    listing = Listing.objects.get(id=instance.listing.id)
    if instance.value > listing.current_price:
        listing.current_price = instance.value
        listing.highest_bidder = instance.bidder
        listing.save()
    else:
        print("Bid is lower than current price!")

@receiver(post_delete, sender=Bid)
def bid_deleted_handler(instance, *args, **kwargs):
    listing = Listing.objects.get(id=instance.listing.id)
    bids = Bid.objects.filter(listing = listing)
    # check if any beds have been placed 
    if bids:
        bids = [(bid.value, bid.bidder) for bid in (listing.bids.all())]
        if instance.value > bids[-1][0]:
            print('The highest bid was just deleted - price and highest bidder were adjusted accordingly')
            # if the bid deleted was the highest bid, set the higest bid value and the highest bidder
            # to whatever bid is next on the stack, also works for bulk deletion
            listing.current_price = bids[-1][0]
            listing.highest_bidder = bids[-1][1]
            listing.save()
        else:
            print('The bid deleted was not the top bid')
    else:
        listing.current_price = listing.initial_price
        listing.highest_bidder = None
        listing.save()

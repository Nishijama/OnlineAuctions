from django.contrib import admin

# from auctions.models import Listing, Comment, User, Bid
from .models import Listing, Comment, User, Bid
# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Bid)

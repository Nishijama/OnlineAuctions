from django.contrib import admin

from auctions.models import Listing, Comment
from .models import Listing, Comment
# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)

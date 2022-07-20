from django.contrib import admin

from auctions.models import Listing
from .models import Listing
# Register your models here.
admin.site.register(Listing)
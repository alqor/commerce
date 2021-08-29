from django.contrib import admin
from django.db.models.fields import IntegerField
from .models import ItemCategory, Listing, Bid, Watchlist
# Register your models here.
admin.site.register(ItemCategory)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
from django.contrib import admin
from django.db.models.fields import IntegerField
from .models import ItemCategory, Listing, Bid

# Register your models here.
admin.site.register(ItemCategory)
admin.site.register(Listing)
admin.site.register(Bid)
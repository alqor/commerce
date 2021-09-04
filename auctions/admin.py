from django.contrib import admin
from django.db.models.fields import IntegerField
from .models import ItemCategory, Listing, Bid, Watchlist, Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_filter = ('listed_by', 'category', 'status')

class BidAdmin(admin.ModelAdmin):
    list_filter = ('item', 'bid_by', 'is_start')

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('author', 'item')


admin.site.register(ItemCategory)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment, CommentAdmin)
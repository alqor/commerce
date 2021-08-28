from django import forms
from .models import ItemCategory, Listing, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'img_url', 'category']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value",]


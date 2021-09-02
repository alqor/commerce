from django import forms
from .models import ItemCategory, Listing, Bid
from django.utils.translation import gettext_lazy as _

FORM_ATTRS = {'class':"item-field form-control"}


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'img_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs=FORM_ATTRS),
            'description': forms.Textarea(attrs={'rows':"5", 'class':"item-field form-control"}),
            'img_url': forms.TextInput(attrs=FORM_ATTRS),
            'category': forms.Select(attrs=FORM_ATTRS)

        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value", ]
        labels = {
            'bid_value': _('Start Bid'),
        }
        widgets = {
            'bid_value': forms.NumberInput(attrs={'min':1, 'class':"item-field form-control"})}


class BidFormSmall(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value", ]
        widgets = {
            'bid_value': forms.NumberInput(attrs={'min':1, 'class':"bid-field form-control"})}
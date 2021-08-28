from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
# from django.shortcuts import get_object_or_404
from django.views import View

from .models import *
from .forms import *

def get_newest_price(item_id):
    bids = Bid.objects.filter(item=item_id)
    if bids: 
        max_bid = bids.order_by('-bid_value')[0].bid_value
    else:
        max_bid = 0
    #     max_bid = Listing.objects.get(pk=item_id).start_bid
    
    return max_bid

def index(request):
    active_items = Bid.objects.filter(item__status='Active') 
    max_bids_items = active_items.values('item',
                                          'item__id',
                                          'item__title',
                                          'item__list_date',
                                          'item__img_url').annotate(Max('bid_value'))
    # items_with_bids = {item:get_newest_price(item.pk) for item in items}      
    # print(items_with_bids)
    print(max_bids_items)
    return render(request, "auctions/index.html", {'items':max_bids_items})


class ItemCard(FormMixin, DetailView):
    template_name = 'auctions/item.html'
    model = Listing

    context_object_name = 'item'
    form_class = BidForm

    def get_success_url(self):
        return reverse('item-card', kwargs={'pk': self.object.id})
        

    def get_context_data(self, **kwargs):
        context = super(ItemCard, self).get_context_data(**kwargs)  
        context['form'] = BidForm(initial={'item': self.object})
        context['max_bid'] = get_newest_price(self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data['bid_value'] <= get_newest_price(self.object.id):
                return self.form_invalid(form)
            saved_form = form.save(commit=False)
            saved_form.bid_by = User.objects.get(username=request.user)
            saved_form.item = Listing.objects.get(pk=self.object.id)
            saved_form.save()
            print('saved')
            return HttpResponseRedirect('/thank-you')
        else:
            return self.form_invalid(form)
    
class Categories(ListView):
    template_name = 'auctions/categories.html'
    model = ItemCategory
    context_object_name = 'cats'

class CategoriesList(ListView):
    template_name = 'auctions/index.html'

    context_object_name = 'items'
    def get_queryset(self, *args, **kwargs):
        cat_id = self.kwargs.get('cat_id')
        active_items = Bid.objects.filter(item__status='Active', item__category=cat_id) 
        max_bids_items = active_items.values('item',
                                          'item__id',
                                          'item__title',
                                          'item__list_date',
                                          'item__img_url').annotate(Max('bid_value'))
        return max_bids_items

class Watchlist(ListView):
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def save_listing(listing_form, request):
    saved_form = listing_form.save(commit=False)
    
    saved_form.listed_by = User.objects.get(username=request.user)
    saved_form.save()
    return saved_form.id


@login_required
def list_new_item(request):   
    if request.method == 'POST':
        list_item_form = ListingForm(request.POST)
        bid_form = BidForm(request.POST)
        if list_item_form.is_valid() and bid_form.is_valid():
            id = save_listing(list_item_form, request)

            bid_form.save(commit=False)
            bid_form.bid_by = User.objects.get(username=request.user)
            bid_form.item = id
            return HttpResponseRedirect('/thank-you')
        else:
            print('something goes wrong')
    else:
        list_item_form = ListingForm()
        bid_form = BidForm()
        list_item_form.listed_by = User.objects.get(username=request.user)
    return render(request, 'auctions/add_listing.html', {'list_item_form':list_item_form,
                                                         'bid_form':bid_form,
                                                        })

@login_required
def thank_you(request):
    return render(request, 'auctions/thank_you.html')



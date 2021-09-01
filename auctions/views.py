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

def index(request):
    active_items = Listing.objects.filter(status='Active') 
    return render(request, "auctions/index.html", {'items':active_items})

class Categories(ListView):
    template_name = 'auctions/categories.html'
    model = ItemCategory
    context_object_name = 'cats'

def items_by_cat(request, cat_id):
    active_items = Listing.objects.filter(status='Active', category=cat_id) 
    return render(request, "auctions/index.html", {'items':active_items})

def item_page(request, id):
    item = Listing.objects.get(pk=id)
    is_wl=None
    if request.user.is_authenticated:
        is_wl = is_watchlisted(request.user, id)
    return render(request, "auctions/item.html", {"item": item, "wl":is_wl})

def is_watchlisted(user, id):
    watchlist = Watchlist.objects.filter(author=user)
    if watchlist and watchlist.first().item.filter(pk=id):
        return True 

@login_required
def watchlist_manipulator(request, item_id):
    user = request.user
    # list_item = Listing.objects.get(pk=item_id)
    if is_watchlisted(user, item_id):
        watchlist = Watchlist.objects.get(author=user)
        watchlist.item.remove(item_id)
        # return HttpResponseRedirect(f'/{item_id}')
    else:
        if Watchlist.objects.filter(author=user):
           watchlist = Watchlist.objects.get(author=user)
           watchlist.item.add(item_id)
        else:
           watchlist = Watchlist(author=user)
           watchlist.save()
           watchlist.item.add(item_id)
    return HttpResponseRedirect(f'/{item_id}')

@login_required
def watchlist_items(request):
    wl_items = Watchlist.objects.filter(author=request.user)
    if wl_items:
        active_items = wl_items[0].item.all()
        return render(request, "auctions/index.html", {'items':active_items})
    else:
        return render(request, "auctions/index.html", {'items':active_items})


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
            raise ValidationError('bid val')
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

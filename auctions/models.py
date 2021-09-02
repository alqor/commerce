from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.db.models import Max


class User(AbstractUser):
    pass


class ItemCategory(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        """
        to use in html templates
        """
        return reverse('list-by-cat', args=[self.id])

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    img_url = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(ItemCategory, on_delete=CASCADE, related_name='listing_items')
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), 
                                                        ('Closed', 'Closed')], default='Active')
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='listing_items')
    list_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.listed_by}'
    
    def get_absolute_url(self):
        """
        to use in html templates
        """
        return reverse('item-page', args=[self.id])
    
    def max_bid(self):
        bids = Listing.objects.all().get(pk=self.id).bids.all()
        max_bid = bids.aggregate(Max('bid_value'))
        return max_bid['bid_value__max']
    
    def is_watchlisted(self):
        pass
    

class Bid(models.Model):
    bid_value =  models.IntegerField(validators=[MinValueValidator(1)])
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                                 related_name='bids')
    bid_date = models.DateField(auto_now_add=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name='bids')

    def __str__(self):
        return f'{self.bid_value} on {self.item} from {self.bid_by}'


class Comment(models.Model):
    comment_text =  models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                            null=True, related_name='comments')
    publish_date = models.DateField(auto_now_add=True)


class Watchlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                            null=True, related_name='watchlist_items')
    item = models.ManyToManyField(Listing)

    def __str__(self):
        return f'{self.author}'
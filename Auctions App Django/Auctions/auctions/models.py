from distutils.command.upload import upload
from statistics import mode
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
import datetime
from datetime import datetime
import datetime
from django.utils import timezone



#model: one for auction listings, one for bids, and one for comments made
# on auction listings. It’s up to you to decide what fields each
# model should have, and what the types of those fields should be.
#  You may have additional models if you would like.

class User(AbstractUser):
    
    watched_list = models.ManyToManyField("List", default='',blank=True ,related_name="watched_list_by_user")

    def __str__(self):
        return f"{self.username}"


category_choices = (("Automotive","Automotive"),("Beauty","Beauty"),("Books","Books"),("Collectibles","Collectibles"),("Craft","Craft"),("Electronics","Electronics"),("Entertainment","Entertainment"),("Fashion","Fashion"),("Garden","Garden"),("Home","Home"),("Office","Office"),("Sports","Sports"),("Toys","Toys"))
class List(models.Model):
    now = timezone.now()

    owner = models.ForeignKey(User,on_delete=models.CASCADE , related_name="owned_list")
    title=models.CharField(max_length=64)
    category = models.CharField(max_length=64 ,choices=category_choices)
    description = models.CharField(max_length=2048)
    starting_bid = models.DecimalField(max_digits=8 ,editable=True, decimal_places=2)
    image_url = models.CharField(max_length=40096)
    closed = models.BooleanField(default=False)

    time=models.DateTimeField( auto_now=True)
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name="purchased_listings")

    def __str__(self):
        return f"{self.title} by {self.owner} : {self.description} with {self.starting_bid}"




class Bids(models.Model):
    list  = models.ForeignKey(List, on_delete=models.CASCADE,related_name="bids")
    aurthor = models.ForeignKey(User , on_delete=models.CASCADE,related_name="bids_made")
    bid_offer = models.DecimalField(max_digits=8 , decimal_places=2)



    def clean(self):
        if self.bid_offer > self.list.starting_bid:
            # self.list.starting_bid = self.bid_offer
            # self.listing.save()
            # print(self.listing.current_price)
            return True
        else:
            return False




    def __str__(self):
        return f"{self.list} by {self.aurthor} offered {self.bid_offer}"

   



class Comments(models.Model):
    user =models.ForeignKey(User, related_name="comments_made", on_delete=models.CASCADE)
    comments = models.CharField(max_length=2048)
    list = models.ForeignKey(List , on_delete=models.CASCADE , related_name="comments_have")

    def __str__(self):
        return f"comment by {self.user} : {self.comments[:20]} on list {self.list}"

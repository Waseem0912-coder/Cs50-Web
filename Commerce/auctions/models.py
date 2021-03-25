from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
 
class Bidder(models.Model):
    user = models.CharField(max_length=64)
    bidded_price= models.IntegerField()

class Comments(models.Model):
    user = models.CharField(max_length=64)
    comments_description= models.CharField(max_length=256)
    comments_title = models.CharField(max_length=64)

class Category(models.Model):
    category=models.CharField(max_length=20)
    

class Listing(models.Model):
    bid_owner= models.CharField(max_length=64)
    bid_title= models.CharField(max_length=64)
    bid_description= models.CharField(max_length=200)
    bid_image=models.CharField(max_length=200, blank=True)
    bid_starting_price = models.IntegerField()
    #bid_current_price = 2#join
    current_bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE, related_name="bidder")
    bid_categories = models.ManyToManyField(Category, related_name="tag")
    bid_comments = models.ManyToManyField(Comments, blank=True, related_name="comments")
    bid_status = False
    def __str__(self):
        return f"{self.id}: Owner: {self.bid_owner} Titlekj {self.current_bidder}"


class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing = models.ManyToManyField(Listing)

class Winners(models.Model):
    owner= models.CharField(max_length=64)
    winner= models.CharField(max_length=64)
    listingid= models.IntegerField()
    win_price= models.IntegerField()
    title= models.CharField(max_length=64, null=True)



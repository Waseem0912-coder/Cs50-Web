from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
 

class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} put a bid in for {self.price}"


class Category(models.Model):
    category=models.CharField(max_length=20, blank=True)
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_coms")
    title = models.CharField(max_length=25, default="")
    comment = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"

class Listing(models.Model):
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owners")
    bid_title= models.CharField(max_length=64)
    bid_description= models.CharField(max_length=200)
    bid_image=models.CharField(max_length=200, blank=True)
    bid_starting_price = models.IntegerField()
    bid_time= models.DateTimeField(auto_now_add=True, blank=True)
    #bid_current_price = 2#join
    current_bidder = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bidder_now")
    bid_comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    bid_categories = models.ManyToManyField(Category,blank=True, related_name="tag")
    bid_status = False
    def __str__(self):
        return f"{self.bid_title}: is {self.current_bidder.price} and is being sold by {self.bid_owner}"


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing)

class Winners(models.Model):
    owner= models.CharField(max_length=64)
    winner= models.CharField(max_length=64)
    listingid= models.IntegerField()
    win_price= models.IntegerField()
    title= models.CharField(max_length=64, null=True)



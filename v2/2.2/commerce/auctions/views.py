from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from  .models import *
from .models import User
from django import forms

class CreateBid(forms.Form):
    bid_title= forms.CharField(label="Type in the title of the entry", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_description = forms.CharField(label="Type in the description of the bid", widget=forms.Textarea(attrs={ 'class' : 'form-control' }))
    bid_image= forms.CharField(label="Enter the link to an image", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_starting_price=forms.IntegerField(label="Enter the starting price for the bid")

class Comment_form(forms.Form):
    title_of_form = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-4 col-lg-4'}))
    comment_of_form = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'class' :'form-control'}))





def index(request):
    return render(request, "auctions/index.html")


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

def test(request, list_id):
   bid= Listing.objects.get(pk=list_id)
   comments= Comment.objects.filter(bid=list_id)
   cat = Category.objects.filter(bid=list_id)
   status = bid.bid_status
   fm = Comment_form(request.POST or None)
   if(request.method=="POST"):
       com= Comment.objects.get(bid=list_id)
       com.user= request.user.username
       com.title= request.POST["title_of_form"]
       com.comment= request.POST["comment_of_form"]
       com.save()
   return render(request, "auctions/test.html", {"fm":fm, "status":status, "bid":bid, "comments":comments, "cat":cat })
   









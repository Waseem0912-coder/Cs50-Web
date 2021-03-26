from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from .models import * 
from django import forms

class CreateBid(forms.Form):
    bid_title= forms.CharField(label="Type in the title of the entry", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_description = forms.CharField(label="Type in the description of the bid", widget=forms.Textarea(attrs={ 'class' : 'form-control' })) 
    bid_image= forms.CharField(label="Enter the link to an image", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_starting_price=forms.IntegerField(label="Enter the starting price for the bid")

class Comment(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-4 col-lg-4'}))
    comment = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'class' :'form-control'}))


def index(request):
    bid_total= Listing.objects.count()
    return render(request, "auctions/index.html", {
        'bid':bid_total
        }
        )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")





#if logged in show the dashboard with active listings
@login_required(login_url='/login')
def watchlist(request):
    watchlist= Watchlist.objects.all()
    if len(watchlist)==0:
        watchlist="No biddings added to watchlist"
    return render(request, "auctions/watchlist.html", {
            "watchlist":watchlist
            })


@login_required(login_url='/login')
def activelist(request):
    active = Listing.objects.filter(bid_status=True)
    if len(active)==0:
        active= "No bids currently"
    return render(request, "auctions/activelist.html", {
        "active": active
        })


@login_required(login_url='/login')
def add_listing(request):
    if request.method == "POST":
        create= CreateBid(request.POST)
        if create.is_valid():
            new_bid= Listing()
            new_bid.bid_title= create.cleaned_data["bid_title"]
            new_bid.bid_description= create.cleaned_data["bid_description"]
            new_bid.bid_image= create.cleaned_data["bid_image"]
            new_bid.bid_starting_price= create.cleaned_data["bid_starting_price"]
            if len(new_bid.bid_image) ==0:
                new_bid.bid_image ="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" 
            new_bid.save()
            return HttpResponseRedirect(reverse("auctions:activelist"))
        else:
            return render(request, "auctions/error.html")
 

def error(request):
    return render(request, "auctions/error.html")
def test(request, listing_id):
    l = Listing.objects.get(pk=listing_id)
    k= l.bid_comments.all()
    r= l.bid_categories.all()
    m = l.current_bidder
    if(request.method=="POST"):
        create = Comment(request.POST)
        if create.is_valid():
            k.comments_title= create.cleaned_data["title"]
            k.comments_description=create.cleaned_data["commet"]
            k.user= request.user.username
            k.save()

    return render(request,"auctions/testing.html", {
        "l":l, "k":k, "r":r,"m":m
        } )















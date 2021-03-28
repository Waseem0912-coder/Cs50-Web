from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from  .models import *
from .models import User
from django.db.models import Max
from django import forms

class CreateBid(forms.Form):
    bid_title= forms.CharField(label="Type in the title of the entry", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_description = forms.CharField(label="Type in the description of the bid", widget=forms.Textarea(attrs={ 'class' : 'form-control' }))
    bid_image= forms.CharField(label="Enter the link to an image", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_starting_price=forms.IntegerField(label="Enter the starting price for the bid")
    bid_category= forms.CharField(label="Tags", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))


class Comform(forms.Form):
    title_of_form = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-4 col-lg-4'}))
    comment_of_form = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'class' :'form-control'}))





def index(request):
    return HttpResponseRedirect(reverse("active_list"))



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

def views_list(request, list_id):
   bid= Listing.objects.get(pk=list_id)
   comments= Comment.objects.filter(bid=list_id)
   cat = Category.objects.filter(bid=list_id)
   usr = request.user
   status = bid.bid_status
   return render(request, "auctions/views_list.html", {"status":status, "bid":bid, "comments":comments, "cat":cat,"form":Comform() })


def com_make(request, list_id):
   bid= Listing.objects.get(pk=list_id)
   cat = Category.objects.filter(bid=list_id)
   usr = request.user
   status = bid.bid_status
   if request.method=="POST":
       form = Comform(request.POST)
       if form.is_valid():
           obj = Comment()
           obj = Comment(user=usr, bid=bid,title=form.cleaned_data["title_of_form"],comment=form.cleaned_data["comment_of_form"])
           obj.save()
           return HttpResponseRedirect(reverse("views_list", args=(bid.id,)))


def create(request):
    if request.method=="POST":
        form= CreateBid(request.POST)
        if form.is_valid():
            usr= request.user
            obj= Listing()
            obj = Listing(bid_owner=usr,bid_title=form.cleaned_data["bid_title"],bid_description=form.cleaned_data["bid_description"], bid_image=form.cleaned_data["bid_image"],bid_starting_price=form.cleaned_data["bid_starting_price"])
            obj.save()
            cat = Category()
            cat=Category(category=form.cleaned_data["bid_category"])
            cat.save()
            cat.bid.add(obj)
            return HttpResponseRedirect(reverse("views_list", args=(obj.id,)))
    else:
        form= CreateBid()
        return render(request, "auctions/create.html", {"form":form
        })



#@login_required(login_url='/login')
def active_list(request):
    obj = Listing.objects.filter(bid_status=1)
    k=0
    l = []
    for x in obj:
        j = Bid.objects.filter(bid_id=x).exists()
        if j:
            r= Bid.objects.all().aggregate(Max('price'))
            l.append(r)
    j=0
    m=3
    return render(request, "auctions/active_list.html", {"obj":obj, "l":l, "j":j, "m":m})


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
    bid_image= forms.CharField(required=False, label="Enter the link to an image", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    bid_starting_price=forms.IntegerField(label="Enter the starting price for the bid")
    bid_category= forms.CharField(label="Tags", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))


class Comform(forms.Form):
    title_of_form = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-4 col-lg-4'}))
    comment_of_form = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'class' :'form-control'}))

class BidForm(forms.Form):
    bidded = forms.IntegerField(required=False, label="Place a bid")

class bidstatForm(forms.Form):
    bid_stat= forms.BooleanField(required=False, label="Stop the bid")



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
   uu= False
   status = bid.bid_status
   watch= False
   if Watchlist.objects.filter(user=usr, listing=bid).exists():
       watch= True
   j = Bid.objects.filter(bid_id=bid).exists()
   if j:
       j= Bid.objects.filter(bid_id=bid)
       l= j.order_by('-price')
       l= l.first()
       j= l.price
   else:
       j=bid.bid_starting_price
   bidForm=0
   if usr!= bid.bid_owner:
       bidForm = BidForm(request.POST)
   else:
       bidForm= bidstatForm()
   c_valid = False
   if len(comments)>0:
       c_valid=True
   if request.method=="POST":
       mkbid = BidForm(request.POST)
       if mkbid.is_valid():
           obj_bid= Bid()
           obj_bid=Bid(bid_id=bid,user=request.user, price=mkbid.cleaned_data["bidded"])
           obj_bid.save()
           if obj_bid.price >j:
               j= obj_bid.price
   owns=False
   Winner=0
   if bid.bid_owner==request.user:
        owns=True
   if bid.bid_status==False:
        Winner="You have Won!"
   bid.bid_price=j
   bid.save()
   if  Winners.objects.filter(listing=bid).exists():
       a = Winners.objects.get(listing=bid)
       if a.user==request.user:
            uu=True
   return render(request, "auctions/views_list.html", {"status":status, "bid":bid, "comments":comments, "cat":cat,"form":Comform(), "j":j,"bidForm":bidForm, "watch":watch,"usr":usr, "c_valid":c_valid,"owns":owns,"Winner":Winner, "uu":uu })


def make_bid(request, list_id):
    bid = Listing.objects.get(pk=list_id)
    l=False
    if request.user == bid.bid_owner:
        l=True
    if request.method=="POST":
        form= BidForm(request.POST)
        if form.is_valid():
            k= Bid.objects.get(bid_id=bid)
            f =form.cleaned_data["bidded"]
            if f>k:
                k= Bid(user=usr,price=f)
                k.save()
                return HttpResponseRedirect(reverse("views_list", args=(bid.id)))


def bid_control(request, list_id):
    bid = Listing.objects.get(pk=list_id)
    if request.method=="POST":
        bid.bid_status=0
        l= bid.bid_price
        bid.save()
        k = Bid.objects.filter(bid_id=list_id) 
        k= k.order_by("-price")
        k= k.first()
        k= k.user
        w = Winners()        
        w= Winners(user=k, listing=bid,win_price=l)
        w.save()
        return HttpResponseRedirect(reverse("views_list", args=(list_id,)))

def add_watch(request, list_id):
    if request.method=="POST":
        w = Watchlist()
        l = Listing.objects.get(pk=list_id)
        w = Watchlist(user=request.user, listing=l)
        k = l.id
        w.save()
        return HttpResponseRedirect(reverse("views_list", args=(l.id,)))




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
            obj = Listing(bid_owner=usr,bid_title=form.cleaned_data["bid_title"],bid_description=form.cleaned_data["bid_description"], bid_starting_price=form.cleaned_data["bid_starting_price"])
            if form.cleaned_data["bid_image"]:
                obj.bid_image = form.cleaned_data["bid_image"]
            else:
                obj.bid_image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            obj.bid_price=form.cleaned_data["bid_starting_price"]
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

@login_required(login_url='/login')
def watch_list(request):
    usr = request.user
    f= Watchlist.objects.filter(user=usr)
    w= False
    if len(f) > 0: 
        w=f
    return render(request, "auctions/watch_list.html", {
        "w":w
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

@login_required(login_url='/login')
def cat(request):
    c = Category.objects.all()
    x=0
    if len(c)>0:
        x=1
    j = len(c)
    return render(request, "auctions/cat.html", {
        "c":c, "x":x, "j":j
        })
@login_required(login_url='/login')
def cat_view(request, cat_id):
    c= Category.objects.get(pk=cat_id)
    c=c.category
    cat= Category.objects.get(pk=cat_id)
    obj = cat.bid.all()
    if len(obj) <=0:
        obj=False
    return render(request, "auctions/cat_view.html", {
        "obj":obj,"c":c 
        })




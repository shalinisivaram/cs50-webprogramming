from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . models import *
from .forms import *



def index(request):
    return render(request,"auctions/index.html",{
        'listings':Listing.objects.all()
    })
            

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


@login_required
def newlist(request):
        if request.method == "POST":
           
            form = Listing_Form(request.POST,request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.owner = request.user
                listing.save()
                return HttpResponseRedirect(reverse(index))
            else:
                return render(request,"auctions/newlist.html",{
                     "form" : form
                })
        else:
            return render(request,"auctions/newlist.html",{
                'form':Listing_Form()})
            
@login_required        
def viewlisting(request, listing_id):
    comments = Comment.objects.filter(listing_id=listing_id)
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        if not listing.closed:
            if request.POST.get("button") == "Close": 
                listing.closed = True
                listing.save()

            newbid = int(request.POST.get('newbid'))
            if listing.bid >= newbid:
                listing = Listing.objects.get(id=listing_id)
                return render(request, "auctions/viewlisting.html", {
                    "listing": listing,
                    "message": "Your Bid should be higher than the Current Bid.",
                    "msg_type": "danger",
                    "comments": comments
                })
        
            else:
                listing.bid = newbid
                listing.save()
      
                bidobj = Bid.objects.filter(listing_id=listing_id)
                if bidobj:
                    bidobj.delete()
                obj = Bid()
                obj.user = request.user.username
                obj.title = listing.title
                obj.listing_id = listing.id
                obj.bid = newbid
                obj.save()
                return render(request, "auctions/viewlisting.html", {
                    "listing": listing,
                    "message": "Your Bid added Successfully.",
                    "msg_type": "danger",
                    "comments": comments
                })
        
  
    else:
        listing = Listing.objects.get(id=listing_id)
        added = Watchlist.objects.filter(
            listingid=listing_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "listing": listing,
            "added": added,
            "comments": comments
        })

@login_required
def addtowatchlist(request,listing_id):
    obj = Watchlist.objects.filter(listingid = listing_id,user=request.user.username)
    if obj:
        obj.delete()
        listing = Listing.objects.get(id = listing_id)
        added = Watchlist.objects.filter(listingid = listing_id,user=request.user.username)
        comments = Comment.objects.filter(listing_id = listing_id)
        return render(request,"auctions/viewlisting.html",{
             'listing': listing,
             'added':added,
             'comments': comments
        })
    else:
        listing = Listing.objects.get(id = listing_id)
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = listing_id
        obj.listing = listing
        obj.save()
        
        added = Watchlist.objects.filter(listingid = listing_id,user=request.user.username)
        comments = Comment.objects.filter(listing_id = listing_id)
        return render(request,"auctions/viewlisting.html",{
             'listing': listing,
             'added':added,
             'comments': comments
         })

@login_required
def addcomment(request,listing_id):
        obj = Comment()
        comment = request.POST.get('comment')
        obj.user = request.user.username
        obj.listing_id = listing_id
        obj.comment = comment
        obj.save()
        comments = Comment.objects.filter(listing_id = listing_id,user=request.user.username)
        added = Watchlist.objects.filter(listingid = listing_id,user=request.user.username)
        listing = Listing.objects.get(id = listing_id)
        
        return render(request,"auctions/viewlisting.html",{
            'listing':listing,
            'added':added,
            'comments':comments,

        })

@login_required           
def closebid(request,listing_id):
  winobj = Winner()
  listobj = Listing.objects.get(id=listing_id)
  obj = Bid.objects.filter(listing_id=listing_id)
  if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
  else:
        bidobj = Bid.objects.get(listing_id=listing_id)
        winobj.owner = request.user.username
        winobj.winner = bidobj.user
        winobj.listingid = listing_id
        winobj.price = bidobj.bid
        winobj.title = bidobj.title
        winobj.save()
        message = "Bid Closed"
        msg_type = "success"
        bidobj.delete()

  if Watchlist.objects.filter(listingid=listing_id):
        watchobj = Watchlist.objects.filter(listingid=listing_id)
        watchobj.delete()
  
  if Comment.objects.filter(listing_id=listing_id):
        commentobj = Comment.objects.filter(listing_id=listing_id)
        commentobj.delete()
    
  listobj.delete()
   
  winners = Winner.objects.all()
  
  empty = False
  if len(winners) == 0:
    empty = True
  return render(request, "auctions/winlist.html", {
        "products": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type
    })


@login_required
def winlist(request):   
  
  user = User.objects.get(username = request.user) 
  winners = Winner.objects.filter(winner = user)
  empty = False
  if len(winners) == 0:
    empty = True
  return render(request, "auctions/winlist.html", {
        "products": winners,
        "empty": empty
    })
    
    
def categories(request):
    return render(request,"auctions/categories.html",{
        "categories": Categories,
    })

def category(request,category):
    listing = Listing.objects.filter(category = category)
    empty = False
    if len(listing) == 0:
        empty = True
    return render(request,"auctions/category.html",{
        "products":listing,
        "empty":empty,
        "category ": category
    })

def watchlist(request):
     user = User.objects.get(username = request.user)
     return render(request,"auctions/watchlist.html",{
        'watchlist':Watchlist.objects.all()
    })



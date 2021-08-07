from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, NullBooleanField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.db.models.lookups import Transform

Categories = (
    ('Accessories','Accessories'),
    ('Concealer','Concealer'),
    ('Makeup Brush','Makeup Brush'),
)


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bid = models.IntegerField()
    category = models.CharField(max_length=12,choices=Categories,default=[1])
    image = models.ImageField(null = True, blank = True)
    time = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)


class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    bid = models.IntegerField()


class Comment(models.Model):
    user =  models.CharField(max_length=64)
    comment = models.CharField(max_length=100)
    listing_id = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
   user = models.CharField(max_length=64)
   listingid = models.IntegerField()
   listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="watchlist",default="")
   
    
class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    price = models.IntegerField()
    listingid = models.IntegerField()
    title = models.CharField(max_length=200)
    




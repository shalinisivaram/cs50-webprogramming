from django.db.models import fields
from django.forms import ModelForm
from django import forms

from .models import *

class Listing_Form (ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','bid','category','image']

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
            'bid' : forms.NumberInput(attrs={'class':'form-control'}),
            'category' : forms.Select(attrs={'class':'form-control'}),
            'image' : forms.FileInput(attrs={'class':'form-control'})

        }
    
from email.policy import default
from django import forms
from .models import Bid, Listing, Comment

categories=[
    ('other', 'Choose category'),
    ('sport', 'Sport'),
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('cars', 'Cars'),
    ('art', 'Art'),
    ('other', 'Other')
]

class NewListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title','price', 'category', 'item_image', 'description')
        
        labels = {
            "title": "",
            "price": "",
            "description": "",
            "category": "",
            
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control new_listing_form', 'placeholder': "Title",}),
            'item_image': forms.FileInput(attrs={'class' : "form-control-file new_listing_form"}),
            'category': forms.Select(choices=categories, attrs={'class': 'form-control new_listing_form'}),
            'description': forms.Textarea(attrs={'class': 'form-control new_listing_form', 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'min':0, 'class': 'form-control new_listing_form', 'placeholder': 'Price'}),
            }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            "body": "",
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control new_listing_form', 'placeholder': 'Comment'}),
        }

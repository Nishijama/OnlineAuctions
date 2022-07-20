from django import forms
from .models import Listing

categories=[
    ('', 'Choose category'),
    ('sport', 'Sport'),
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('cars', 'Cars'),
    ('art', 'Art'),
]

class NewListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title','price', 'category','end_date', 'description')
        widgets = {
            'category': forms.Select(choices=categories),
            'description': forms.Textarea,
            'price': forms.NumberInput(attrs={'min':0}),
            }
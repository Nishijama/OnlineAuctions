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
        fields = ('title', 'category', 'description')
        widgets = {
            'category': forms.Select(choices=categories),
            'description': forms.Textarea,
            }
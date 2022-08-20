
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment
from .forms import NewListingForm, CommentForm
from decimal import Decimal

def index(request, category="All"):
    if request.method=="POST":
        if "search_submit" in request.POST:
            search_data = request.POST.dict()
            search_term = search_data.get("q")
            return HttpResponseRedirect(f"/search_results/{search_term}")

        elif "close_submit" in request.POST:
            l = Listing.objects.get(id=request.POST['close_submit'])
            l.close_auction()
            l.save()
            return HttpResponseRedirect(reverse("index"))

        elif "watch_submit" in request.POST:
            listing = Listing.objects.get(id=request.POST['watch_submit'])
            user = request.user

            listing.watchers.add(user)
            print("Added " + listing.title + " to " + user.username + "'s watchlist")

            # return HttpResponseRedirect(reverse("index"))


    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(state="active")
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

def new_listing(request):

    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm()
        })

def listing(request, listing_id):
    l = Listing.objects.get(id=listing_id)

    if request.method == "POST":
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_commennt = form.save(commit=False)
                new_commennt.listing = l
                new_commennt.author = request.user.username
                new_commennt.save()

        elif 'close_submit' in request.POST:
            l.close_auction()
            l.save()
            return HttpResponseRedirect(reverse("index"))
            
        elif "watch_submit" in request.POST:
            listing = Listing.objects.get(id=request.POST['watch_submit'])
            user = request.user

            listing.watchers.add(user)
            print("Added " + listing.title + " to " + user.username + "'s watchlist")


    return render(request, "auctions/listing.html", {
        "listing": l,
        "min_next_price": "{:.2f}".format(l.price + Decimal(0.01)),
        "comments": l.comment_set.all(),
        "comment_form": CommentForm(),
        "watchers": l.watchers.all()
    })

def categories(request):
    if request.method == "POST":
        category = request.POST.dict()
        category = category.get("category").lower()
        return HttpResponseRedirect(f"/categories/{category}")

    else:
        return render(request, "auctions/categories.html",{
            "categories": [
                "Art", 
                "Cars",
                "Electronics",
                "Fashion",
                "Home",
                "Sport", 
                "Toys",
                "Other",
                ]
        })

def category(request, category):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(category=category, state="active")
    })

def search_results(request, search_term):
    matching_results = []
    for listing in Listing.objects.filter(state="active"):
        if search_term.lower() in listing.title.lower():
            matching_results.append(listing)

    return render(request, "auctions/index.html", {
        # "search_term": search_term,
        "listings": matching_results,
    })


def watchlist(request):
    user = request.user

    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["watch_remove"])
        listing.watchers.remove(user)
        pass

    return render(request, "auctions/watchlist.html", {
        "watched_items": user.watched_items.all(),
        
    })
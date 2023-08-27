"""
Core app views.
"""
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse

from django.contrib.auth import get_user_model


def index(request):
    """Main page view."""
    return render(request, "core/index.html")


def register(request):
    """Register page view."""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,
                          "core/register.html",
                          {"email_placeholder": email,
                           "alert": "Passwords do not match."})

        try:
            user = get_user_model().objects.create_user(email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request,
                          "core/register.html",
                          {"email_placeholder": email,
                           "alert": "Username already taken."})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "core/register.html")


def login_view(request):
    """Log in view."""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request,
                            email=email,
                            password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,
                          "core/login.html",
                          {"email_placeholder": email,
                           "alert": "User could not be authenticated."})

    else:
        return render(request, "core/login.html")



def logout_view(request):
    """Log out view."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))

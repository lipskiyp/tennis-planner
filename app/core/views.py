"""
Core app views.
"""
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse
from django.views import View


class IndexView(View):
    """Main page view."""
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MySessionsView(View):
    """My sessions view."""
    template_name = "core/mysessions.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    """Register page view."""
    template_name = "core/register.html"

    def get(self, request, *args, **kwarsg):
        return render(request, self.template_name)

    def post(self, request, *args, **kwarsg):
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,
                        self.template_name,
                        {"email_placeholder": email,  # fill email field with user input
                        "alert": "Passwords do not match."})

        try:
            user = get_user_model().objects.create_user(email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request,
                        self.template_name,
                        {"alert": f"User: {email} already exists."})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """Login page view."""
    template_name = "core/login.html"

    def get(self, request, *args, **kwarsg):
        return render(request, self.template_name)

    def post(self, request, *args, **kwarsg):
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
                          self.template_name,
                          {"email_placeholder": email,  # fill email field with user input
                           "alert": "User could not be authenticated."})


class LogoutView(View):
    """Log out view."""
    def get(self, request, *args, **kwarsg):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


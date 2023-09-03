"""
Core app url configuration.
"""
from django.urls import path, include

from core import views


app_name = 'core'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("mysessions", views.MySessionsView.as_view(), name="mysessions")
]
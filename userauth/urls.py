from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "userauth"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    # path("", include('django.contrib.auth.urls')),
]


# login/ [name='login']
# logout/ [name='logout']

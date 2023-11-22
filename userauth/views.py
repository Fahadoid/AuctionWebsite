from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, get_user_model
import django.contrib.auth as auth
import api.mailer as mailer


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    """User login method"""
    if request.user.is_authenticated:
        # User is already logged in, redirect to root path
        return HttpResponseRedirect("/")

    # User isn't logged in yet
    if request.method == "GET":
        # GET method
        template = loader.get_template("login.html")
        return HttpResponse(template.render(None, request))
    else:
        # POST method
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            # Redirect to root path
            return HttpResponseRedirect("/")
        else:
            template = loader.get_template("login.html")
            return HttpResponse(
                template.render(
                    {"error_msg": "Invalid credentials."},
                    request,
                )
            )


def logout(request: HttpRequest) -> HttpResponse:
    """User logout method"""
    auth.logout(request)
    return HttpResponseRedirect("/")


@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    """User signup method"""
    if request.user.is_authenticated:
        # User is already logged in, redirect to root path
        return HttpResponseRedirect("/")

    # User isn't logged in yet
    if request.method == "GET":
        # GET method
        template = loader.get_template("signup.html")
        return HttpResponse(template.render(None, request))
    else:
        # POST method
        email = request.POST["email"]
        password = request.POST["password"]
        dob = request.POST["dob"]

        User = get_user_model()
        user = User(email=email, dob=dob)
        user.set_password(password)
        try:
            user.save()
            mailer.welcome_user(user)
        except Exception as e:
            template = loader.get_template("signup.html")
            return HttpResponse(template.render({"error_msg": str(e)}, request))

        auth.login(request, user)
        # Redirect to root path
        return HttpResponseRedirect("/")


def health(request: HttpRequest) -> HttpResponse:
    """required by openshift"""
    return HttpResponse("")

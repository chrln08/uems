from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages import error, info
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, NewEventForm

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        error(request, "You are not logged in. Please log in first.")
        return redirect("login")

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)

            return redirect("main")
        else:
            error(request, "Username or password is incorrect. Please try again.")
    elif request.user.is_authenticated:
        return redirect("main")
    
    form = LoginForm()

    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        info(request, "You have been logged out.")
    
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get("email"))
            error(request, "Failed to register. This email has already been registered in the system. Please try again.")
        except ObjectDoesNotExist as dne:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)

                return redirect("main")
            else:
                error(request, "Failed to register. Please ensure that you have meet the criteria in each field.")

    elif request.user.is_authenticated:
        return redirect("main")
    
    form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
    
def events_view(request):
    if request.user.is_authenticated:
        return render(request, "events/index.html")
    else:
        error(request, "You are not logged in. Please log in first.")

        return redirect("login")
    
def new_event_view(request):
    if request.user.is_authenticated:
        # todo - GET and POST data; if POST save if GET, get event data; rename function
        if request.method == "POST":
            form = NewEventForm(request.POST)
            if form.is_valid():
                form.save()

                info(request, "New event has been created successfully.")

                return redirect("events")
            else:
                error(request, "Failed to create new event. Please ensure that you have filled the details correctly.")

                return redirect("new_event")
            
        form = NewEventForm()
        
        return render(request, "events/create.html", {"form": form})
    else:
        error(request, "You are not logged in. Please log in first.")

        return redirect("login")

def profile_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get("old_email") is None:
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    info(request, "Your password has been changed successfully. Please log in again.")

                    return redirect("login")
                else:
                    error(request, "Failed to change password. Please ensure that you have followed each step correctly and retry again.")

                    return redirect("profile")
            else:
                if request.POST.get("old_email") == request.user.email:
                        try:
                            user = User.objects.get(email=request.POST.get("new_email"))

                            error(request, "Error saving new email. The new email is already in use.")

                            return redirect("profile")
                        except ObjectDoesNotExist as dne:
                            user = User.objects.get(email=request.user.email)
                            user.email = request.POST.get("new_email")
                            user.save()
                            request.user.email = request.POST.get("new_email")

                            info(request, "Your email has been changed successfully.")

                            return redirect("profile")
                else:
                    error(request, "Email mismatch. Please try again.")

                    return redirect("profile")


        pwChange = PasswordChangeForm(request.user)

        return render(request, "profile/index.html", {"password_form": pwChange})
    else:
        error(request, "You are not logged in. Please log in first.")

        return redirect("login")
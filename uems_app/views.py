from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages import error, info
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm

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
    
def events(request):
    if request.user.is_authenticated:
        return render(request, "events/index.html")
    else:
        error(request, "You are not logged in. Please log in first.")

        return redirect("login")
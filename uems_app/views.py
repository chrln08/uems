from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, EventForm, AttendeeForm
from .models import Event, Attendee

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        messages.error(request, "You are not logged in. Please log in first.")
        return redirect("login")

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Username or password is incorrect. Please try again.")
    elif request.user.is_authenticated:
        return redirect("main")

    form = LoginForm()
    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get("email"))
            messages.error(request, "This email has already been registered.")
        except ObjectDoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("main")
            else:
                messages.error(request, "Failed to register. Please check each field carefully.")
    elif request.user.is_authenticated:
        return redirect("main")

    form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})

def profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in. Please log in first.")
        return redirect("login")

    if request.method == 'POST':
        if request.POST.get("old_email") is None:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                messages.info(request, "Your password has been changed successfully. Please log in again.")
                return redirect("login")
            else:
                messages.error(request, "Failed to change password. Please ensure all fields are correct.")
        else:
            # Email change logic
            if request.POST.get("old_email") == request.user.email:
                try:
                    User.objects.get(email=request.POST.get("new_email"))
                    messages.error(request, "Error saving new email. The new email is already in use.")
                except ObjectDoesNotExist:
                    user = User.objects.get(email=request.user.email)
                    user.email = request.POST.get("new_email")
                    user.save()
                    messages.info(request, "Your email has been changed successfully.")
            else:
                messages.error(request, "Email mismatch. Please try again.")

        return redirect("profile")

    pwChange = PasswordChangeForm(request.user)
    return render(request, "profile/index.html", {"password_form": pwChange})

class EventListView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'
    paginate_by = 12

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/view.html'
    context_object_name = 'event'

def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            if request.user.is_authenticated:
                attendee.user = request.user
            attendee.save()
            messages.success(request, "Successfully registered for the event!")
            return redirect(event.get_absolute_url())
    else:
        form = AttendeeForm()
    return render(request, 'events/register.html', {'form': form, 'event': event})

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create.html'
    success_url = reverse_lazy('events_list')

def new_event_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in. Please log in first.")
        return redirect("login")

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "New event has been created successfully.")
            return redirect("events")
        else:
            messages.error(request, "Failed to create event. Please check your inputs.")
    else:
        form = EventForm()

    return render(request, "events/create.html", {"form": form})

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/update.html'
    success_url = reverse_lazy('events_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You are not authorized to edit events.")
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You are not authorized to delete events.")
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
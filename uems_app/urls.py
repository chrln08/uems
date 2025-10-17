from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('events/', views.events_view, name="events"),
    path('events/create', views.new_event_view, name="new_event"),
    path('profile/', views.profile_view, name="profile")
]
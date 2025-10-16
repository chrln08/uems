from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('events/', views.events, name="events")
]
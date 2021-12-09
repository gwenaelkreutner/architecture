from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

from .views import fridge_display, recipe_display, search_recipe_display

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('fridge/', fridge_display, name='fridge'),
    path('recipe/', recipe_display, name='recipe'),
    path('search/', search_recipe_display, name='search'),
]

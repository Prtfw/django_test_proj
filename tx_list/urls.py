from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('profile/', views.profile, name='profile'),
	path('delete/<list_id>', views.delete, name='delete'),
	path('edit/<list_id>', views.edit, name='edit'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('edit_profile/', views.edit_profile, name='edit_profile'),
	path('password/', views.change_pswd, name='change_pswd'),
	path('stripe_pay/', views.stripe_pay, name='stripe_pay'),
]

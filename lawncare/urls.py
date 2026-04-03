from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/booking/', views.booking_api, name='booking_api'),
    path('dashboard/', views.custom_dashboard, name='dashboard'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('login/', auth_views.LoginView.as_view(template_name='lawncare/login.html'), name='login'),
]
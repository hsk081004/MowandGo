from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.custom_dashboard, name='dashboard'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
from django.contrib import admin
from django.urls import path
from lawncare import views

urlpatterns = [
    path('admin/', admin.site.name_view),
    path('', views.home_view, name='home'),
    path('dashboard/', views.custom_dashboard, name='dashboard'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
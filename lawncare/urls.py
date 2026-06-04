from django.urls import path
from . import views

urlpatterns = [
    # Frontend Page
    path('', views.home_view, name='home'),
    
    # API for the booking form
    path('api/booking/', views.booking_api, name='booking_api'),
    
    # Custom CRM Dashboard
    path('dashboard/', views.custom_dashboard, name='dashboard'),

    # --- NEW: Status Update Route (Approve/Reject) ---
    path('update-status/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_status'),

    # Delete Route
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
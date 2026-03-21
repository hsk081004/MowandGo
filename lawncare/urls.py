from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('api/booking/', views.booking_api),
    path('dashboard/', views.custom_dashboard),
    path('delete/<int:booking_id>/', views.delete_booking),
]
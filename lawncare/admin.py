from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'preferred_date', 'is_completed', 'created_at')
    list_filter = ('service', 'is_completed', 'preferred_date')
    search_fields = ('name', 'phone', 'email')
    date_hierarchy = 'preferred_date'
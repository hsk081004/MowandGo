from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # 1. The Table View (What you already had, which is great)
    list_display = ('name', 'phone', 'service', 'preferred_date', 'is_completed', 'created_at')
    list_filter = ('service', 'is_completed', 'preferred_date')
    search_fields = ('name', 'phone', 'email')
    date_hierarchy = 'preferred_date'
    
    # --- SAAS UPGRADES ---
    
    # 2. Quick Edits: Allows the client to check the "completed" box directly from the main list without opening the record.
    list_editable = ('is_completed',)
    
    # 3. Pagination: Keeps the table loading instantly even when they have 1,000+ customers.
    list_per_page = 25 
    
    # 4. Read-Only Protection: Prevents the client from accidentally changing the date the booking was submitted.
    readonly_fields = ('created_at',)
    
    # 5. Fieldsets: When they click a specific booking, this organizes the form into beautiful, logical sections instead of a messy list.
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Job Details', {
            'fields': ('service', 'preferred_date', 'is_completed')
        }),
        ('System Log', {
            'fields': ('created_at',),
            'classes': ('collapse',) # This minimizes the section by default to keep the screen clean
        }),
    )
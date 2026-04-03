from django.contrib import admin
from django.urls import path, include

# =========================
# CUSTOM ADMIN HEADERS
# =========================
admin.site.site_header = "Mow & Go CRM Dashboard"
admin.site.site_title = "Mow & Go Admin"
admin.site.index_title = "Welcome to the Operations Center" 

# =========================
# URL ROUTING
# =========================
urlpatterns = [
    # The new Jazzmin SaaS Dashboard
    path('admin/', admin.site.urls), 
    
    # Your custom app routes (frontend form, login, etc.)
    path('', include('lawncare.urls')), 
]
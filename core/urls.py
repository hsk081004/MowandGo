from django.contrib import admin
from django.urls import path, include

# =========================
# CUSTOM ADMIN HEADERS
# =========================
admin.site.site_header = "Greenzo CRM Dashboard"
admin.site.site_title = "Greenzo Admin"
admin.site.index_title = "Welcome to the Operations Center" 

# =========================
# URL ROUTING
# =========================
urlpatterns = [
    # The SaaS Dashboard
    path('admin/', admin.site.urls), 
    
    # 🟢 ADD THIS LINE: This turns on Django's built-in login/logout system!
    path('', include('django.contrib.auth.urls')),
    
    # Your custom app routes (frontend form, CRM, etc.)
    path('', include('lawncare.urls')), 
]
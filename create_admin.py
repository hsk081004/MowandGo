import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Configuration - CHANGE THESE TO YOUR LIKING
username = 'admin'
email = 'Neel.30898@gmail.com'
password = 'Neel@123'  # Change this to something strong!

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ SUCCESS: Superuser '{username}' created!")
else:
    print(f"ℹ️ INFO: Superuser '{username}' already exists.")
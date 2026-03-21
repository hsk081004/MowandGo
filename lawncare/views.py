import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from .models import Booking


# ✅ HOME PAGE (ONLY HTML)
def home_view(request):
    return render(request, 'lawncare/index.html')


# ✅ API FOR BOOKING (ONLY JSON)
@csrf_exempt
def booking_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Save to Database
            booking = Booking.objects.create(
                name=data.get('Name'),
                phone=data.get('Phone'),
                email=data.get('Email'),
                address=data.get('Address'),
                service=data.get('Service'),
                preferred_date=data.get('Date'),
                message=data.get('Message')
            )

            # Email
            subject = f"Mow & Go | New Booking from {booking.name}"
            email_body = f"""
=========================================
🌿 MOW & GO - NEW BOOKING REQUEST 🌿
=========================================

Name: {booking.name}
Phone: {booking.phone}
Email: {booking.email}
Address: {booking.address}
Service: {booking.get_service_display()}
Date: {booking.preferred_date}

Message:
{booking.message if booking.message else "No message provided."}

Dashboard:
https://mowandgo-4hxy.onrender.com/dashboard/
=========================================
"""

            try:
                send_mail(
                    subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking saved and email sent!'
                })

            except Exception as email_error:
                print("EMAIL ERROR:", email_error)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking saved (email pending)'
                })

        except Exception as e:
            print("GENERAL ERROR:", e)
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'message': 'Invalid request'}, status=405)


# --- CUSTOM ADMIN DASHBOARD ---
@staff_member_required(login_url='/admin/login/')
def custom_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'lawncare/admin_dashboard.html', {'bookings': bookings})


# --- DELETE BOOKING ---
@staff_member_required(login_url='/admin/login/')
def delete_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
    return redirect('dashboard')
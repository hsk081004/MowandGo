import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Booking


# ✅ HOME PAGE (ONLY HTML)
def home_view(request):
    return render(request, 'lawncare/index.html')


# ✅ API FOR BOOKING (STRICT JSON API)
@csrf_exempt
@require_POST
def booking_api(request):
    try:
        # ✅ Parse JSON safely
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)

        # ✅ Validate required fields
        required_fields = ['Name', 'Phone', 'Address', 'Date', 'Service']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'{field} is required'
                }, status=400)

        # ✅ Save to Database
        booking = Booking.objects.create(
            name=data.get('Name'),
            phone=data.get('Phone'),
            email=data.get('Email'),
            address=data.get('Address'),
            service=data.get('Service'),
            preferred_date=data.get('Date'),
            message=data.get('Message')
        )

        # ✅ Email Content (SAFE)
        subject = f"Mow & Go | New Booking from {booking.name}"
        email_body = f"""
New Booking

Name: {booking.name}
Phone: {booking.phone}
Email: {booking.email}
Address: {booking.address}
Service: {booking.service}
Date: {booking.preferred_date}

Message: {booking.message}
"""

        # ✅ SAFE EMAIL BLOCK (VERY IMPORTANT)
        email_status = "sent"
        try:
            send_mail(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,   # 🔥 FIX HERE
            )
        except Exception as email_error:
            print("EMAIL ERROR:", email_error)
            email_status = "failed"

        # ✅ ALWAYS RETURN JSON (NO HTML EVER)
        return JsonResponse({
            'status': 'success',
            'message': 'Booking saved successfully',
            'email_status': email_status
        })

    except Exception as e:
        print("FULL ERROR:", e)

        return JsonResponse({
            'status': 'error',
            'message': str(e)   # show real error for debugging
        }, status=500)


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
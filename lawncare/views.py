import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from .models import Booking


# HOME PAGE
def home_view(request):
    return render(request, 'lawncare/index.html')


# BOOKING API
@csrf_exempt
@require_POST
def booking_api(request):
    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)

        required_fields = ['Name', 'Phone', 'Address', 'Date', 'Service']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'{field} is required'
                }, status=400)

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

        subject = f"GreenZo | New Booking from {booking.name}"

        email_body = f"""
<h2 style="color:#2e7d32;">🌿 New Lawn Service Booking</h2>
<table style="border-collapse: collapse; width: 100%; font-family: Arial;">
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Name</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.name}</td></tr>
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Phone</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.phone}</td></tr>
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Email</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.email}</td></tr>
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Address</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.address}</td></tr>
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Service</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.service}</td></tr>
<tr><td style="border:1px solid #ddd; padding:8px;"><b>Preferred Date</b></td><td style="border:1px solid #ddd; padding:8px;">{booking.preferred_date}</td></tr>
</table>
<br>
<p style="color:#555;">This booking was submitted from the <b>Greenzo Website</b>.</p>
"""

        email_status = "sent"
        try:
            email = EmailMessage(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['harshkadikar@gmail.com'] # Keep this as your notification email
            )
            email.content_subtype = "html"
            email.send()
        except Exception as email_error:
            print("EMAIL ERROR:", email_error)
            email_status = "failed"

        return JsonResponse({
            'status': 'success',
            'message': 'Booking saved successfully',
            'email_status': email_status
        })

    except Exception as e:
        print("FULL ERROR:", e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# DASHBOARD
@login_required(login_url='/login/')
def custom_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'lawncare/admin_dashboard.html', {
        'bookings': bookings
    })


# --- NEW: UPDATE BOOKING STATUS (APPROVE/REJECT) ---
@login_required(login_url='/login/')
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # 1. Update the status
    if action == 'approve':
        booking.status = 'Approved'
        subject = "Booking Confirmed! 🌿 - Greenzo"
        message_body = f"""
        <div style="font-family: Arial; color: #333;">
            <h2 style="color: #2e7d32;">Great news, {booking.name}!</h2>
            <p>Your lawn care booking for <b>{booking.preferred_date}</b> has been <b>Approved</b>.</p>
            <p>Our team will arrive at your address: <i>{booking.address}</i></p>
            <br>
            <p>See you soon!</p>
            <p><b>- The Greenzo Team</b></p>
        </div>
        """
    elif action == 'reject':
        booking.status = 'Rejected'
        subject = "Update regarding your Greenzo Booking"
        message_body = f"""
        <div style="font-family: Arial; color: #333;">
            <h2>Hello {booking.name},</h2>
            <p>Thank you for reaching out to Greenzo. Unfortunately, we are unable to fulfill your booking for <b>{booking.preferred_date}</b> at this time.</p>
            <p>We apologize for the inconvenience. Please feel free to book another available slot on our website.</p>
            <br>
            <p>Best regards,</p>
            <p><b>- The Greenzo Team</b></p>
        </div>
        """
    
    booking.save()

    # 2. Send email to the CONSUMER (using Resend)
    if booking.email:
        try:
            email = EmailMessage(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [booking.email] # To the Customer
            )
            email.content_subtype = "html"
            email.send()
            print(f"STATUS EMAIL SENT TO {booking.email}")
        except Exception as e:
            print("STATUS EMAIL ERROR:", e)

    return redirect('dashboard')


# DELETE BOOKING
@login_required(login_url='/login/')
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('dashboard')
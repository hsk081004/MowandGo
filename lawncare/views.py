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

        booking = Booking.objects.create(
            name=data.get('Name'),
            phone=data.get('Phone'),
            email=data.get('Email'),
            address=data.get('Address'),
            service=data.get('Service'),
            preferred_date=data.get('Date'),
            message=data.get('Message')
        )

        subject = f"Mow & Go | New Booking from {booking.name}"

        email_body = f"""
<h2 style="color:#2e7d32;">🌿 New Lawn Service Booking</h2>

<table style="border-collapse: collapse; width: 100%; font-family: Arial;">
<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Name</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.name}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Phone</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.phone}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Email</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.email}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Address</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.address}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Service</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.service}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Preferred Date</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.preferred_date}</td>
</tr>

<tr>
<td style="border:1px solid #ddd; padding:8px;"><b>Message</b></td>
<td style="border:1px solid #ddd; padding:8px;">{booking.message if booking.message else "No message provided"}</td>
</tr>
</table>

<br>

<p style="color:#555;">This booking was submitted from the <b>Mow & Go Lawn Care website</b>.</p>
"""

        email_status = "sent"

        try:
            email = EmailMessage(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )

            email.content_subtype = "html"
            email.send()

            print("EMAIL SENT SUCCESSFULLY")

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

        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


# DASHBOARD
@login_required(login_url='/login/')
def custom_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')

    return render(request, 'lawncare/admin_dashboard.html', {
        'bookings': bookings
    })


# DELETE BOOKING
@login_required(login_url='/login/')
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()

    return redirect('dashboard')
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from .models import Booking

@csrf_exempt
def home_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the frontend
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

            # Prepare Email Notification
            subject = f"Mow & Go | New Booking from {booking.name}"
            email_body = f"""
            =========================================
             🌿 MOW & GO - NEW BOOKING REQUEST 🌿
            =========================================
            
            Customer Details:
            Name:       {booking.name}
            Phone:      {booking.phone}
            Email:      {booking.email}
            Address:    {booking.address}
            Service:    {booking.get_service_display()}
            Date:       {booking.preferred_date}
            
            Message:
            {booking.message if booking.message else "No message provided."}
            
            -----------------------------------------
            Manage at: https://mowandgo-4hxy.onrender.com/dashboard/
            =========================================
            """
            
            # Try to send the email
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success', 'message': 'Booking saved and email sent!'})
                
            except Exception as email_error:
                # Log the email error but don't crash the website!
                print(f"\n--- CRITICAL EMAIL ERROR ---")
                print(f"{email_error}")
                print(f"----------------------------\n")
                
                # We return 'success' because the booking WAS saved to the DB, 
                # even if the email notification is just being slow.
                return JsonResponse({'status': 'success', 'message': 'Booking saved (Email notification pending).'})

        except Exception as e:
            print(f"\n--- CRITICAL GENERAL ERROR ---")
            print(f"{e}")
            print(f"------------------------------\n")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # For GET requests, render the page
    return render(request, 'lawncare/index.html')

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
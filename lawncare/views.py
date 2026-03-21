import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .models import Booking

def home_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the frontend fetch request
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

            # Send Email Notification
            subject = f"Mow & Go | New Booking from {booking.name}"
            message = f"""
            =========================================
             🌿 MOW & GO - NEW BOOKING REQUEST 🌿
            =========================================
            
            Hello! You have received a new service request from your website. 
            Here are the customer's details:

            Customer Name:     {booking.name}
            Phone Number:      {booking.phone}
            Email Address:     {booking.email}
            Service Address:   {booking.address}
            Service Requested: {booking.get_service_display()}
            Preferred Date:    {booking.preferred_date}
            
            Additional Message/Details: 
            {booking.message if booking.message else "No message provided."}
            
            -----------------------------------------
            Manage this request in your admin dashboard: 
            https://mowandgo-4hxy.onrender.com/dashboard/
            =========================================
            """
            
            # Try to send the email
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER], # Sending to yourself
                    fail_silently=False,
                )
                email_status = "and email sent."
                
            except Exception as email_error:
                # THIS WILL PRINT THE EXACT REASON GOOGLE IS REJECTING IT
                print(f"\n--- CRITICAL EMAIL ERROR ---")
                print(f"{email_error}")
                print(f"----------------------------\n")
                
                # Tell the frontend to show the error
                return JsonResponse({'status': 'error', 'message': 'Email failed to send. Check logs.'}, status=400)

            return JsonResponse({'status': 'success', 'message': f'Booking saved {email_status}'})

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
    # Fetch all bookings, newest first
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'lawncare/admin_dashboard.html', {'bookings': bookings})

# --- DELETE BOOKING ---
@staff_member_required(login_url='/admin/login/')
def delete_booking(request, booking_id):
    if request.method == 'POST':
        # Find the booking by its ID and delete it
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
    
    # Refresh the dashboard page
    return redirect('dashboard')
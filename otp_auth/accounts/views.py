# accounts/views.py
import random
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from .forms import EmailForm, OTPForm
from .models import OTPVerification

def generate_otp():
    # Generate a 6-digit OTP code
    return f"{random.randint(100000, 999999)}"

def registration_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Generate OTP and save it
            otp_code = generate_otp()
            otp_record = OTPVerification.objects.create(email=email, otp_code=otp_code)
            
            # Send email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp_code}. It will expire in 5 minutes.",
                from_email=None,  # uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[email],
            )
            # Store email in session to use in OTP verification view
            request.session['email'] = email
            return redirect('accounts:otp_verification')
    else:
        form = EmailForm()
    return render(request, 'accounts/registration.html', {'form': form})

def otp_verification_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('accounts:registration')

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            try:
                otp_record = OTPVerification.objects.filter(email=email, verified=False).latest('created_at')
            except OTPVerification.DoesNotExist:
                form.add_error(None, "No OTP record found. Please request a new OTP.")
            else:
                if otp_record.is_expired():
                    form.add_error(None, "OTP has expired. Please resend OTP.")
                elif otp_record.otp_code != otp_code:
                    form.add_error('otp_code', "Incorrect OTP. Please try again.")
                else:
                    # Mark OTP as verified and complete registration process.
                    otp_record.verified = True
                    otp_record.save()
                    # (Here you can create the user account or mark the registration as complete)
                    return render(request, 'accounts/success.html', {'email': email})
    else:
        form = OTPForm()
    return render(request, 'accounts/otp_verification.html', {'form': form, 'email': email})

def resend_otp_view(request):
    """
    This view handles AJAX requests to resend the OTP.
    Implements a 40-second cooldown.
    """
    email = request.session.get('email')
    if not email:
        return JsonResponse({'error': 'Session expired. Please restart the registration process.'}, status=400)

    # Check for recent OTP (40-second cooldown)
    cooldown_period = timezone.now() - timedelta(seconds=40)
    recent_otp = OTPVerification.objects.filter(email=email, created_at__gte=cooldown_period).exists()

    if recent_otp:
        return JsonResponse({'error': 'Please wait before requesting a new OTP.'}, status=400)
    
    # Create a new OTP record
    otp_code = generate_otp()
    otp_record = OTPVerification.objects.create(email=email, otp_code=otp_code)

    # Send email
    send_mail(
        subject="Your New OTP Code",
        message=f"Your new OTP code is {otp_code}. It will expire in 5 minutes.",
        from_email=None,
        recipient_list=[email],
    )
    return JsonResponse({'success': 'OTP resent successfully.'})

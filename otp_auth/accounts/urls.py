# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registration_view, name='registration'),
    path('verify/', views.otp_verification_view, name='otp_verification'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
]
# Compare this snippet from otp_auth/accounts/views.py:
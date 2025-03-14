# OTP Email Authentication System

This is a web-based email authentication system built with Django that implements OTP (One-Time Password) verification for user registration. The system is designed with a clear and secure user interface inspired by Gmail and Microsoft authentication flows.

## Features

- **User Registration Flow:** Users can register using their email address.
- **OTP Verification:** A 6-digit OTP is generated and sent to the user's email. The OTP expires in 5 minutes.
- **Resend OTP:** Users can request a new OTP if needed. A 40-second cooldown prevents abuse.
- **Email Sending:** In production, real emails are sent using SMTP (e.g., Gmail SMTP).

## Technologies Used

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Email Service:** SMTP (configured for Gmail in this example)

## Setup and Installation

### Prerequisites

- Python 3.x
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Gaurav5189/OTP-Verification.git
   cd your-repo

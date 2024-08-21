from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
import pyotp
from django.contrib.auth.models import User
from django.conf import settings
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                auth_login(request, user)
                return redirect('index')
            else:
                request.POST = {'email': user.email}
                return send_otp_view(request)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_verified:
                auth_login(request, user)
                return redirect('index')
            otp = pyotp.TOTP(settings.OTP_SECRET_KEY, interval=300)
            otp_code = otp.now()

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            request.session['otp_code'] = otp_code
            request.session['email'] = user.email

            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'signup.html', {'form': form})

OTP_SECRET_KEY = 'base32secret3232'

def send_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = pyotp.TOTP(settings.OTP_SECRET_KEY, interval=300)
        otp_code = otp.now()
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        request.session['otp_code'] = otp_code
        request.session['email'] = email
        return redirect('verify_otp')
    return render(request, 'send_otp.html')

def verify_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        user_input_code = request.POST.get('otp_code')
        otp = pyotp.TOTP(settings.OTP_SECRET_KEY, interval=300)
        if otp.verify(user_input_code):
            try:
                user = get_user_model().objects.get(email=user_email)
                user.is_verified = True
                user.save()
                return redirect('index')
            except get_user_model().DoesNotExist:
                return render(request, 'verify_otp.html', {'error': 'User not found'})
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')
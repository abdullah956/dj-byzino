from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
import pyotp
from django.conf import settings
from categories.models import Category
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

#home
def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

#login
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
    return render(request, 'users/login.html', {'form': form})

#register
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
    
    return render(request, 'users/signup.html', {'form': form})


OTP_SECRET_KEY = 'base32secret3232'
#otp for verification
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
    return render(request, 'users/send_otp.html')

#verify the otp for verification
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
                return render(request, 'users/verify_otp.html', {'error': 'User not found'})
        else:
            return render(request, 'users/verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'users/verify_otp.html')

#password forgot
def forgot_password_view(request):
    return render(request, 'users/forgot_password.html')

#sending otp for pass forgot
def send_password_otp_view(request):
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
        return redirect('verify_password_otp')
#verify otp for pass forgot
def verify_password_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        user_input_code = request.POST.get('otp_code')
        otp = pyotp.TOTP(settings.OTP_SECRET_KEY, interval=300)
        if otp.verify(user_input_code):
            return redirect('reset_password')
        else:
            return render(request, 'users/verify_password_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'users/verify_password_otp.html')

#resetting the pass
def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        try:
            user = get_user_model().objects.get(email=email)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            return redirect('index')
        except get_user_model().DoesNotExist:
            return render(request, 'users/reset_password.html', {'error': 'User not found'})
    return render(request, 'users/reset_password.html')


#logout
def logout_view(request):
    logout(request)
    return redirect('index')
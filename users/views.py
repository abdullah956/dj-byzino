from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as auth_login, update_session_auth_hash, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Sum
from django.core.paginator import Paginator
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from users.models import ContactMessage, Subscriber
from categories.models import Product, Category, Review
from orders.models import Order
import pyotp
from io import BytesIO
from openpyxl import Workbook
import openpyxl


#home
def index(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True).annotate(
        average_rating=Avg('review__stars')
    )
    five_star_reviews = Review.objects.filter(stars=5).select_related('product')[:5]

    return render(request, 'index.html', {
        'categories': categories,
        'featured_products': featured_products,
        'five_star_reviews': five_star_reviews,
    })

#login
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')
            else:
                messages.warning(request, 'Your account is not verified. Please check your email for the verification link.')
                request.POST = {'email': user.email}
                return send_otp_view(request)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
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
                messages.success(request, 'Signup successful! You are now logged in.')
                return redirect('index')
            else:
                request.POST = {'email': user.email}
                return send_otp_view(request)
        else:
            messages.error(request, 'Please correct the errors below.')
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
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['otp_code'] = otp_code
            request.session['email'] = email
            messages.success(request, 'An OTP code has been sent to your email. Please check your inbox.')
            return redirect('verify_otp')
        except Exception as e:
            messages.error(request, 'There was an error sending the OTP. Please try again.')


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
                auth_login(request, user)
                messages.success(request, 'Your account has been verified successfully. You are now logged in.')
                return redirect('index')
            except get_user_model().DoesNotExist:
                messages.error(request, 'User not found. Please check the email and try again.')
                return render(request, 'users/verify_otp.html', {'error': 'User not found'})
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
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
        
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['otp_code'] = otp_code
            request.session['email'] = email
            messages.success(request, 'OTP has been sent to your email address.')
            return redirect('verify_password_otp')
        except Exception as e:
            messages.error(request, 'There was an error sending the OTP. Please try again.')
    
#verify otp for pass forgot

def verify_password_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        user_input_code = request.POST.get('otp_code')
        otp = pyotp.TOTP(settings.OTP_SECRET_KEY, interval=300)
        
        if otp.verify(user_input_code):
            messages.success(request, 'OTP verified successfully. You can now reset your password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
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
            update_session_auth_hash(request, user)
            auth_login(request, user)
            messages.success(request, 'Password has been reset successfully.')
            return redirect('index')
        except get_user_model().DoesNotExist:
            messages.error(request, 'User not found. Please check the email address and try again.')
    
    return render(request, 'users/reset_password.html')


#logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

#profile update
@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('update_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/update_profile.html', {'form': form})

#subs
def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return HttpResponseBadRequest("Email is required.")
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        if not created:
            subscriber.is_subscribed = True
            subscriber.save()
            messages.success(request, "You have been subscribed successfully.")
        return redirect('index')
    return redirect('index')

#contact
def contact_view(request):
    return render(request, 'users/contact.html')

def contact_message_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('review_form_text')
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully.")
        return redirect('index')
    return redirect('index')
    
#search
def product_search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'users/search_result.html', {
        'products': products,
        'query': query,
    })

#dashboard
def stats_view(request):
    total_subscribers = Subscriber.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_earnings = Order.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    order_list = Order.objects.all().order_by('-order_date')
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'total_subscribers': total_subscribers,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_earnings': total_earnings,
        'recent_orders': page_obj,
    }
    return render(request, 'users/stats.html', context)


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    product_data = order.products
    product_ids = [item['product_id'] for item in product_data]
    products = Product.objects.filter(id__in=product_ids)
    products_with_quantities = []
    for item in product_data:
        product_id = item['product_id']
        quantity = item['quantity']
        product = products.filter(id=product_id).first()
        if product:
            products_with_quantities.append({
                'product': product,
                'quantity': quantity
            })
    context = {
        'order': order,
        'products_with_quantities': products_with_quantities,
    }
    return render(request, 'users/order_detail.html', context)



def message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'users/message_list.html', {'page_obj': page_obj})

def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'users/message_detail.html', {'message': message})


User = get_user_model()
def user_list_view(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.GET.get('export') == 'excel':
        email_list = [user.email for user in users]
        wb = Workbook()
        ws = wb.active
        ws.title = 'Users'
        ws.append(['Email'])
        for email in email_list:
            ws.append([email])
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=emails.xlsx'
        stream = BytesIO()
        wb.save(stream)
        response.write(stream.getvalue())
        return response

    return render(request, 'users/user_list.html', {'page_obj': page_obj})

def export_users_to_excel(request):
    users = User.objects.all()
    email_list = [user.email for user in users]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Users'
    ws.append(['Email'])
    for email in email_list:
        ws.append([email])
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    response = HttpResponse(
        stream.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="users_emails.xlsx"'
    return response

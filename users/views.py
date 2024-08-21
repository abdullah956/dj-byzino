from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login

from users.forms import UserLoginForm, UserRegistrationForm

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index') 
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})
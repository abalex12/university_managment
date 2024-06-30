from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Student, Teacher
from academics.models import Enrollment
from django.contrib import messages

user = settings.AUTH_USER_MODEL

@login_required
def index(request):
    return render(request,"userauth/index.html")

def signin(request):
    return render(request,"userauth/sign_in.html")

def signup(request):
    return render(request,"userauth/sign_up.html")

def logout_view(request):
    logout(request)
    return redirect("userauth:sign-in")

def log_in(request):
    if request.user.is_authenticated: 
        return render(request, 'userauth/index.html')
    
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'userauth/sign_in.html')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'The email address is not registered.')
            return render(request, 'userauth/sign_in.html')

        if not user.check_password(password):
            messages.error(request, 'Incorrect password.')
            return render(request, 'userauth/sign_in.html')

        if not user.is_active:
            messages.error(request, 'This account is inactive.')
            return render(request, 'userauth/sign_in.html')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            
            # Redirect to the same function to handle the authenticated user case
            return redirect('userauth:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'userauth/sign_in.html')
    
    return render(request, 'userauth/sign_in.html')
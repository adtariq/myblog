from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserPasswordResetForm, SetPasswordForm
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            # Create the user profile
            messages.success(request,f"successfully loged in!")
            return redirect('accounts:login')
        else:
            msg=""
            username_errors = form.errors.get('username')
            userpass2_errors=form.errors.get('password2')
            if username_errors:
                msg=username_errors[0]
            elif userpass2_errors:
                msg=userpass2_errors[0]
            else:
                msg="Unknown error occure!"
            messages.success(request,f"{msg}")
            
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
from django import forms


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log in the user using the login function
                login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, f"Username or password  is invalid Try again!")
    else:
        # return redirect('accounts:login')  
        form = CustomUserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    # Log the user out
    logout(request)
    # Redirect to a specific page after logout, or use reverse() to redirect to a named URL
    return redirect("post_list")

def get_host(request):
    if request.is_secure:
        host = 'https://{}'.format(request.get_host())
    else:
        host = 'http://{}'.format(request.get_host())
    return host

# def password_reset(request):
#     if request.method == 'POST':
#         form = CustomUserPasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('password_reset_confirm')
#     else:
#         form = CustomUserPasswordResetForm()
#     return render(request, 'registration/password_reset.html', {'form': form})

# password_reset.py
from django.conf import settings

def password_reset(request):
    if request.method == 'POST':
        form = CustomUserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            host = settings.EMAIL_HOST  # Use host from settings
            send_reset_email(request.user.email, host)
            return redirect('password_reset_complete')
    else:
        form = CustomUserPasswordResetForm()
    return render(request, 'registration/password_reset.html', {'form': form})

def password_reset_confirm(request, uid, token):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
    else:
        context = {'user': user, 'form': form}
        return render(request, 'registration/password_reset_confirm.html', context)
    
def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')
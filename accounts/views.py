from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update user profile
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.phone = form.cleaned_data['phone']
            profile.whatsapp_number = form.cleaned_data.get('whatsapp_number') or form.cleaned_data['phone']
            profile.college_name = form.cleaned_data.get('college_name', '')
            profile.course = form.cleaned_data.get('course', '')
            profile.save()

            login(request, user)
            messages.success(request, f"Welcome to CampusNest, {user.first_name or user.username}! Zero-Brokerage account created successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        role_pref = request.GET.get('role', 'STUDENT')
        form = UserRegistrationForm(initial={'role': role_pref})
        
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or 'dashboard'
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user fields
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial)
        
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

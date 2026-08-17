from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm
from .models import StudentProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create standard User instance
            user = User.objects.create_user(
                username=form.cleaned_data['admission_number'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            # Create attached StudentProfile
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'accounts/dashboard.html', {'profile': profile})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    students = StudentProfile.objects.select_related('user').prefetch_related('user__documents').order_by('-created_at')
    return render(request, 'accounts/admin_dashboard.html', {'students': students})
  
@user_passes_test(lambda u: u.is_staff)
def update_status(request, pk, status):
    profile = get_object_or_404(StudentProfile, pk=pk)
    if status in ['VERIFIED', 'REJECTED', 'PENDING']:
        profile.status = status
        profile.save()
    return redirect('admin_dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    # Prefetch related user documents for efficient queries
    students = StudentProfile.objects.select_related('user').prefetch_related('user__documents').order_by('-created_at')
    return render(request, 'accounts/admin_dashboard.html', {'students': students})
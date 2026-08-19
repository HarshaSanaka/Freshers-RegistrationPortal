from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from students.forms import PersonalInfoForm
from students.models import StudentProfile

def _login_destination(user):
    if user.is_staff:
        return 'verification_dashboard'
    return 'dashboard'

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect(_login_destination(request.user))

    if request.method == 'POST':
        from .forms import StudentLoginForm
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            profile = StudentProfile.objects.select_related('user').filter(
                registration_number__iexact=form.cleaned_data['admission_number']
            ).first()
            if profile and profile.date_of_birth == form.cleaned_data['date_of_birth']:
                login(request, profile.user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(_login_destination(profile.user))
            form.add_error(None, 'Admission number or date of birth is incorrect.')
    else:
        from .forms import StudentLoginForm
        form = StudentLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def complete_profile_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    profile = get_object_or_404(StudentProfile, user=request.user)
    if profile.is_profile_complete:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PersonalInfoForm(instance=profile)

    return render(request, 'accounts/complete_profile.html', {'form': form})

@login_required
@never_cache
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

@never_cache
def logout_view(request):
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    # Prefetch related user documents for efficient queries
    students = StudentProfile.objects.select_related('user').prefetch_related('user__documents').order_by('-created_at')
    return render(request, 'accounts/admin_dashboard.html', {'students': students})
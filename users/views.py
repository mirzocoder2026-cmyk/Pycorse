from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import CustomUser

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('admin_panel' if user.is_admin_role else 'dashboard')
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'student'
        user.save()
        login(request, user)
        messages.success(request, 'Хуш омадед!')
        return redirect('dashboard')
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    from courses.models import Enrollment
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    students    = CustomUser.objects.filter(role='student').order_by('-score')
    rank        = list(students.values_list('id', flat=True)).index(request.user.id) + 1 if request.user in students else '-'
    return render(request, 'users/dashboard.html', {
        'enrollments': enrollments, 'rank': rank, 'total': students.count()
    })

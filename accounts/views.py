from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Asosiy sahifa"""
    if request.user.is_authenticated:
        return redirect('admin:index')
    return render(request, 'accounts/home.html', {})

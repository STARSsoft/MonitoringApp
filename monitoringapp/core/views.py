from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm


def register_view(request):
    print("Регистрация: представление вызвано!")  # Текст для проверки
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Остальные представления

def start_page(request):
    return render(request, 'start_page.html')

def price_add(request):
    return render(request, 'price_add.html')

def statistics(request):
    return render(request, 'statistics.html')

def about_us(request):
    return render(request, 'about_us.html')

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

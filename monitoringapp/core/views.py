from django.shortcuts import render

# core/views.py

def start_page(request):
    return render(request, 'start_page.html')  # Путь без 'core/'

def main_page(request):
    return render(request, 'main_page.html')

def price_add(request):
    return render(request, 'price_add.html')

def statistics(request):
    return render(request, 'statistics.html')

def about_us(request):
    return render(request, 'about_us.html')

def test_page(request):
    return render(request, 'test_page.html')



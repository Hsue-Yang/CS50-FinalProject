from django.shortcuts import render
from .models import Website
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .services import concat_products
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json
import logging
logger = logging.getLogger(__name__)

@login_required(login_url='login')
def index(request):
    websites = Website.objects.filter(is_active=True).values('id', 'name', 'url', 'api_endpoint')
    if websites.exists():
        websites = list(websites)
    
    context = {
        'websites': websites,
        'timestamp':timezone.now().timestamp()
    }
    return render(request, 'index.html', context)

@csrf_exempt
def search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword', '').strip()
            site = data.get('site', '')
            page = data.get('page', 1)
            if not keyword:
                return JsonResponse({'errors': 'Please enter a keyword'})
            products = concat_products(keyword, site, page)
            if not products:
                return JsonResponse({'errors': 'No matching products found'})
            return JsonResponse({'products': products})
        except Exception as e:
            logger.error(f"搜尋時發生錯誤: {e}")
            return JsonResponse({'errors': 'An error occurred during the search process'})
        
    return JsonResponse({'errors': 'Invalid request method'})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'errors': 'Invalid username or password'})    
    else:
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form, 'errors':form.errors})
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'register.html', context)
from django.shortcuts import render
from django.core.paginator import Paginator
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
        # 如果資料庫中有網站資料，則使用資料庫中的資料
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
            if not keyword:
                return JsonResponse({'errors': '請輸入關鍵字'})
            products = concat_products(keyword, site)
            if not products:
                return JsonResponse({'errors': '沒有找到相關商品'})
            return JsonResponse({'products': products})
        except Exception as e:
            logger.error(f"搜尋時發生錯誤: {e}")
            return JsonResponse({'errors': '搜尋過程中發生錯誤'})
        
    return JsonResponse({'errors': '無效的請求'})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'errors': '無效的使用者名稱或密碼'})    
    else:
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('login')  # 登出後重定向到首頁

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 註冊成功後重定向到登入頁面
        else:
            return render(request, 'register.html', {'form': form, 'errors':form.errors})
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'register.html', context)
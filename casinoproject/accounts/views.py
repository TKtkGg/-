from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser

# Create your views here.

def landing(request):
    """ランディングページ：サインアップとログインの選択画面"""
    if request.user.is_authenticated:
        return redirect('top')
    return render(request, 'accounts/landing.html')

def signup_view(request):
    """サインアップビュー"""
    if request.user.is_authenticated:
        return redirect('top')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # バリデーション
        if not username or not password:
            messages.error(request, 'ユーザーネームとパスワードを入力してください。')
            return render(request, 'accounts/signup.html')
        
        if password != password_confirm:
            messages.error(request, 'パスワードが一致しません。')
            return render(request, 'accounts/signup.html')
        
        # ユーザーが既に存在するか確認
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'このユーザーネームは既に使用されています。')
            return render(request, 'accounts/signup.html')
        
        # 新規ユーザー作成
        user = CustomUser.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('top')
    
    return render(request, 'accounts/signup.html')

def login_view(request):
    """ログインビュー"""
    if request.user.is_authenticated:
        return redirect('top')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 認証
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            messages.error(request, 'ユーザーネームまたはパスワードが正しくありません。')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    """ログアウトビュー"""
    logout(request)
    return redirect('landing')

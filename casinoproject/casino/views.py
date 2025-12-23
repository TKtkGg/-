import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .trump import TRUMP
from accounts.models import CustomUser
from .models import GameHistory
from .bacarrat import Baccarat
from .blackjack import Blackjack

# Create your views here.
@login_required
def top(request):
    player = request.user
    bj = Blackjack()
    return render(request, 'casino/top.html',{'money': player.money})

class BaccaratGameView(LoginRequiredMixin, Baccarat, View):
    """バカラゲームビュー"""
    def get(self, request):
        return self.start_game(request)
    
    def post(self, request):
        return self.play_game(request)

class BaccaratBetView(LoginRequiredMixin, Baccarat, View):
    """バカラベットビュー"""
    def get(self, request):
        return self.process_bet(request)
    
    def post(self, request):
        return self.save_bet(request)

# 後方互換性のための関数ラッパー
bacarrat = BaccaratGameView.as_view()
bacara_bet = BaccaratBetView.as_view()


class BlackjackGameView(LoginRequiredMixin, Blackjack, View):
    """ブラックジャックゲームビュー"""
    
    def get(self, request):
        return self.start_game(request)
    
    def post(self, request):
        return self.play_game(request)

class BlackjackBetView(LoginRequiredMixin, View):
    """ブラックジャックベットビュー"""
    
    def get(self, request):
        # ブラックジャックベットの処理（GETリクエスト処理）
        player = request.user
        
        # 新しいゲームを開始するため、前回のゲーム結果をクリア
        request.session['game_result_saved'] = False
        
        return render(request, 'casino/blackjack_bet.html', {'money': player.money})
    
    def post(self, request):
        # ブラックジャックベット情報の保存（POSTリクエスト処理）
        bet_amount = int(request.POST.get('bet_amount', 0))
        bet_type = request.POST.get('bet_type', 'blackjack')
        
        # セッションにベット情報を保存し、前回のゲーム結果をクリア
        request.session['bet_amount'] = bet_amount
        request.session['bet_type'] = bet_type
        request.session['game_result_saved'] = False
        
        return redirect('blackjack')

# 後方互換性のための関数ラッパー
blackjack = BlackjackGameView.as_view()
blackjack_bet = BlackjackBetView.as_view()
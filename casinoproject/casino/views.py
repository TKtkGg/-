import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .trump import TRUMP
from accounts.models import CustomUser
from .models import GameHistory
from .bacarrat import Baccarat

# Create your views here.
@login_required
def top(request):
    player = request.user
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


class Blackjack:
    """ブラックジャックゲームのロジッククラス"""
    @staticmethod
    def calculate_score(cards):
        """カードのスコアを計算"""
        score = 0
        ace_count = 0
        
        for card in cards:
            rank = card['rank']
            if rank >= 10:
                score += 10
            elif rank == 1:
                ace_count += 1
                score += 11  # 最初はエースを11としてカウント
            else:
                score += rank
        
        # エースの調整
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        
        return score

    @staticmethod
    def handle_result(player_score, dealer_score, player, bet_amount, bet_type):
        """勝敗判定とDB保存"""
        # 勝敗判定
        if player_score > 21:
            winner = 'dealer'
            player.money -= bet_amount
        elif dealer_score > 21 or player_score > dealer_score:
            winner = 'player'
            player.money += bet_amount
        elif dealer_score > player_score:
            winner = 'dealer'
            player.money -= bet_amount
        else:
            winner = 'draw'
            # 引き分けの場合、ベット金額は変わらない
        
        player.save()

        GameHistory.objects.create(
            user=player,
            winner=winner,
            player_score=player_score,
            dealer_score=dealer_score
        )

        return winner
    
    def start_game(self, request):
        """ブラックジャックゲームの開始（GETリクエスト処理）"""
        player = request.user
        # 初回表示：2枚ずつ配る
        cards = random.sample(TRUMP, 4)
        player_cards = cards[:2]
        dealer_cards = cards[2:]
        used_cards = [card['name'] for card in cards]
        
        player_score = self.calculate_score(player_cards)
        dealer_score = self.calculate_score(dealer_cards)

        origin_money = player.money
        bet_amount = request.session.get('bet_amount', 0)
        bet_type = request.session.get('bet_type')

        # セッションにカード情報を保存
        request.session['player_cards'] = player_cards
        request.session['dealer_cards'] = dealer_cards
        request.session['used_cards'] = used_cards
        
        return render(request, 'casino/blackjack.html', {
            'player_cards': player_cards,
            'dealer_cards': dealer_cards,
            'player_score': player_score,
            'dealer_score': dealer_score,
            'origin_money':origin_money,
            'money': player.money,
        })
    
    def play_game(self, request):
        """ブラックジャックゲームの実行（POSTリクエスト処理）"""
        player = request.user
        action = request.POST.get('value')
        # セッションからカード情報を取得
        player_cards = request.session.get('player_cards')
        dealer_cards = request.session.get('dealer_cards')
        used_cards = request.session.get('used_cards', [])
        remaining_cards = [card for card in TRUMP if card['name'] not in used_cards]
        origin_money = player.money
        bet_amount = request.session.get('bet_amount', 0)
        bet_type = request.session.get('bet_type')

        if action == 'hit':
            pass
        elif action == 'stand':
            pass

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
        pass  # 実装省略
    
    def post(self, request):
        # ブラックジャックベット情報の保存（POSTリクエスト処理）
        pass  # 実装省略

# 後方互換性のための関数ラッパー
blackjack = BlackjackGameView.as_view()
blackjack_bet = BlackjackBetView.as_view()
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .trump import TRUMP
from accounts.models import CustomUser
from .models import GameHistory

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
    def handle_result(player_score, dealer_score, player, bet_amount, bet_type, player_cards):
        """勝敗判定とDB保存"""
        # ブラックジャック判定（最初の2枚で21）
        is_blackjack = len(player_cards) == 2 and player_score == 21
        
        # 勝敗判定
        if player_score > 21:
            winner = 'dealer'
            player.money -= bet_amount
        elif dealer_score > 21 or player_score > dealer_score:
            if is_blackjack:
                winner = 'blackjack'
                # ブラックジャックは1.5倍の配当
                player.money += int(bet_amount * 1.5)
            else:
                winner = 'player'
                player.money += bet_amount
        elif dealer_score > player_score:
            winner = 'dealer'
            player.money -= bet_amount
        else:
            winner = 'draw'
            # 引き分けの場合、ベット金額は変わらない
        
        player.save()

        return winner
    
    def start_game(self, request):
        """ブラックジャックゲームの開始（GETリクエスト処理）"""
        player = request.user
        
        # セッションにゲーム結果が既に保存されているか確認（リロード対策）
        if request.session.get('game_result_saved', False):
            # 既にゲームが終了している場合は、保存されたデータを使用
            player_cards = request.session.get('player_cards')
            dealer_cards = request.session.get('dealer_cards')
            player_score = request.session.get('player_score')
            dealer_score = request.session.get('dealer_score')
            winner = request.session.get('winner')
            origin_money = request.session.get('origin_money')
            game_over = request.session.get('game_over', False)
            
            return render(request, 'casino/blackjack.html', {
                'player_cards': player_cards,
                'dealer_cards': dealer_cards,
                'player_score': player_score,
                'dealer_score': dealer_score,
                'winner': winner,
                'game_over': game_over,
                'origin_money': origin_money,
                'money': player.money,
            })
        
        # 新しいゲームの開始：2枚ずつ配る
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
        request.session['origin_money'] = origin_money
        request.session['game_result_saved'] = False  # まだゲーム終了していない
        
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
        action = request.POST.get('action')
        # セッションからカード情報を取得
        player_cards = request.session.get('player_cards')
        dealer_cards = request.session.get('dealer_cards')
        used_cards = request.session.get('used_cards', [])
        remaining_cards = [card for card in TRUMP if card['name'] not in used_cards]
        origin_money = player.money
        bet_amount = request.session.get('bet_amount', 0)
        bet_type = request.session.get('bet_type')

        if action == 'hit':
            # プレイヤーがヒットを選択
            new_card = random.choice(remaining_cards)
            player_cards.append(new_card)
            used_cards.append(new_card['name'])
            
            player_score = self.calculate_score(player_cards)
            dealer_score = self.calculate_score(dealer_cards)

            # セッションに更新したカード情報を保存
            request.session['player_cards'] = player_cards
            request.session['used_cards'] = used_cards

            if player_score >= 21:
                # プレイヤーがバースト、ブラックジャック
                while dealer_score < 17:
                    new_card = random.choice(remaining_cards)
                    dealer_cards.append(new_card)
                    used_cards.append(new_card['name'])
                    dealer_score = self.calculate_score(dealer_cards)

                winner = self.handle_result(player_score, dealer_score, player, bet_amount, bet_type, player_cards)

                # ゲーム終了時にセッションに結果を保存
                request.session['player_score'] = player_score
                request.session['dealer_score'] = dealer_score
                request.session['winner'] = winner
                request.session['game_over'] = True
                request.session['game_result_saved'] = True

                return render(request, 'casino/blackjack.html', {
                    'player_cards': player_cards,
                    'dealer_cards': dealer_cards,
                    'player_score': player_score,
                    'dealer_score': dealer_score,
                    'winner': winner,
                    'game_over': True,
                    'origin_money':origin_money,
                    'money': player.money,
                })
            else:
                return render(request, 'casino/blackjack.html', {
                    'player_cards': player_cards,
                    'dealer_cards': dealer_cards,
                    'player_score': player_score,
                    'dealer_score': dealer_score,
                    'origin_money':origin_money,
                    'money': player.money,
                })
            
        elif action == 'stand':
            # プレイヤーがスタンドを選択
            player_score = self.calculate_score(player_cards)
            dealer_score = self.calculate_score(dealer_cards)
            
            # ディーラーのターン
            while dealer_score < 17:
                new_card = random.choice(remaining_cards)
                dealer_cards.append(new_card)
                used_cards.append(new_card['name'])
                dealer_score = self.calculate_score(dealer_cards)
            
            winner = self.handle_result(player_score, dealer_score, player, bet_amount, bet_type, player_cards)
            
            # ゲーム終了時にセッションに結果を保存
            request.session['player_score'] = player_score
            request.session['dealer_score'] = dealer_score
            request.session['winner'] = winner
            request.session['game_over'] = True
            request.session['game_result_saved'] = True
            
            return render(request, 'casino/blackjack.html', {
                'player_cards': player_cards,
                'dealer_cards': dealer_cards,
                'player_score': player_score,
                'dealer_score': dealer_score,
                'winner': winner,
                'game_over': True,
                'origin_money':origin_money,
                'money': player.money,
            })
        
        # どのアクションにも該当しない場合（フォールバック）
        return redirect('top')
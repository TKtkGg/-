import random
from django.shortcuts import render, redirect
from .trump import TRUMP

# Create your views here.
def top(request):
    return render(request, 'casino/top.html')

def get_card_value(rank):
    """バカラでのカードの値を取得"""
    if rank >= 10:
        return 0
    return rank

def calculate_score(cards):
    """カードのスコアを計算（下一桁）"""
    total = sum(get_card_value(card['rank']) for card in cards)
    return total % 10

def should_draw_third_card(player_score, banker_score, player_third_value=None):
    """3枚目を引くべきか判定"""
    # 8-9はナチュラル、引かない
    if player_score >= 8 or banker_score >= 8:
        return False, False
    
    # プレイヤーの判定
    player_draws = player_score <= 5
    
    # バンカーの判定
    if not player_draws:
        # プレイヤーが引かない場合
        banker_draws = banker_score <= 5
    else:
        # プレイヤーが3枚目を引いた場合のバンカーのルール
        if banker_score <= 2:
            banker_draws = True
        elif banker_score == 3:
            banker_draws = player_third_value != 8
        elif banker_score == 4:
            banker_draws = player_third_value in [2, 3, 4, 5, 6, 7]
        elif banker_score == 5:
            banker_draws = player_third_value in [4, 5, 6, 7]
        elif banker_score == 6:
            banker_draws = player_third_value in [6, 7]
        else:
            banker_draws = False
    
    return player_draws, banker_draws

def bacarrat(request):
    if request.method == 'POST':
        # 3枚目を引く処理
        action = request.POST.get('action')
        if action == 'draw':
            # セッションからカード情報を取得
            player_cards = request.session.get('player_cards')
            banker_cards = request.session.get('banker_cards')
            used_cards = request.session.get('used_cards', [])
            
            # 3枚目を引くカードを取得
            remaining_cards = [card for card in TRUMP if card['name'] not in used_cards]
            new_cards = random.sample(remaining_cards, 2)
            
            player_draws = request.session.get('player_draws')
            banker_draws = request.session.get('banker_draws')
            
            if player_draws:
                player_cards.append(new_cards[0])
                used_cards.append(new_cards[0]['name'])
            
            if banker_draws:
                banker_cards.append(new_cards[1] if player_draws else new_cards[0])
            
            player_score = calculate_score(player_cards)
            banker_score = calculate_score(banker_cards)
            
            # 勝敗判定
            if player_score > banker_score:
                winner = 'player'
            elif banker_score > player_score:
                winner = 'banker'
            else:
                winner = 'draw'
            
            return render(request, 'casino/bacarrat.html', {
                'player_cards': player_cards,
                'banker_cards': banker_cards,
                'player_score': player_score,
                'banker_score': banker_score,
                'winner': winner,
                'game_over': True,
            })
    
    # 初回表示：2枚ずつ配る
    cards = random.sample(TRUMP, 4)
    player_cards = cards[:2]
    banker_cards = cards[2:]
    
    player_score = calculate_score(player_cards)
    banker_score = calculate_score(banker_cards)
    
    # 3枚目を引くか判定
    player_draws, banker_draws = should_draw_third_card(player_score, banker_score)
    
    # 3枚目を引く場合はセッションに保存
    if player_draws or banker_draws:
        request.session['player_cards'] = player_cards
        request.session['banker_cards'] = banker_cards
        request.session['used_cards'] = [card['name'] for card in cards]
        request.session['player_draws'] = player_draws
        request.session['banker_draws'] = banker_draws
        
        return render(request, 'casino/bacarrat.html', {
            'player_cards': player_cards,
            'banker_cards': banker_cards,
            'player_score': player_score,
            'banker_score': banker_score,
            'need_third_card': True,
        })
    else:
        # 3枚目を引かない場合は即決着
        if player_score > banker_score:
            winner = 'player'
        elif banker_score > player_score:
            winner = 'banker'
        else:
            winner = 'draw'
        
        return render(request, 'casino/bacarrat.html', {
            'player_cards': player_cards,
            'banker_cards': banker_cards,
            'player_score': player_score,
            'banker_score': banker_score,
            'winner': winner,
            'game_over': True,
        })
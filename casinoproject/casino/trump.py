# スート名と画像ファイル名の対応
SUIT_MAP = {
    'spade': 'S',
    'heart': 'H',
    'diamond': 'D',
    'club': 'C'
}

# ランクと画像ファイル名の対応
RANK_MAP = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}

def get_card_image(suit, rank):
    """カードの画像ファイル名を取得"""
    suit_char = SUIT_MAP[suit]
    rank_char = RANK_MAP.get(rank, str(rank))
    # J、Q、Kは絵柄のある_alt版を使用
    if rank in [11, 12, 13]:
        return f"{rank_char}{suit_char}_alt.png"
    return f"{rank_char}{suit_char}.png"

TRUMP = [
    {
        'suit': suit, 
        'rank': rank, 
        'name': f"{suit}{rank}",
        'image': get_card_image(suit, rank)
    } 
    for suit in ['spade', 'heart', 'diamond', 'club'] 
    for rank in range(1, 14)
]
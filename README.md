# CardCasino

## 概要
Django製のカジノゲームWebアプリです。主にブラックジャックとバカラが遊べます。

- ユーザー登録・ログイン機能
- ブラックジャック（スプリッティングペアーズ対応）
- バカラ
- ゲームごとにチップ管理
- 勝敗履歴保存

## セットアップ
1. 必要なパッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```
2. マイグレーション実行
   ```bash
   python manage.py migrate
   ```
3. 開発サーバー起動
   ```bash
   python manage.py runserver
   ```
4. ブラウザで `http://localhost:8000/` にアクセス

## ディレクトリ構成
```
casinoproject/
  ├─ accounts/         # ユーザー管理
  ├─ casino/           # ゲームロジック・画面
  ├─ casinoproject/    # 設定・ルート
  ├─ media/            # 画像等
  ├─ staticfiles/      # 静的ファイル
  ├─ templates/        # HTMLテンプレート
```

## ブラックジャックの特徴
- スプリッティングペアーズ（ペアの分割）に対応
  - J/Q/Kは同じ値として分割可能
  - Aのスプリットは1回だけヒット可能
- 勝敗・チップの推移が画面中央に表示
- ディーラーの手札は決着後に全公開

## 開発・デバッグ
- プレイヤーの初期手札はデバッグ用に10が2枚配られます（blackjack.pyで変更可能）
- テンプレートはDjango標準構文のみ使用

## ライセンス
MIT

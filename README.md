# Private Django Project

趣味で作っているDjangoアプリケーションを公開していく．

### Requirement

このプロジェクトを運用する際は以下のアプリケーション・ライブラリが必要になります．

- Python 2.7
- pip

Python, pip をインストール後，requirements.txt を使いライブラリのインストールを行って下さい．

    pip install -r requirements.txt

### Usage

Django の runserver を使うのが一番手っ取り早い．

    python manage.py runserver

アプリケーションが起動したら以下のURLにアクセスするとアプリケーションリストが表示されます．

    http://localhost:8000/

## 1. SURM

サービス名は Share Useful Resources with Members の頭文字を取ったもの

目的としてはグループメンバー内でのWeb上のページ(リソース)の共有

### Todo

- ページネーション(デザインも内部処理も)をもう少し凝る
- メール送信機能
# Private Django Project

趣味で作っているDjangoアプリケーションを公開していく．

## Requirement

このプロジェクトを運用する際は以下のアプリケーション・ライブラリが必要になります．

- Python 2.7
- pip

Python, pip をインストール後，requirements.txt を使いライブラリのインストールを行って下さい．

    pip install -r requirements.txt

## Usage

### setting.py の書き換え

DB, Email の設定を自分のサーバの設定に書き換える

    DATABASES = {
        'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django-proj',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

    EMAIL_USE_TLS = 
    EMAIL_HOST = 
    EMAIL_HOST_USER = 
    EMAIL_HOST_PASSWORD = 
    EMAIL_PORT = 

### アプリケーションの起動方法

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
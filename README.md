# Private Django Project

趣味で作っているDjangoアプリケーションを公開していく．

設定は共有で特に問題はないはずなのでこのプロジェクトに新しいアプリとして追加していく．

その方がアプリ間の連携などもできそうなので．

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

目的としては開発チーム等のグループ内のメンバー間でのWebページ(リソース)の共有

### Usage

#### 基本機能

- 「グループを作成」ボタンをクリックすることでグループの作成ができる
- グループのページメンバーから「追加」をクリックしてメンバーの追加が行える
- URL を入力してサブミットすることでページのタイトルは自動で取得する
- 投稿されたリソースのリンクをクリックすることで「既読」状態となり誰がそのリソースを見たのか，誰が見ていないのかが分かる
- これとは別にそのリソースが全部で何回見られたのか分かる

#### その他の機能
- 投稿されたリソースに対してコメントを付与することができる
- 投稿されたリソースをお気に入り登録してこれを管理することができる

### Todo

- ページネーション(デザインも内部処理も)をもう少し凝る
- メール送信機能
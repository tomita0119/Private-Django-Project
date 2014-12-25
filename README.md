# SURM #

Share Useful Resources with Members (仮)

### インストールしたpipモジュール ###
requirements.txtに記述．

### テンプレート継承メモ ###

ややこしくなってきたのでテンプレートの継承はメモしておく.

* 一番大本のベースとなるテンプレート : base.html
    - navbarとかfooterとか全テンプレートで使うもの．基本はこれを継承している．
    - 基本はheaderblockとcontentblockを書き換え
    - headerにはパンくずリストとか，contentにはメインのコンテンツを

* グループ内コンテンツのベースとなるテンプレート : group_index.html
    - base.htmlを継承した上でグループ内コンテンツのベースとなるテンプレート
    - グループ内コンテンツではこれを継承する
    - 段組み(3段)を用意して，左側，右側は同じ物を表示させておきたい
    - 基本的にはcenter-contentを書き換え
    - それとそこでの静的ファイルはadditional_static_from_indexに
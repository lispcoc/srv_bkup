#################### 基本設定 ####################
use strict;
use utf8;

package set;

## ●管理パスワード (必ず変更してください)
   our $masterkey = 'zjtrstgn';

## ●登録キー
 # 新規登録をする際に必要な文字列。空欄なら誰でも登録可能。荒らし対策。
   our $registkey = '';

## ●メール関係
 # sendmailのパス
   our $sendmail = '/usr/sbin/sendmail';
 # 管理人メールアドレス
   our $admimail = '';
 # データが登録されたら管理人に通知  0=しない 1=する
   our $notice = 0;

## ●各種ファイル
 # データ記録ファイル1
   our $passfile = 'charpass.cgi';
 # データ記録ファイル2
   our $listfile = 'charlist.cgi';

## ●各種URLの設定
 # CGI本体  # 変更なし
   our $cgi     = main::url(-relative, 1);
 # カレントディレクトリのURL  # 変更なし
   our $current = main::url();
       $current =~ s/[\/][^\/]*$/\//g;
 # キャラクターシートの [ TOP ] のリンク先
   our $backurl = '../';
 # キャラクターリストの [ HOME ] のリンク先
   our $homeurl = '';
 # キャラクタデータ保存ディレクトリ
   our $datadir = 'data/';
 # CSSファイル：通常
   our $css     = 'style.css';
 # 添付画像のディレクトリ
   our $imgdir  = 'tmp/';

## ●バックアップの設定
 # バックアップを 取る=1 取らない=0
   our $backuponoff = 1;
 # キャラクタデータバックアップディレクトリ
   our $backdir     = 'backup/';
 # 1キャラあたりのバックアップの最大数
   our $backupage   = 50;

## ●その他の設定
 # タイトル
   our $title = 'ゆとシート for DX3rd'; # ページ左上のタイトル
   our $titlelink = ''; # ページ左上のタイトルから飛ぶURL(空欄でリンクなし)
   our $subtitle = ''; # ページ右上のサブタイトル
 # リストTOPに表示するメッセージ
   our $message = '';
 # リスト(詳細)の1頁あたりの表示件数
   our $list_max_num = 20;
 # リスト(詳細)の1頁あたりの表示件数の選択肢
   our @list_max_nums = ( 20, 50, 100, 200, 500 );
 # HTMLタグの使用(限定)を 許可=1 不許可=0
   our $tag_on = 1;
 # 名前が未記入でもリストに表示 する=1 しない=0
   our $noname_view = 1;
 # 「一覧に表示しない」ボタンを表示 する=1 しない=0
   our $hide_button = 1;
 # キャラシートのファイル名 登録したID=1 登録した時間=0
   our $filename = 1;
 # キャラシートでのタグの位置 上部(キャラ名の直下)=1 一番下=0
   our $tag_position = 1;
 # データ削除フォームを表示 する=1 しない=0  ※管理パスワードで編集画面にログインすれば、0でも表示されます。
   our $del_on = 0;
 # データを削除するとき、バックアップも削除 する=1 しない=0
   our $del_back = 1;
 # キャラクター画像のファイルサイズ上限(単位byte)
   our $image_maxsize = 1024 * 512;
 # タグリストの閲覧を禁止 する=1 しない=0
   our $taglist_forbid = 0;

## ●リンクを貼った時にワンクッション「おかない」サイト
 #   例：'http://yutorize.2-d.jp' を設定すると http://yutorize.2-d.jp/ft_sim/ もワンクッションおかなくなります
   our @safeurl = (
     'http://yutorize.2-d.jp',
     '',
     '',
   );

## ●キャラクターシートの各種初期値
   our $make_exp   = 130;  # 初期経験点
   our $make_fix   = 0;  # 初期値を固定にする(PLが変更出来ないようにする)=1 しない=0

   our $auto_calc = 0; # 履歴からの経験点の自動計算を固定にする

## ●グループ設定
 # ["ID", "ソート順(空欄で非表示)", "分類名", "分類の説明文"],
 # 選択時はここで書いた順番、キャラ一覧(グループ別)ではソート順で数字が小さい方から表示されます
 # 増減OK
   our @groups = (
    ["PC", "01", "PC", "プレイヤーキャラクター"],
    ["NPC", "99", "NPC", "ノンプレイヤーキャラクター"],

   #  ["A", "01", "キャンペーン「A」", "GM：○○"],
   #  ["B", "02", "キャンペーン「B」", "GM：××"],
   #  ["", "", "", ""],
   );

## ●デザイン設定
   our %design = (
     'body_back' => '#555555', # 奥側の背景色
     'body_imag' => './img/check1.png',        # 背景画像
     'body_repe' => 'repeat',  # 背景画像をリピート する=repeat しない=no-repeat 横のみ=repeat-x 縦のみ=repeat-y
     'body_atta' => 'fixed',   # 背景画像を固定 する=fixed しない=scroll
     'body_posi' => 'center',  # 背景画像配置(background-position)
     'body_text' => '#bbbbbb', # 文字色
     'base_back' =>  0,        # 手前側(中央付近)の背景色 0=黒 1=白
     'head_text' => '#eeeeee', # ヘッダ(タイトル)の文字色
     'head_line' => '#666666', # ヘッダの罫線
     'link_text' => '#99aacc', # リンクの文字色
     'link_hove' => '#cccccc', # リンクにカーソルを載せた時の文字色
     'link_hvtx' => '#000000', # リンクにカーソルを載せた時の文字色
     
     'list_back' => '#b0bbcc', # キャラ一覧(簡易)の背景色
     'list_text' => '#000000', # キャラ一覧(簡易)の文字色
     'list_hove' => '#444b66', # キャラ名にカーソルを載せた時の背景色
     'list_hvtx' => '#ffffff', # キャラ名にカーソルを載せた時の文字色
     
     'table_row1' => '#303030', # キャラ一覧(詳細)の背景色・奇数段
     'table_row2' => '#292929', # キャラ一覧(詳細)の背景色・偶数段
     'table_hove' => '#113030', # キャラ一覧(詳細)の背景色・カーソルを載せた段
     'table_text' => '#dddddd', # キャラ一覧(詳細)の文字色
     'table_head' => '#222733', # キャラ一覧(詳細)のヘッダの背景色
     'table_hdtx' => '#dddddd', # キャラ一覧(詳細)のヘッダの文字色
     'table_line' => '#555555', # キャラ一覧(詳細)の罫線の色
     
     'box_line' => '#000000', # ボックスの枠の色
     'box_head' => '#222222', # ボックスのヘッダの背景色
     'box_text' => '#dddddd', # ボックスのヘッダの文字色
   );


##################################################
## 一部の人向け。普通は変更しません。

 # セッションログ(ゆとチャ)自動リンク
   our $loglink = 0; # 機能のON=1/OFF=0
   our @logurl = (
   # ['', 0, 'http://yutorize.2-d.jp/ytchat2/sample_sw2/log/'],
   # ['', 0, ''],
   );
   # ['ログファイルの末尾文字', 年毎にフォルダ分けしている場合は1, 'ログフォルダのURL'],

 # PLリスト連携
   our $pllist = ''; #PLリストのURL
   our $entry_restrict = 0; #新規登録をPLリストからのみに制限


1;

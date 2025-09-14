## 初期言語設定
$config{'lang'} = 'jp';
#$config{'lang'} = 'en';

## データディレクトリ
$config{'dir.data'} = './data/';

## 一時ファイル保存用ディレクトリ
$config{'dir.tmp'} = $config{'dir.data'} . 'tmp/';

## ピクチャ
$config{'dir.picture'} = $config{'dir.data'} . 'picture/';

## 許容エラー回数
$config{'error.limit'} = 5;

## ブロック時間（秒数）
$config{'error.time'} = 86400;

## ユーザーリストファイル
$config{'file.user'} = "$config{'dir.data'}user.cgi";

## エラーログファイル
$config{'file.error'} = "$config{'dir.data'}error.cgi";

## エラーログディレクトリ
$config{'dir.errors'} = "$config{'dir.data'}errors/";

## タスクディレクトリ
$config{'dir.task'} = "$config{'dir.data'}task/";

## スレッドを保存するディレクトリ
$config{'dir.thread'} = "$config{'dir.data'}thread/";

## スレッドリストファイル
$config{'file.thread'} = "$config{'dir.data'}thread.cgi";

## セッション保存ディレクトリ
$config{'dir.session'} = "$config{'dir.data'}session/";

## キーファイル
$config{'file.key'} = "$config{'dir.data'}key.cgi";

## ics保存ディレクトリ
#$config{'dir.ics'} = "$config{'dir.data'}";
$config{'dir.ics'} = "../../../../Dropbox/";

## ホスト情報を取得しない（レスポンスがちょっと速くなります）
$config{'host.disabled'} = 1;

## 難読化桁数
$config{'keycode.digit'} = 20;

## Cookie prefix
$config{'prefix'} = 'unbbs';

## Time start
$config{'day.start'} = '09:00:00';

## Time start
$config{'day.end'} = '17:00:00';


## Sendmailのパス
$config{'sendmail'} = '/usr/sbin/sendmail';
#$config{'sendmail'} = 'C:\sendmail\sendmail.exe';

## SMTP Server
#$config{'smtp.server'} = 'smtp.domain.com';

## SMTP User
#$config{'smtp.user'} = 'smtp@domain.com';

## SMTP Password
#$config{'smtp.passwd'} = '**********';

## SMTP Port
#$config{'smtp.port'} = '587';

## SMTP TLS
#$config{'smtp.tls'} = 1;

## 通知メールの宛先メールアドレス
$config{'notice.to'} = 'support@synck.com';

## 通知メールの差出人メールアドレス
$config{'notice.from'} = 'no-reply@synck.com';

## 通知メールの差出人名
$config{'notice.fromname'} = 'SYNCK GRAPHICA';

## 通知メールに添付ファイル名を記載しない
$config{'notice.attached.filename.none'} = 1;

## 通知メールの署名
$config{'notice.signature'} = <<'__EMAIL__';
--
SYNCKG RAPHICA
customer@synck.com
https://www.synck.com
__EMAIL__

## 文字列最適化 1:on / 0:off
$config{'text.optimization'} = 1;

## ファイルアップロード許可拡張子
$config{'accept.filetype'} = 'jpg,jpeg,gif,png,doc,docx,xls,xlsx,ppt,pptx,zip,lzh,pdf,txt,ai,eps,psd,mp4,m4v,mov';

## ファイルアップロード許可サイズ / ex.200MB
$config{'accept.filesize'} = 1024 * 1024 * 200;

## 画像自動リサイズ（要PHP GD） 1:on / 0:off
$config{'image.resize'} = 1;

## 画像サムネイルの横幅
$config{'image.resize.width'} = 320;

## 並び順を逆順にする
$config{'reverse'} = 0;

## メールフォームプロ連携
$config{'connect'} = 0;

1;
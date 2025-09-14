################### リマインダ ###################
#use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";

my $in_mail = param('mail');
open (my $FH, "<", $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
my $i = 0; my $text;
while (<$FH>){
	my($id, $pass, $file, $name, $mail) = (split /<>/)[0..3,4];
	if($mail eq param('mail')){ $text .= "$name\nID:${id}\n${set::current}${set::datadir}${file}.html\n\n"; }
}
close ($FH);

if (!$text){ &error('入力エラー','メールアドレスが間違っています。'); }

my $text = 'あなた('.$in_mail.')が登録しているキャラクター一覧'."\n\n".$text;
&sendmail($in_mail, $set::title." : Reminder", $text);

require $set::lib_template;
print "Content-type: text/html\n\n";
print &template::_header('送信完了');
print <<"HTML";
<div class="chara" style="width:500px;">
	<div class="box">
		<h2>送信完了</h2>
		<div class="text">
			<br>
			【$in_mail】で登録されたキャラクターの一覧を送信しました。<br>
			<br>
			<a href="$main::backurl">[戻る]</a><br>
			<br>
		</div>
	</div>
</div>
HTML
print &template::_footer();

1;
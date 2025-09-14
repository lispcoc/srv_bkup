################### リマインダ ###################
#use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";

my $in_id = param('id');
my $in_mail;
my $text;
my $time = time;

open (my $FH, '<', $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
my @list = <$FH>;
close($FH);

foreach(@list){
	my($id, $pass, $file, $name, $mail, $pl) = (split /<>/, $_)[0..5];
	if($id eq $in_id){
		$in_mail = $mail;
		my $s;
		my @salt = ('0'..'9','A'..'Z','a'..'z');
		1 while (length($s .= $salt[rand(@salt)]) < 24);
		$_ = "$id<>$pass<>$file<>$name<>$mail<>$pl<>$s-$time<>\n";
		$text = "パスワードを再設定します。\n下記のURLにアクセスしてください。\n\n${set::current}${set::cgi}?mode=form&m=preset&id=$id&code=${s}-${time}\n\nパスワードを再設定したくない場合、このメッセージは無視してください。";
	}
}

if (!$text){ &error('入力エラー','IDが間違っています。'); }

open (my $FH, '+<', $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
flock($FH, 2);
seek($FH, 0, 0);
foreach(@list) { print $FH $_; }
truncate($FH, tell($FH));
close($FH);

&sendmail($in_mail, $set::title." : PassReset", $text);

require $set::lib_template;
print "Content-type: text/html\n\n";
print &template::_header('送信完了');
print <<"HTML";
<div class="chara" style="width:500px;">
	<div class="box">
		<h2>パスワード再設定用URLをメールで送信しました。</h2>
		<div class="text">
			<br>
			数分以内にメールが届かない場合は、スパムや迷惑メールフィルターを確認してください。<br>
			もしくは、メールを<a href="${set::cgi}?mode=form&m=forget">もう一度送信してください</a>。<br>
			<br>
			<a href="$set::current$set::cgi">[戻る]</a><br>
			<br>
		</div>
	</div>
</div>
HTML
print &template::_footer();

1;
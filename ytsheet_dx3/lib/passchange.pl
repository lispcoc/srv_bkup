#################### パス変更 ####################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";

if (param('code') eq ''){
	if (param('id') eq '' || param('oldpass') eq '' || param('newpass') eq '' || param('confirm') eq '') { &error('記入エラー','未入力項目があります。'); }
} else {
	my(undef, $time) = (split /-/, param('code'))[0..1];
	if(time - $time > 60*60){ &error('タイムアウト','URLの有効期限が過ぎています'); }
}
if (param('newpass') ne param('confirm')) { &error('記入エラー','再入力されたパスワードが新しいパスワードと一致していません。'); }
if (param('newpass') =~ /[^0-9A-Za-z\.\-\/]/){ &error('記入エラー','パスワードに使える文字は、半角の英数字とピリオド、ハイフン、スラッシュだけです。'); }

my $flag = 1;
open (my $FH, "<", $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
my @list = <$FH>;
close($FH);

if (param('code') eq ''){
	foreach(@list){
		my($id, $pass, $file, $name, $mail, $pl) = split /<>/;
		if(param('id') eq $id){
			if(&c_crypt(param('oldpass'),$pass || $_[1] eq $set::masterkey)){
				$_ = "$id<>".&main::e_crypt(param('newpass'))."<>$file<>$name<>$mail<>$pl<>\n";
				$flag = 0;
				last;
			}
		}
	}
	if($flag) { &error('記入エラー','ユーザーIDかパスワードが間違っています。'); }
} else {
	foreach(@list){
		my($id, $pass, $file, $name, $mail, $pl, $code) = (split /<>/, $_)[0..9];
		if(param('id') eq $id && param('code') eq $code){
			$_ = "$id<>".&main::e_crypt(param('newpass'))."<>$file<>$name<>$mail<>$pl<>\n";
			$flag = 0;
			last;
		}
	}
	if($flag) { &error('記入エラー','ユーザーIDが間違っています。またはURLの有効期限が過ぎています。'); }
}

open (my $FH, "+<", $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
flock($FH, 2);
seek($FH, 0, 0);
foreach(@list) { print $FH $_; }
truncate($FH, tell($FH));
close($FH);

require $set::lib_template;
print "Content-type: text/html\n\n";
print &template::_header('パスワード変更');
print <<"HTML";
<div class="chara" style="width:500px;">
	<div class="box">
		<h2>パスワード変更</h2>
		<div class="text">
			<br>
			パスワードの変更が完了しました。<br>
			<br>
			<a href="$set::current$set::cgi">[戻る]</a><br>
			<br>
		</div>
	</div>
</div>
HTML
print &template::_footer();

1;
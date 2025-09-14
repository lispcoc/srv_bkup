################### データ削除 ###################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use Fcntl;

my (undef, undef, $file, undef, undef, undef) = getfile(param('id'), param('pass'));
if(!$file){ &error('入力エラー','IDかパスワードが間違っています。'); }

require $set::lib_template;
print "Content-type: text/html\n\n";
print &template::_header('パスワード変更');
print <<"HTML";
<div class="chara" style="width:500px;">
	<div class="box">
		<h2>データ削除</h2>
		<div class="text">
			<br>
HTML

open (my $FH, "+<", $set::listfile) or error('システムエラー','リストファイルのオープンに失敗しました。');
my @liss = sort { (split(/<>/,$a))[5] cmp (split(/<>/,$b))[5] || (split(/<>/,$a))[0] cmp (split(/<>/,$b))[0] } <$FH>;
flock($FH, 2);
seek($FH, 0, 0);
my $lisshit;
foreach (@liss){
	my($num, undef) = split /<>/;
	if ($file eq $num){
		print '一覧データから削除しました。<br>';
	}else{
		print $FH $_;
	}
}
truncate($FH, tell($FH));
close($FH);

if (unlink "${set::datadir}${file}.cgi") { print '個別データを削除しました。<br>'; }
if (unlink "${set::datadir}${file}.html"){ print '個別ページを削除しました。<br>'; }

open (my $FH, '+<', $set::passfile) or error('システムエラー','パスワードファイルのオープンに失敗しました。');
my @list = sort { (split(/<>/,$a))[2] cmp (split(/<>/,$b))[2] || (split(/<>/,$a))[5] cmp (split(/<>/,$b))[5] } <$FH>;
flock($FH, 2);
seek($FH, 0, 0);
foreach (@list){
	my($id, $pass, $file, $name, $mail, $pl) = split /<>/;
	if (param('id') eq $id){
		print 'IDを削除しました。<br>';
	} else {
		print $FH $_;
	}
}
truncate($FH, tell($FH));
close($FH);

if($set::del_back){
	my $dir = "${set::backdir}${file}/";
	opendir (my $DIR, $dir);
	my @files = grep { !m/^(\.|\.\.)$/g } readdir $DIR;
	close ($DIR);
	my $flag = @files;
	if ($flag) {
		foreach (@files) {
			unlink "$dir$_";
		}
	}
	if(rmdir $dir){ print 'バックアップを削除しました。<br>'; } else { print 'バックアップフォルダ'.$dir.'の削除に失敗しました。<br>'; }
}

print <<"HTML";
			<br>
			<a href="$set::current$set::cgi">[戻る]</a><br>
			<br>
		</div>
	</div>
</div>
HTML
print &template::_footer();
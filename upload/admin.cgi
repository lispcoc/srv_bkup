#!/usr/bin/perl

#┌─────────────────────────────────
#│ UP-LOADER : admin.cgi - 2014/09/14
#│ copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib "./lib";
use CGI::Minimal;

# 設定ファイル認識
require "./init.cgi";
my %cf = set_init();

# データ受理
CGI::Minimal::max_read_size($cf{maxdata});
my $cgi = CGI::Minimal->new;
error('容量オーバー') if ($cgi->truncated);
my %in = parse_form($cgi);

# 認証
check_passwd();

# 管理モード
if ($in{mode_data}) { mode_data(); }
if ($in{mode_dlog}) { mode_dlog(); }
mode_data();

#-----------------------------------------------------------
#  データ画面画面
#-----------------------------------------------------------
sub mode_data {
	# 削除処理
	if ($in{del} && $in{no}) {

		# 削除情報
		my %del;
		for ( $cgi->param('no') ) { $del{$_}++; }

		# 削除情報をマッチング
		my @log;
		open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);

			if (defined($del{$no})) {
				unlink("$cf{upldir}/$rand/$fnam.$ex");
				rmdir("$cf{upldir}/$rand");
				next;
			}
			push(@log,$_);
		}
		seek(DAT, 0, 0);
		print DAT @log;
		truncate(DAT, tell(DAT));
		close(DAT);

		# カウントファイル削除
		my @log;
		open(DAT,"+< $cf{cntfile}") or error("open err: $cf{cntfile}");
		eval "flock(DAT, 2);";
		while(<DAT>) {
			my ($no,undef) = split(/:/);
			next if (defined($del{$no}));
			push(@log,$_);
		}
		# 更新
		seek(DAT, 0, 0);
		print DAT @log;
		truncate(DAT, tell(DAT));
		close(DAT);

	# ファイル名変更
	} elsif ($in{rename}) {
		if (!$in{no}) { error('変更するファイル名にチェックを入れてください'); }

		# ファイル名変更
		file_rename();
	}

	# 画面表示
	header("データ画面","js");
	menu_btn();
	print <<"EOM";
<div class="body">
<p class="ttl">■ データ管理</p>
<ul>
<li>チェックボタンをチェックして実行ボタンを押します。
<li>ファイルへの直接リンクを避けるため、「ファイル名の変更」を行うことができます。
</ul>
<form action="$cf{admin_cgi}" method="post" name="allchk">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="mode_data" value="1">
<input type="submit" name="del" value="削除" class="btn" onclick="return confirm('削除しますか？');">
&nbsp;
<input type="submit" name="rename" value="ファイル名変更" class="btn">
<table class="list">
<tr>
	<th><input type="button" onclick="allcheck();" value="全選択"></th>
	<th>アップ日時</th>
	<th>ファイル名</th>
	<th>サイズ</th>
</tr>
EOM

	open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
	while (<IN>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);

		print qq|<td class="ta-c"><input type="checkbox" name="no" value="$no"></td>|;
		print qq|<td>$date</td>|;
		print qq|<td><a href="$cf{uplurl}/$rand/$fnam.$ex" target="_blank">$fnam.$ex</a></td>|;
		print qq|<td class="ta-r">$size</td></tr>\n|;
	}
	close(IN);

	print <<EOM;
</table>
</form>
</div>
EOM
	footer();
}

#-----------------------------------------------------------
#  DLログ画面
#-----------------------------------------------------------
sub mode_dlog {
	# 画面表示
	header("DLログ閲覧");
	menu_btn();
	print <<"EOM";
<div class="body">
<p class="ttl">■ DLログ閲覧</p>
<ol class="log">
EOM

	my %job = (dl => 'DL成功', err => '認証ミス');
	open(IN,"$cf{dlfile}") or error("open err: $cf{dlfile}");
	while (<IN>) {
		my ($job,$num,$date,$host) = split(/<>/);

		print qq|<li>[$job{$job}] <b>$num</b> - $date &nbsp; &lt;<span>$host</span>&gt;</li>\n|;
	}
	close(IN);

	print <<EOM;
</ol>
</div>
EOM
	footer();
}

#-----------------------------------------------------------
#  ファイル名変更
#-----------------------------------------------------------
sub file_rename {
	# 対象ファイル
	my %ren;
	for ( $cgi->param('no') ) { $ren{$_}++; }

	# データ更新
	my ($i,@log);
	open(DAT,"+< $cf{logfile}") or error("open err: $cf{logfile}");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($no,$date,$mime,$ex,$rand,$com,$del,$lock,$size,$host,$fnam) = split(/<>/);

		if (defined($ren{$no})) {
			# 乱数作成
			my $new = make_rand();

			# リネーム
			rename("$cf{upldir}/$rand/$fnam.$ex","$cf{upldir}/$new/$fnam.$ex");

			# フォーマット
			$i++;
			$_ = "$no<>$date<>$mime<>$ex<>$new<>$com<>$del<>$lock<>$size<>$host<>$fnam<>\n";
		}
		push(@log,$_);
	}
	seek(DAT, 0, 0);
	print DAT @log;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 完了
	message("$i個のファイル名を変更しました");
}

#-----------------------------------------------------------
#  HTMLヘッダー
#-----------------------------------------------------------
sub header {
	my ($ttl,$js) = @_;

	print <<EOM;
Content-type: text/html; charset=utf-8

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th { font-size:80%; font-family:Verdana,"MS PGothic","Osaka",Arial,sans-serif; }
p.ttl { font-weight:bold; color:#004080; border-bottom:1px solid #004080; padding:2px; width:100%; }
p.err { color:#dd0000; }
p.msg { color:#006400; }
table.menu-btn { border-collapse:collapse; width:150px; }
table.menu-btn th { border:1px solid #383872; padding:4px; height:38px; background:#cdcde7; }
table.menu-btn input { width:130px; }
table.list { border-collapse:collapse; margin:1em 0; }
table.list th,table.list td { border:1px solid #5e2f00; padding:4px; }
table.list th { background:#ffe4ca; }
div.menu { float:left; width:170px; padding:1.2em; }
div.body { float:left; width:600px; padding:1.2em; }
div.foot { width:100%; clear:both; }
input.btn { width:100px; }
ol.log li { line-height:150%; }
ol.log li span { color:green; }
table.login { margin:3em auto; width:400px; }
.ta-c { text-align:center; }
.ta-r { text-align:right; }
-->
</style>
EOM

	js_boxchk() if ($js eq 'js') ;

	print <<EOM;
<title>$ttl</title>
</head>
<body>
EOM
}

#-----------------------------------------------------------
#  javascriptチェック
#-----------------------------------------------------------
sub js_boxchk {
	print <<'EOM';
<script type="text/javascript">
<!--
function allcheck() {
	var check = document.getElementsByName('no');

    var cnt = check.length;
	for ( var i = 0; i < cnt; i++ ) {
		if (check.item(i).checked) {
			check.item(i).checked = false;
		} else {
			check.item(i).checked = true;
		}
	}
}
// -->
</script>
EOM
}

#-----------------------------------------------------------
#  パスワード認証
#-----------------------------------------------------------
sub check_passwd {
	# パスワードが未入力の場合は入力フォーム画面
	if ($in{pass} eq "") {
		enter_form();

	# パスワード認証
	} elsif ($in{pass} ne $cf{password}) {
		error("認証できません");
	}
}

#-----------------------------------------------------------
#  入室画面
#-----------------------------------------------------------
sub enter_form {
	header("入室画面");
	print <<EOM;
<div class="ta-c">
<form action="$cf{admin_cgi}" method="post">
<table class="login">
<tr>
	<td height="40" class="ta-c">
		<fieldset><legend>管理パスワード入力</legend><br>
		<input type="password" name="pass" size="26">
		<input type="submit" value=" 認証 "><br><br>
		</fieldset>
	</td>
</tr>
</table>
</form>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  エラー
#-----------------------------------------------------------
sub error {
	my $msg = shift;

	header("ERROR!");
	print <<EOM;
<div class="ta-c">
<hr width="350">
<h3>ERROR!</h3>
<p class="err">$msg</p>
<hr width="350">
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  完了メッセージ
#-----------------------------------------------------------
sub message {
	my $msg = shift;

	header("完了");
	print <<EOM;
<div class="ta-c" style="margin-top:3em;">
<hr width="350">
<p class="msg">$msg</p>
<hr width="350">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="管理画面に戻る">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  メニューボタン
#-----------------------------------------------------------
sub menu_btn {
	my %menu = (
		mode_data => 'データ管理',
		mode_dlog => 'DLログ閲覧',
	);

	print <<EOM;
<div class="menu">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table class="menu-btn">
EOM

	foreach (qw(mode_data mode_dlog)) {
		if ($in{$_}) {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}" disabled></th></tr>\n|;
		} else {
			print qq|<tr><th><input type="submit" name="$_" value="$menu{$_}"></th></tr>\n|;
		}
	}

	print <<EOM;
<tr>
	<th><input type="button" value="一般画面に戻る" onclick="window.open('$cf{upload_cgi}','_top')"></th>
</tr><tr>
	<th><input type="button" value="ログオフ" onclick="window.open('$cf{admin_cgi}','_top')"></th>
</tr>
</table>
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  フッター
#-----------------------------------------------------------
sub footer {
	print <<EOM;
<div class="foot">
</div>
</body>
</html>
EOM
	exit;
}


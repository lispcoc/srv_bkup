#################### フォーム ####################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";

my $mode = param('m');

my $title_sub;
if   ($mode eq 'login'){ $title_sub = 'ログインフォーム'; }
elsif($mode eq 'remind'){ $title_sub = 'IDを忘れた'; }
elsif($mode eq 'forget'){ $title_sub = 'パスワードを忘れた'; }
elsif($mode eq 'preset'){ $title_sub = 'パスワード再設定'; }
elsif($mode eq 'change'){ $title_sub = 'パスワード変更'; }
elsif($mode eq 'delete'){ $title_sub = 'データ削除'; }

if (param('code')){
	my(undef, $time) = (split /-/, param('code'))[0..1];
	if(time - $time > 60*60){ &error('タイムアウト','URLの有効期限が過ぎています'); }
}

my $style = <<"HTML";
	<style TYPE="text/css">
		input,select,textarea {
			padding:2px;
			font-size:13px;
		}
		table {
			margin:1em auto;
		}
		table,th,td{
			font-size:12px;
			line-height:13px;
		}
	</style>
HTML

require $set::lib_template;

print "Content-type: text/html\n\n";
print &template::_header($title_sub, $style);
### ログイン ###
if($mode eq 'login'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
		<h2>ログインフォーム</h2>
		<div class="text">
		<form name="reminder" method="post" action="$set::cgi">
		<input type="hidden" name="mode" value="edit">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
				<td>ID</td><td>：<input type="text" name="id" style="width:100px;"></td>
			</tr>
			<tr>
				<td>pass</td><td>：<input type="password" name="pass" style="width:100px;"></td>
			</tr>
		</table>
		<div style="text-align:right;"><input type="submit" value="編 集" style="width:50px;"></div>
		</form>
		<a href="${set::cgi}?mode=form&m=change">パスワード変更</a> ／
		<a href="${set::cgi}?mode=form&m=remind">IDを忘れた</a> ／
		<a href="${set::cgi}?mode=form&m=forget">パスワード忘れた</a><br>
		<br>
		<a href="$set::current$set::cgi">[戻る]</a><br>
		</div>
	</div>
</div>
HTML
}
### リマインダ ###
elsif($mode eq 'remind'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
		<h2>IDを忘れた</h2>
		<div class="text">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
				<td>登録時に記入したメールアドレスを入力してください。<br>そのメールアドレスで登録されたIDとURLのリストを送ります。</td>
			</tr>
			<tr>
				<td>
					<br>
					<form name="reminder" method="post" action="$set::cgi">
						<input type="hidden" name="mode" value="remind">
						E-Mail：<input type="text" name="mail" size="40"><br>
						<br>
						<div style="text-align:right;"><input type="submit" value="送 信" style="width:50px;"></div>
					</form>
				</td>
			</tr>
		</table>
		<a href="$set::current$set::cgi">[戻る]</a><br>
		</div>
	</div>
</div>
HTML
}
### パス忘れ ###
elsif($mode eq 'forget'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
		<h2>パスワードを忘れた</h2>
		<div class="text">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
				<td>パスワードを忘れたIDを入力してください。</td>
			</tr>
			<tr>
				<td>
					<br>
					<form name="reminder" method="post" action="$set::cgi">
						<input type="hidden" name="mode" value="forget">
						ID：<input type="text" name="id" size="40"><br>
						<br>
						<div style="text-align:right;"><input type="submit" value="送 信" style="width:50px;"></div>
					</form>
				</td>
			</tr>
		</table>
		<a href="$set::current$set::cgi">[戻る]</a><br>
		</div>
	</div>
</div>
HTML
}
### パス再設定 ###
elsif($mode eq 'preset'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
	<h2>パスワード再設定</h2>
		<div class="text">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
			  <td>ユーザーID、パスワードは大文字、小文字を区別します。</td>
			</tr>
		</table>
		<form method="post" action="$set::cgi">
			<input type="hidden" name="mode" value="change">
			<input type="hidden" name="id" value="@{[param('id')]}">
			<input type="hidden" name="code" value="@{[param('code')]}">
			<table border="0" cellspacing="1" cellpadding="1">
				<tr> 
					<td align="right">新しいパスワード</td>
					<td>：<input size="20" type="password" name="newpass">（半角英数）</td>
				</tr>
				<tr> 
					<td align="right">新しいパスワード<br>を再入力</td>
					<td>：<input size="20" type="password" name="confirm">（半角英数）</td>
				</tr>
			</table>
			<div style="text-align:right;"><input type="submit" value="送 信" style="width:50px;"></div>
			<a href="$set::current$set::cgi">[戻る]</a><br>
		</form>
		</div>
	</div>
</div>
HTML
}
### パス変更 ###
elsif($mode eq 'change'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
	<h2>パスワード変更</h2>
		<div class="text">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
			  <td>ユーザーID、パスワードは大文字、小文字を区別します。</td>
			</tr>
		</table>
		<form method="post" action="$set::cgi">
			<input type="hidden" name="mode" value="change">
			<table border="0" cellspacing="1" cellpadding="1">
				<tr> 
					<td align="right">ユーザーID</td>
					<td>：<input size="20" type="text" name="id">（半角英数）</td>
				</tr>
				<tr> 
					<td align="right">現在のパスワード</td>
					<td>：<input size="20" type="password" name="oldpass">（半角英数）</td>
				</tr>
				<tr> 
					<td align="right">新しいパスワード</td>
					<td>：<input size="20" type="password" name="newpass">（半角英数）</td>
				</tr>
				<tr> 
					<td align="right">新しいパスワード<br>を再入力</td>
					<td>：<input size="20" type="password" name="confirm">（半角英数）</td>
				</tr>
			</table>
			<div style="text-align:right;"><input type="submit" value="送 信" style="width:50px;"></div>
			<a href="$set::current$set::cgi">[戻る]</a><br>
		</form>
		</div>
	</div>
</div>
HTML
}
### データ削除 ###
elsif($mode eq 'delete'){
	print <<"HTML";
<div class="chara" style="width:400px;">
	<div class="box">
	<h2>データ削除</h2>
		<div class="text">
		<table border="0" cellspacing="1" cellpadding="1">
			<tr>
			  <td>本当に削除しますか？</td>
			</tr>
		</table>
		<form method="post" action="$set::cgi">
			<input type="hidden" name="mode" value="delete">
			<input type="hidden" name="id" value="@{[param('id')]}">
			<input type="hidden" name="pass" value="@{[param('pass')]}">
			<table border="0" cellspacing="1" cellpadding="1">
				<tr>
					<td><input type="submit" value="削除" style="width:50px;"></td>
				</tr>
			</table>
			<a href="$set::current$set::cgi">[戻る]</a><br>
		</form>
		</div>
	</div>
</div>
HTML
}
print &template::_footer;

1;
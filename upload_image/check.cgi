#!/usr/bin/perl

#┌─────────────────────────────────
#│ UP-LOADER : check.cgi - 2017/03/08
#│ copyright (c) kentweb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 外部ファイル取込み
require './init.cgi';
my %cf = set_init();

print <<EOM;
Content-type: text/html; charset=utf-8

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
<li>Perlバージョン : $]
EOM

# ログファイル
my %log = (
	logfile => 'ログファイル',
	cntfile => 'カウントファイル',
	dlfile  => 'DLログ',
	);
foreach ( keys %log ) {
	if (-f $cf{$_}) {
		print "<li>$log{$_}パス : OK\n";
		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}パーミッション : OK\n";
		} else {
			print "<li>$log{$_}パーミッション : NG\n";
		}
	} else {
		print "<li>$log{$_}パス : NG\n";
	}
}

# 画像ディレクトリ
if (-d $cf{upldir}) {
	print "<li>アップロードディレクトリパス : OK\n";
	if (-r $cf{upldir} && -w $cf{upldir} && -x $cf{upldir}) {
		print "<li>アップロードディレクトリパーミッション : OK\n";
	} else {
		print "<li>アップロードディレクトリパーミッション : NG\n";
	}
} else {
	print "<li>アップロードディレクトリパス : NG\n";
}

# テンプレート
foreach (qw(upload error message popup image)) {
	if (-f "$cf{tmpldir}/$_.html") {
		print "<li>テンプレート [ $_.html ] : OK\n";
	} else {
		print "<li>テンプレート [ $_.html ] : NG\n";
	}
}

print <<EOM;
</ul>
</body>
</html>
EOM
exit;


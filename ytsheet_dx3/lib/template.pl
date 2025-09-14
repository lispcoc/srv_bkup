################## テンプレート ##################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";

package template;

sub apart {
	(my $base = $_[0]) =~ s/\#//;
	my($re, $gr, $bl) = $base =~ /.{2}/g;
	return (hex($re), hex($gr), hex($bl));
}

sub _header {
	my ($sub, $style) = @_;
	my $title = $set::title;
	my $back = ($set::design{'base_back'} ? 238 : 0);
	my $list_border;
	my $list_dim_border;
	my $list_hover_border;
	if(1) {
		my($re, $gr, $bl) = apart($set::design{'list_back'});
		my $rel = $re + 51; if($rel > 255){ $rel = 255; }
		my $grl = $gr + 51; if($grl > 255){ $grl = 255; }
		my $bll = $bl + 51; if($bll > 255){ $bll = 255; }
		my $red = $re - 51; if($red < 0)  { $red = 0; }
		my $grd = $gr - 51; if($grd < 0)  { $grd = 0; }
		my $bld = $bl - 51; if($bld < 0)  { $bld = 0; }
		my $light = sprintf("#%02x%02x%02x",$rel,$grl,$bll);
		my $dark  = sprintf("#%02x%02x%02x",$red,$grd,$bld);
		$list_border = "$light $dark $dark $light";
	}
	if(1) {
		my($re, $gr, $bl) = apart($set::design{'list_hove'});
		my $rel = $re + 51; if($rel > 255){ $rel = 255; }
		my $grl = $gr + 51; if($grl > 255){ $grl = 255; }
		my $bll = $bl + 51; if($bll > 255){ $bll = 255; }
		my $red = $re - 51; if($red < 0)  { $red = 0; }
		my $grd = $gr - 51; if($grd < 0)  { $grd = 0; }
		my $bld = $bl - 51; if($bld < 0)  { $bld = 0; }
		my $light = sprintf("#%02x%02x%02x",$rel,$grl,$bll);
		my $dark  = sprintf("#%02x%02x%02x",$red,$grd,$bld);
		$list_hover_border = "$light $dark $dark $light";
	}
	return <<"TMP";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta http-equiv="Cache-Control" content="no-cache">
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Expires" content="0">
	<link rel="stylesheet" href="$set::css" hreflang="ja" type="text/css" media="screen, tv, projection">
	<title>${set::title}@{[ $sub?" : $sub":'']}</title>
<style type="text/css">
body {
	color:$set::design{'body_text'};
	background-color     :$set::design{'body_back'};
	background-image     :url("$set::design{'body_imag'}");
	background-repeat    :$set::design{'body_repe'};
	background-attachment:$set::design{'body_atta'};
	background-position  :$set::design{'body_posi'};
}
#base {
	background: url("./img/translucent_@{[ $back?'white':'black' ]}70.png");
	background: rgba($back, $back, $back, 0.7);
	background:         linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
	background:      -o-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
	background:    -moz-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
	background: -webkit-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
}
#footer {
	background: rgb($back, $back, $back);
	background: rgba($back, $back, $back, 0.5);
}

a        { color:$set::design{'link_text'}; }
a:visited{ color:$set::design{'link_visi'}; }
a:hover  { color:$set::design{'link_hvtx'} !important; background-color:$set::design{'link_hove'} !important; }
.navi a:link    { color:$set::design{'body_text'}; }
.navi a:visited { color:$set::design{'body_text'}; }

#header,
#header:before,
#header:after,
#sub:before,
#sub:after,
#sub h1:before,
#sub h1:after,
#footer,
.navi {
	color:$set::design{'head_text'};
	border-color:$set::design{'head_line'};
}
#header h1 a:link    { color:$set::design{'head_text'}; }
#header h1 a:visited { color:$set::design{'head_text'}; }

input[type="text"],
input[type="password"],
select {
	background-color:$set::design{'input_back'};
	border-color:$set::design{'body_text'};
	color:$set::design{'input_text'};
}

.chara .box li a {
	background-color:$set::design{'list_back'};
	border-color:$list_border;
	color:$set::design{'list_text'};
}
.chara .box li a:hover {
	background-color:$set::design{'list_hove'} !important;
	border-color:$list_hover_border;
	color:$set::design{'list_hvtx'} !important;
}

.group {
	border-color:$set::design{'table_line'};
}
.group th {
	background-color:$set::design{'table_head'};
	border-color:$set::design{'table_line'};
	color:$set::design{'table_hdtx'};
}
.group td {
	background-color:$set::design{'table_row1'};
	border-color:$set::design{'table_line'};
	color:$set::design{'table_text'};
}
.group .rv td {
	background-color:$set::design{'table_row2'};
}
.group tr:hover td {
	background-color:$set::design{'table_hove'};
}
.group th a {
	color:$set::design{'table_hdtx'};
}

.box,
.sort {
	background: url("./img/translucent_@{[ $back?'white':'black' ]}70.png");
	background: rgba($back, $back, $back, 0.7);
	border-color:$set::design{'box_line'};
}

.box h2 {
	background-color:$set::design{'box_head'};
	color:$set::design{'box_text'};
}

</style>
$style
</head>
<body>
<div id="base">
<div id="header">
	<h1>@{[ $set::titlelink?'<a href="'.$set::titlelink.'">':'' ]}${set::title}@{[ $set::titlelink?'</a>':'' ]}</h1>
</div>
<div id="sub"><h1>@{[ $set::subtitle?$set::subtitle:'&nbsp;' ]}</h1></div>
<div class="navi">
	@{[ $set::homeurl?'[ <a href="'.$set::homeurl.'">HOME</a> ] &nbsp;':'' ]}
	[ <a href="${set::current}${set::cgi}">TOP</a> ] &nbsp;
	[
	<a href="${set::cgi}?mode=form&m=login">シート更新</a> |
	<a href="${set::cgi}?mode=entry">新規作成</a>
	]
</div>
<div class="navi" style="padding-top:2px;">
	<div style="float:left;">
	<select onchange="location.href = this.options[selectedIndex].value">
		<option value="./">グループ別</option>
		<option value="${set::cgi}?mode=tags" @{[ (main::param('mode') eq 'tags')?'selected':'' ]}>タグリスト</option>
	</select>
	</div>
	<form method="get" action="${set::cgi}">
	<input type="text" name="g" value="@{[ ($main::m =~ /search/) ? $main::g : '' ]}" style="width:150px;">
	<input type="hidden" name="mode" value="list2">
	<select name="m">
		<option value="search_t" @{[ ($main::m eq 'search_t')?'selected':'' ]}>タグ</option>
		<option value="search_n" @{[ ($main::m eq 'search_n')?'selected':'' ]}>名前</option>
	</select>
	<input type="submit" value=" 検索 ">
	</form>
</div>

TMP
}

sub _footer {
	return <<"TMP";

<div id="footer">
	<div class="copy">
	ゆとシート for DX3rd ver.$main::ver - <a href="http://yutorize.2-d.jp/">ゆとらいず工房</a>
	</div>
</div>
</div>
</body>
</html>
TMP
}

1;
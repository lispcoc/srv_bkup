#################### リスト.2 ####################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use Encode;

my $oldtime = $set::oldtime;

my $url = $set::cgi;
my $page= "20";
   $page= $set::list_max_num if $set::list_max_num;
my @list_max_nums = (20,50,100,200,500);
   @list_max_nums = @set::list_max_nums if @set::list_max_nums;
my $now = time;

our $l = Encode::decode('utf8', param('l'));
our $m = Encode::decode('utf8', param('m'));
our $g = Encode::decode('utf8', param('g'));
our $s = Encode::decode('utf8', param('s'));
our $p = Encode::decode('utf8', param('p'));
our $o = Encode::decode('utf8', param('o'));

$page = $l if $l;

### 読み込み ###
open my $FH, $set::listfile or die $!;

my @list;
if($m eq 'group')   { @list = grep { (split(/<>/))[4] eq $g } <$FH>; }
#elsif($m eq 'pl')   { @list = grep { (split(/<>/))[5] eq $g } <$FH>; }
elsif($m eq 'search_t') { @list = grep { $g && (split(/<>/))[16] =~ / $g / } <$FH>; }
elsif($m eq 'search_n') { @list = grep { (split(/<>/))[3] =~ /$g/ } <$FH>; }
else{ @list = <$FH>; }

if    ($s eq 'name') { @list = sort { (split(/<>/,$a))[3] cmp (split(/<>/,$b))[3] } @list; }
elsif ($s eq 'exp')  { @list = sort { (split(/<>/,$b))[6] <=> (split(/<>/,$a))[6] } @list; }
elsif ($s eq 'pl' )  { @list = sort { (split(/<>/,$b))[5] <=> (split(/<>/,$a))[5] } @list; }
elsif ($s eq 'age')  { @list = sort { (split(/<>/,$b))[11] <=> (split(/<>/,$a))[11] || (split(/<>/,$b))[11] cmp (split(/<>/,$a))[11] } @list; }
elsif ($s eq 'time') { @list = sort { (split(/<>/,$b))[2] <=> (split(/<>/,$a))[2] } @list; }
elsif ($m eq '')     { @list = sort { (split(/<>/,$b))[1] <=> (split(/<>/,$a))[1] } @list; }

###  ###
if($p < 0){ $p = 0; }
my $count = my $hidden = my $exp_to = 0; my $pp = $p * $page + $page; my $lost; my @print; my %pls; my %sex;
foreach (@list) {
  my $sort;
  my ($file, undef, $time, $name, $group, $pl, $exp, $age, $sex, $sign, $blood, $breed, $syndrome, $d_lois, $codename, $hide, $works, $cover) = (split /<>/, $_)[0..14,17,18..19];
  if($hide == 1 && $m ne 'search_t'){ next; }
  if(!$pls{$pl}){ $pls{$pl} = $pl; }
  if($m eq 'pl' && $pl ne $g){ next; }
  if($oldtime && $m ne "pl" && $now-$time > $oldtime) { next; }
  if($set::noname_view && $name eq "" && !$codename){ $name = '&nbsp;' }
  if($set::noname_view && $pl eq "")  { $pl   = '&nbsp;' }
  if($name eq "" && $codename){ $name = $codename; } elsif($m eq "pl" && $name eq ""){ $hidden++; $exp_to += $exp; next; } elsif ($name eq ""){ next; }
  if($m eq "pl" && $group eq "rip"){ $lost++; }
  if($sex eq ''){ $sex = '空欄' }
  
  my @syndrome = (split /\//, $syndrome);
  my @d_lois = (split /\//, $d_lois);
  
  my $p_sex;
  if   ($sex eq "男" || $sex eq "♂" || $sex eq "男性" || $sex eq "男性型" || $sex eq "男の子" || $sex eq "雄" || $sex eq "爺" || $sex eq "漢") { $p_sex = '♂'; $sex{'♂'}++; if($s eq "sex"){ $sort = "1"; } } 
  elsif($sex eq "女" || $sex eq "♀" || $sex eq "女性" || $sex eq "女性型" || $sex eq "女の子" || $sex eq "雌" || $sex eq "婆") { $p_sex = '♀'; $sex{'♀'}++;  if($s eq "sex"){ $sort = "2"; } }
  else { $p_sex = '？'; $sex{$sex}++; if($s eq "sex"){ $sort = "3"; } }
  if($m eq 'sex' && (($p_sex ne '？' && $p_sex ne $g) || ($p_sex eq '？' && $sex ne $g))){ next; }
  

  my $p_group;
  foreach (@set::groups){
    if($group eq @$_[0]){
      $p_group = @$_[2];
      if($s eq "group"){
        if(@$_[1] eq ""){ if($o){ $sort = '0'; } else { $sort = 'xx'; } }
        else { $sort = @$_[1]; }
      }
    }
  }
  
  my $pll = uri_escape_utf8($pl);
  
  my $agesize = length($age); my $agecss; if ($agesize > 8){ $agecss = " sml"; }else{ $agecss = ""; }

  my ($min,$hour,$day,$mon,$year) = (localtime($time))[1..5];
  ###
  my $tds = "$sort<>";
  $tds .= '<td class="name"><a href="'.$set::datadir.$file.'.html">'.$name.'</a></td>';
  if($m ne "pl")  { $tds .= '<td class="name nr sml"><a href="'.$url.'?mode=list2&m=pl&g='.$pll.'">'.$pl.'</a></td>'; }
  if($m ne "sex"){ $tds .= '<td class="C" style="color:'.($p_sex eq '♂' ? '#8888dd' : $p_sex eq '♀' ? '#dd8888' : '').'">'.$p_sex.'</td>'; }
  $tds .= '<td class="C'.$agecss.'">'.$age.'</td>';
  $tds .= '<td class="name">'.$sign.'</td>';
  if($m ne "group") { $tds .= '<td class="name nr"><a href="'.$url.'?mode=list2&m=group&g='.$group.'">'.$p_group.'</a></td>'; }
  $tds .= '<td class="C nr">'.$exp.'</td>';
  $tds .= '<td class="C nr">'.$breed.'</td>';
  $tds .= '<td class="nr">'.join(" , ", @syndrome).'</td>';
  $tds .= '<td class="nr">'.join(" , ", @d_lois).'</td>';
  $tds .= '<td class="nr">'. $works.'／'.$cover.'</td>';
  $tds .= '<td class="C nr sml">'.sprintf("%02d/%02d-%02d:%02d",$mon+1,$day,$hour,$min).'</td>';
  $tds .= "\n";
  push @print, "$tds";
  
  $count++; $exp_to += $exp;
}

### サブタイトル、メニュー ###
  my ($nowpage,$title_sub,$menu,$head,$pn);
  if($p*$page+$page >= $count){ $nowpage = ($p*$page+1)."-$count"; }
  else { $nowpage = ($p*$page+1)."-".($p*$page+$page); }
$menu = '<div class="navi" style="padding-top:2px;text-align:left;overflow:hidden;">';

$menu .= '<div style="float:right;">表示件数: <select onchange="location.href = this.options[selectedIndex].value">';
foreach(@list_max_nums){
  $menu .= '<option value="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').'&l='.$_.($o?"&o=1":'').'"'.(($l == $_ || (!$l && $_ == $page))?' selected':'').'>'.$_.'</option>';
}
$menu .= '</select></div>';

if($m eq "group"){
  my @groups = sort { @$a[1] cmp @$b[1] } @set::groups;
  $menu .= '<select onchange="location.href = this.options[selectedIndex].value">';
  $menu .= '<option value="'.$url.'?mode=list2">ALL</option>';
  foreach (@groups){
    if($g eq @$_[0]){ $title_sub = @$_[2]; $head = "@$_[2] <small>@$_[3]（$nowpage/$count）　<a href=\"./#@$_[2]\">&lt;&lt;</a></small>"; }
    if(!@$_[1]){ next; }
    $menu .= '<option value="'.$url.'?mode=list2&m=group&g='.@$_[0].($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'"'.(($g eq @$_[0])?' selected':'').'>'.@$_[2].'</option>';
  }
  $menu .= '</select>';
}
elsif($m eq "pl"){
  if($hidden == 0){ $hidden = ""; }else{ $hidden = "+$hidden" }
  $title_sub = $g; $head = "$g <small>（$nowpage/$count）　<a href=\"$url?mode=list1&m=pl#$g\">&lt;&lt;</a></small>";
  $menu .= '<select onchange="location.href = this.options[selectedIndex].value">';
  $menu .= '<option value="'.$url.'?mode=list2">ALL</option>';
  foreach (sort keys %pls){
    $menu .= '<option value="'.$url.'?mode=list2&m=pl&g='.uri_escape_utf8($_).($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'"'.(($g eq $_)?' selected':'').'>'.$_.'</option>';
  }
  $menu .= '</select>';
}
elsif($m eq "sex"){
  $title_sub = $g; $head = "$g <small>（$nowpage/$count）　<a href=\"$url?mode=list1&m=sex#$g\">&lt;&lt;</a></small>";
  $menu .= '<select onchange="location.href = this.options[selectedIndex].value">';
  $menu .= '<option value="'.$url.'?mode=list2">ALL</option>';
  foreach (sort { $sex{$b} cmp $sex{$a} } keys  %sex){
    $menu .= '<option value="'.$url.'?mode=list2&m=sex&g='.uri_escape_utf8($_).($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'"'.(($g eq $_)?' selected':'').'>'.$_.'</option>';
  }
  $menu .= '</select>';
}
elsif($m eq "search_t"){
  $title_sub = "タグ「$g」検索結果"; $head = "タグ「$g」検索結果 <small>（$nowpage/$count）</small>";
}
elsif($m eq "search_n"){
  $title_sub = "名前「$g」検索結果"; $head = "名前「$g」検索結果 <small>（$nowpage/$count）</small>";
}
else {
  $title_sub = "全キャラ一覧"; $head = "全キャラ一覧 <small>（$nowpage/$count）</small>";
}
$menu .= '</div>';

### prev/next ###
if(1){
  my $last = int($count / $page);
  $pn  = '<div class="sort C">';
  if($p <= 0){ $pn .= '&lt;&lt;first '; }
  else{ $pn .= '<a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'&p=0">&lt;&lt;first</a> '; }
  if($p <= 0){ $pn .= '&lt;&lt;prev'; }
  else{ $pn .= '<a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'&p='.($p - 1).'">&lt;&lt;prev</a>'; }
  for(my $i = 0; $i <= $last; $i++){
    if($i == $p){ $pn .= ' ['.($i+1).'] ' }
    else { $pn .= ' <a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'&p='.$i.'">['.($i + 1).']</a> '; }
  }
  if($p >= $last){ $pn .= 'next&gt;&gt;'; }
  else{ $pn .= '<a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'&p='.($p + 1).'">next&gt;&gt;</a>'; }
  if($p >= $last){ $pn .= ' last&gt;&gt;'; }
  else{ $pn .= ' <a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').($s?"&s=$s":'').($l?"&l=$l":'').($o?"&o=1":'').'&p='.$last.'">last&gt;&gt;</a>'; }
  $pn .= '</div>';
}
### print ###
my $header_head = <<"TMP";
  <style type="text/css">
  .chara { max-width:932px; }
  .sort { width:802px; margin:auto; }
  .C { text-align:center; padding:5px 0px !important; }
  .R { text-align:right; }
  .nr{ white-space:nowrap; }
  .sml{ font-size:11px !important; }
  </style>
TMP

require $set::lib_template;

print "Content-type: text/html\n\n";

print &template::_header($title_sub, $header_head);
print <<"HTML";
$template::header
$menu
<div class="chara">
$pn
<div class="box"><h2>$head</h2>
<table class="group">
HTML
  my ($o_rv1, $o_rv2); 
  if($o == 1) { $o_rv1 = '&o=1'; $o_rv2 = ''; } else { $o_rv1 = ''; $o_rv2 = '&o=1'; }
  if($m eq "pl" || $m eq "faith"){ $g =  uri_escape_utf8($g); }
  print "<tr>";
    if($s eq "name") { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=name'.($l?"&l=$l":'').$o_rv2.'">PC</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=name'.($l?"&l=$l":'').$o_rv1.'">PC</a></th>'; }
  if($m ne "pl") {
    if($s eq "pl")   { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=pl'.($l?"&l=$l":'').$o_rv2.'">PL</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=pl'.($l?"&l=$l":'').$o_rv1.'">PL</a></th>'; }
  }
  if($m ne "sex") {
    if($s eq "sex")  { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=sex'.($l?"&l=$l":'').$o_rv2.'">性</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=sex'.($l?"&l=$l":'').$o_rv1.'">性</a></th>'; }
  }
  if($m ne "age") {
    if($s eq "age")  { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=age'.($l?"&l=$l":'').$o_rv2.'">年齢</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=age'.($l?"&l=$l":'').$o_rv1.'">年齢</a></th>'; }
  }
  if($m ne "sign") {
    if($s eq "sign") { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=sign'.($l?"&l=$l":'').$o_rv2.'">星座</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=sign'.($l?"&l=$l":'').$o_rv1.'">星座</a></th>'; }
  }
  if($m ne "group") {
    if($s eq "group"){ print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=group'.($l?"&l=$l":'').$o_rv2.'">分類</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=group'.($l?"&l=$l":'').$o_rv1.'">分類</a></th>'; }
  }
  if($m ne "exp") {
    if($s eq "exp")  { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=exp'.($l?"&l=$l":'').$o_rv2.'">経験点</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=exp'.($l?"&l=$l":'').$o_rv1.'">経験点</a></th>'; }
  }
  if($m ne "breed") {
    if($s eq "breed"){ print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=breed'.($l?"&l=$l":'').$o_rv2.'">ブリード</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=breed'.($l?"&l=$l":'').$o_rv1.'">ブリード</a></th>'; }
  }
  if($m ne "syndrome") {
    if($s eq "syndrome"){ print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=syndrome'.($l?"&l=$l":'').$o_rv2.'">シンドローム</a></th>'; }
    else                { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=syndrome'.($l?"&l=$l":'').$o_rv1.'">シンドローム</a></th>'; }
  }
  if($m ne "d_lois") {
    if($s eq "d_lois"){ print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=d_lois'.($l?"&l=$l":'').$o_rv2.'">Dロイス</a></th>'; }
    else              { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=d_lois'.($l?"&l=$l":'').$o_rv1.'">Dロイス</a></th>'; }
  }
  if($m ne "works") {
    print "aaa";
    if($s eq "works"){ print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=works'.($l?"&l=$l":'').$o_rv2.'">ワークス／カヴァー</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=works'.($l?"&l=$l":'').$o_rv1.'">ワークス／カヴァー</a></th>'; }
  }
  if($m ne "time") {
    if($s eq "time") { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=time'.($l?"&l=$l":'').$o_rv2.'">更新日時</a></th>'; }
    else             { print '<th><a href="'.$url.'?mode=list2'.($m?"&m=$m":'').($g?"&g=$g":'').'&s=time'.($l?"&l=$l":'').$o_rv1.'">更新日時</a></th>'; }
  }
  print "</tr>\n";
  
  if ($s eq "sign" || $s eq "sex" || $s eq "group" || $s eq "syndrome"){ @print = sort { (split(/<>/,$a))[0] cmp (split(/<>/,$b))[0] } @print; }
  if($o == 1) { @print = reverse(@print); }
  my $i = 0;
  foreach ( @print ){ $i++;
    if($i > $pp || $i <= $p * $page){ next; }
    my @printv = split( /<>/, $_);
    my $rv = "";
    if($i % 2 == 0){ $rv = ' class="rv"'; }
    print "  <tr$rv>".$printv[1]."</tr>\n";
  }
print <<"HTML";
</table><div Style="clear:both;"></div></div>
$pn
</div>
HTML
print &template::_footer($set::admin);
1;
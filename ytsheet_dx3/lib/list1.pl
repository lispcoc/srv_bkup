#################### リスト.1 ####################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use Encode;

my $url = $set::cgi;

our $m = Encode::decode('utf8', param('m'));

my $title_sub;
if   ($m eq "pl")   { $title_sub = "プレイヤー別"; }

require $set::lib_template;

my $now = time;

### print ###
print "Content-type: text/html\n\n";
print &template::_header($title_sub);
print '<div class="chara" style="width:500px;"><div class="box"><p class="text">'.$set::message.'</p></div></div>' if ($set::message);
print '<div class="chara">';

open (my $FH, '<', $set::listfile) or die $!;

my (%list,%ct_fai,%ct_pri,%exp,%count,%lost,%alive);
while (<$FH>) {
  chomp $_;
  my ($name_s,$sort,$rv);
  my ($file, undef, $time, $name, $group, $pl, $exp, $age, $sex, $sign, $blood, $breed, $syndrome, $d_lois, $codename, $hide, $works, $cover) = (split /<>/, $_)[0..14,17,18..19];
  if($hide == 1 && $m ne 'search_t'){ next; }
  if($set::oldtime && $now-$time > $set::oldtime && $m ne "pl") { next; }
  if($set::noname_view && $name eq ""){ $name = '&nbsp;' }
  if($set::noname_view && $pl eq "")  { $pl   = '&nbsp;' }
  if($name eq "" && $m ne "pl"){ next; }
  my $sub;
  if($m eq "pl"){
    $sub = $pl;
    if(!$alive{$sub}){ $alive{$sub} = 0; }
    if($set::oldtime && $now-$time < $set::oldtime) { $alive{$sub}++; }
    $exp{$sub} += $exp; $count{$sub}++;
    if($group eq "rip"){ $lost{$sub}++; } #ロストキャラカウント
    if($pl eq "" || $name eq ""){ next; }
    foreach my $i (@set::groups){
      if($group eq @$i[0]){
        $name_s = @$i[2];
        if (@$i[1] eq "") { $sort = "<!-- xx -->"; }
        else { $sort = "<!-- @$i[1] -->"; }
        last;
      }
    }
  }
  elsif($m eq "sex"){
    if   ($sex eq "♂" || $sex eq "男" || $sex eq "男性" || $sex eq "男の子" || $sex eq "男性型" || $sex eq "雄") { $sub = "1<>♂<>男・男性・男の子・男性型・雄"; }
    elsif($sex eq "♀" || $sex eq "女" || $sex eq "女性" || $sex eq "女の子" || $sex eq "女性型" || $sex eq "雌") { $sub = "2<>♀<>女・女性・女の子・女性型・雌"; }
    elsif($sex eq "&nbsp;" || !$sex) { $sub = "4<>空欄"; }
    else { $sub = "3<>" . $sex; }
    $name_s = $pl;
  }
  else {
    $sub = 0;
    foreach my $i (@set::groups){
      if($group eq @$i[0]){
        if(!@$i[1]){ last; }
        else{ $sub = "@$i[1]<>@$i[0]<>@$i[2]<>@$i[3]"; last; }
      }
    }
    $name_s = $pl;
  }

  push @{$list{$sub}}, "$sort<li$rv><a href=\"${set::datadir}${file}.html\">".($codename?"“$codename”":'')."$name <small>（$name_s）</small></a></li>";
}

foreach my $sub (sort keys %list) {
  my $p_name; my $p_text; my $count;
  if($m eq "pl"){
    if($set::oldtime &&( !$count{$sub} || !$alive{$sub})){ next; }
    $count = @{$list{$sub}};
    my $link = uri_escape_utf8($sub);
    @{$list{$sub}} = sort { $a cmp $b } @{$list{$sub}};
    $p_name = $sub;
    $p_text = "（$count{$sub}）　<a href=\"$url?mode=list2&m=pl&g=$link\">&gt;&gt;</a>";
  }
  elsif($m eq "race"){
    my($name, $link) = (split /<>/, $sub)[1,2];
    $count = @{$list{$sub}};
    if($link =~ /ナイトメア/){ $link = "ナイトメア"; }
    if($link =~ /ウィークリング/){ $link = "ウィークリング"; }
    $link = uri_escape_utf8($link);
    $p_name = $name;
    $p_text = "（$count）　<a href=\"$url?mode=list2&m=race&g=$link\">&gt;&gt;</a>";
  }
  elsif ($m eq "faith"){
    my($name, $link) = (split /<>/, $sub)[1,2];
    $link = uri_escape_utf8($link);
    if($ct_fai{$sub} eq ""){ $ct_fai{$sub} = 0; }
    if($ct_pri{$sub} eq ""){ $ct_pri{$sub} = 0; }
    $p_name = $name;
    $p_text = "（$ct_pri{$sub}+$ct_fai{$sub}）　<a href=\"$url?mode=list2&m=faith&g=$link\">&gt;&gt;</a>";
  }
  elsif($m eq "sex"){
    my($name, $text) = (split /<>/, $sub)[1,2];
    $count = @{$list{$sub}};
    $p_name = $name;
    $p_text = "$text （$count）";
  }
  elsif($m eq "honor"){
    my ($name, $text) = (split /<>/, $sub)[1,2];
    $count = @{$list{$sub}};
    $p_name = $name;
    $p_text = "$text （$count）";
  }
  else{
    my ($name, $text, $link)  = (split /<>/, $sub)[2,3,1];
    $link = uri_escape_utf8($link);
    $count = @{$list{$sub}};
    $p_name = $name;
    $p_text = "$text （$count）　<a href=\"$url?mode=list2&m=group&g=$link\">&gt;&gt;</a>";
  }
  print '<div class="box"><div class="anchor_hide" id="'.$p_name.'"></div><h2>'.$p_name.' <small>'.$p_text.'</small></h2><ul>' . (join ' ', @{$list{$sub}}) . '</ul></div>'."\n";
}
print '</div>';
print &template::_footer;

1;
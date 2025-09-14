################### データ保存 ###################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use Encode;

my $mode = param('mode');

our %pc;
for (param()){ $pc{$_} = param($_); }
$pc{'birth'} = time;
if ($pc{'id'} eq ''){
  $pc{'id'} = $pc{'birth'};
}
if (!$pc{'file'}) {
  $pc{'file'} = $pc{'birth'};
}

our $make_error;
if ($mode eq 'make'){
  if ($pc{'id'} eq '')  { $make_error .= '記入エラー：IDが入力されていません。<br>'; }
  elsif ($pc{'id'} =~ /[^0-9A-Za-z\.\-_]/) { $make_error .= '記入エラー：パスワードに使える文字は、半角の英数字とピリオド、ハイフン、アンダーバーだけです。'; }
  else {
    open (my $FH, '<', $set::passfile) or $make_error .= 'システムエラー : 一覧データのオープンに失敗しました。<br>';
    while (<$FH>){ 
      if ($_ =~ /^$pc{'id'}<>/){ $make_error .= '記入エラー：そのIDは既に使用されています。<br>'; last; }
    }
    close ($FH);
  }
  if ($pc{'pass'} eq ''){ $make_error .= '記入エラー：パスワードが入力されていません。<br>'; }
  else {
    if (!$set::entry_restrict && $pc{'pass'} =~ /[^0-9A-Za-z\.\-\/]/) { $make_error .= '記入エラー：パスワードに使える文字は、半角の英数字とピリオド、ハイフン、スラッシュだけです。<br>'; }
    if ($pc{'confirm'} eq '') { $make_error .= '記入エラー：パスワードが再入力されていません。<br>'; }
    else { if($pc{'pass'} ne $pc{'confirm'}){ $make_error .= '記入エラー：パスワードと再入力されたパスワードが一致しません。<br>'; } }
  }
#  if ($pc{'mail'} eq '') { $make_error .= '記入エラー：メールアドレスが入力されていません。<br>'; }
  if ($set::registkey ne '' && $set::registkey ne $pc{'registkey'}) { $make_error .= '記入エラー：登録キーが一致しません。<br>'; }
}
if ($make_error) { require $set::lib_edit; exit; }


######################################################################################################
## バージョン
  my $ver = $main::ver;

## 最終更新
  $pc{'lastupdate'} = time;
  my($day,$mon,$year) = (localtime($pc{'lastupdate'}))[3..5];
  $year += 1900; $mon++;
  my $lastupdate = sprintf("%04d/%02d/%02d",$year,$mon,$day);


### 基礎ステータス算出 ###############################################################################
## 経験点
  if($pc{'exp_auto'}){
    $pc{'exp'} = $pc{'make_exp'};
    for (my $i = 1; $i <= $pc{'count_history'}; $i++){
      $pc{'exp'} += s_eval($pc{"hist_exp$i"});
    }
  }

## ブリード
  my $breed;
  if($pc{'syndrome1'} && $pc{'syndrome2'} && $pc{'syndrome3'})
    { $breed = 'トライブリード'; }
  elsif($pc{'syndrome1'} && $pc{'syndrome2'})
    { $breed = 'クロスブリード'; }
  elsif($pc{'syndrome1'})
    { $breed = 'ピュアブリード'; }

## 基礎能力値
  my ($stt_syn_body, $stt_syn_sense, $stt_syn_spirit, $stt_syn_social);
  if ($breed eq 'ピュアブリード') {
    $stt_syn_body   = $set::syndrome{$pc{'syndrome1'}}{'stt'}[0] * 2;
    $stt_syn_sense  = $set::syndrome{$pc{'syndrome1'}}{'stt'}[1] * 2;
    $stt_syn_spirit = $set::syndrome{$pc{'syndrome1'}}{'stt'}[2] * 2;
    $stt_syn_social = $set::syndrome{$pc{'syndrome1'}}{'stt'}[3] * 2;
  } else {
    $stt_syn_body   = $set::syndrome{$pc{'syndrome1'}}{'stt'}[0] + $set::syndrome{$pc{'syndrome2'}}{'stt'}[0];
    $stt_syn_sense  = $set::syndrome{$pc{'syndrome1'}}{'stt'}[1] + $set::syndrome{$pc{'syndrome2'}}{'stt'}[1];
    $stt_syn_spirit = $set::syndrome{$pc{'syndrome1'}}{'stt'}[2] + $set::syndrome{$pc{'syndrome2'}}{'stt'}[2];
    $stt_syn_social = $set::syndrome{$pc{'syndrome1'}}{'stt'}[3] + $set::syndrome{$pc{'syndrome2'}}{'stt'}[3];
  }
  my $stt_body   = $stt_syn_body   + $pc{'stt_grow_body'}   + $pc{'stt_add_body'}   + ($pc{'stt_works'} eq 'body'  ? 1 : 0);
  my $stt_sense  = $stt_syn_sense  + $pc{'stt_grow_sense'}  + $pc{'stt_add_sense'}  + ($pc{'stt_works'} eq 'sense' ? 1 : 0);
  my $stt_spirit = $stt_syn_spirit + $pc{'stt_grow_spirit'} + $pc{'stt_add_spirit'} + ($pc{'stt_works'} eq 'spirit'? 1 : 0);
  my $stt_social = $stt_syn_social + $pc{'stt_grow_social'} + $pc{'stt_add_social'} + ($pc{'stt_works'} eq 'social'? 1 : 0);
  

## 副能力値
  my $hpmax   = $stt_body * 2 + $stt_spirit + 20 + $pc{'sub_hp_add'};
  my $provide = $stt_social * 2 + $pc{'skill_raise_lv'} * 2 + $pc{'sub_provide_add'};
  my $speed   = $stt_sense * 2 + $stt_spirit + $pc{'sub_speed_add'};
  my $move    = $speed + 5 + $pc{'sub_move_add'};
  my $fullmove= $move * 2;
  
  my $stt_invade = $pc{'lifepath_awaken_invade'} + $pc{'lifepath_urge_invade'} + $pc{'lifepath_other_invade'};
  
## 消費経験点 / 財産ポイント
  my $exp_use = -9;

  my $stt_base_body   = $stt_syn_body   + ($pc{'stt_works'} eq 'body'  ? 1 : 0);
  my $stt_base_sense  = $stt_syn_sense  + ($pc{'stt_works'} eq 'sense' ? 1 : 0);
  my $stt_base_spirit = $stt_syn_spirit + ($pc{'stt_works'} eq 'spirit'? 1 : 0);
  my $stt_base_social = $stt_syn_social + ($pc{'stt_works'} eq 'social'? 1 : 0);
  for(my $i = $stt_base_body  +1; $i<=$stt_base_body  +$pc{'stt_grow_body'}  ; $i++){ $exp_use += ($i > 21) ? 30 : ($i > 11) ? 20 : 10; }
  for(my $i = $stt_base_sense +1; $i<=$stt_base_sense +$pc{'stt_grow_sense'} ; $i++){ $exp_use += ($i > 21) ? 30 : ($i > 11) ? 20 : 10; }
  for(my $i = $stt_base_spirit+1; $i<=$stt_base_spirit+$pc{'stt_grow_spirit'}; $i++){ $exp_use += ($i > 21) ? 30 : ($i > 11) ? 20 : 10; }
  for(my $i = $stt_base_social+1; $i<=$stt_base_social+$pc{'stt_grow_social'}; $i++){ $exp_use += ($i > 21) ? 30 : ($i > 11) ? 20 : 10; }
  
  foreach(1..$pc{'skill_fight_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_shoot_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_RC_lv'})   { $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_nego_lv'}) { $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_dodge_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_perce_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_will_lv'}) { $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach(1..$pc{'skill_raise_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 2; }
  foreach my $num(1..$pc{'count_skill'}){
    foreach(1..$pc{'skill_drive'.$num.'_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 1; }
    foreach(1..$pc{'skill_art'  .$num.'_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 1; }
    foreach(1..$pc{'skill_know' .$num.'_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 1; }
    foreach(1..$pc{'skill_info' .$num.'_lv'}){ $exp_use += ($_ > 21) ? 10 : ($_ > 11) ? 5 : ($_ > 6) ? 3 : 1; }
  }
  
  foreach(1..$pc{'count_effect'}){
    $exp_use += ($pc{'effect'.$_.'_lv'}) ? ($pc{'effect'.$_.'_lv'} * 5 + 10) : 0;
    if($pc{'effect'.$_.'_limit'} eq 'Dロイス' || $pc{'effect'.$_.'_limit'} eq 'Ｄロイス'){ $exp_use -= 15; }
  }
  foreach(1..$pc{'count_effect_ez'}){ $exp_use += ($pc{'effect_ez'.$_.'_lv'}) ? 2 : 0; }

  my $item_total_point;
  foreach(1..$pc{'count_weapon'}){ $item_total_point += $pc{'weapon'.$_.'_point'}; $exp_use += $pc{'weapon'.$_.'_exp'}; }
  foreach(1..$pc{'count_armour'}){ $item_total_point += $pc{'armour'.$_.'_point'}; $exp_use += $pc{'armour'.$_.'_exp'}; }
  foreach(1..$pc{'count_item'})  { $item_total_point += $pc{'item'.$_.'_point'};   $exp_use += $pc{'item'.$_.'_exp'}; }
  my $money = $provide - $item_total_point;

### 戦闘特技関連 #####################################################################################
### タグ #############################################################################################
  $pc{'tag'} =~ tr/　/ /;
  $pc{'tag'} =~ tr/０-９Ａ-Ｚａ-ｚ/0-9A-Za-z/;
  $pc{'tag'} =~ tr/＋－＊／．，＿/\+\-\*\/\.,_/;
  $pc{'tag'} =~ tr/ / /s;

### 画像アップロード #################################################################################
  if ($pc{'upload_file'} || $pc{'upload_thum'} || $pc{'upload_back'} || $pc{'del_file'} || $pc{'del_thum'} || $pc{'del_back'}) { require $set::lib_upload; }

### myCSS ############################################################################################
  if($pc{'mycss'}){
    foreach my $i ("css_frame","css_cell1","css_cell2","css_font1","css_font2"){
      next if !$pc{"$i"};
      $pc{"$i"} =~ s/\#//;
      my($re, $gr, $bl) = $pc{"$i"} =~ /.{2}/g;
      $re = hex($re); if($re > 208){ $re = 208; } elsif($i !~ /font/ && $re < 32){ $re = 32; }
      $gr = hex($gr); if($gr > 208){ $gr = 208; } elsif($i !~ /font/ && $gr < 32){ $gr = 32; }
      $bl = hex($bl); if($bl > 208){ $bl = 208; } elsif($i !~ /font/ && $bl < 32){ $bl = 32; }
      my @rgb;
      if($i eq "css_frame"){
        @rgb = sort {$b<=>$a} ($re,$gr,$bl);
        if($re-$rgb[2] > 128) { $re = $rgb[2] + 128; }
        if($gr-$rgb[2] > 128) { $gr = $rgb[2] + 128; }
        if($bl-$rgb[2] > 128) { $bl = $rgb[2] + 128; }
      }
      elsif($i eq "css_cell1" || $i eq "css_cell2" || $i eq "css_font2"){
        @rgb = sort {$b<=>$a} ($re,$gr,$bl);
        if($re-$rgb[2] > 80) { $re = $rgb[2] + 80; }
        if($gr-$rgb[2] > 80) { $gr = $rgb[2] + 80; }
        if($bl-$rgb[2] > 80) { $bl = $rgb[2] + 80; }
      }
      $pc{"$i"} = sprintf("#%02x%02x%02x",$re,$gr,$bl);
    }
  }

#### 改行を<br>タグに変換 ############################################################################
  $pc{'text_free'}    =~ s/\r\n/<br>/g; $pc{'text_free'}    =~ s/\n/<br>/g; $pc{'text_free'}    =~ s/\r/<br>/g;
  $pc{'text_history'} =~ s/\r\n/<br>/g; $pc{'text_history'} =~ s/\n/<br>/g; $pc{'text_history'} =~ s/\r/<br>/g;

######################################################################################################
### 各種ファイル更新 #################################################################################
### エスケープ
  foreach (keys %pc) {
    $pc{$_} =~ s/&/&amp;/g;
    $pc{$_} =~ s/"/&quot;/g;
    $pc{$_} =~ s/</&lt;/g;
    $pc{$_} =~ s/>/&gt;/g;
    $pc{$_} =~ s/\r//g;
    $pc{$_} =~ s/\n//g;
  }
### $passfile
my ($file, $charname, $mail, $charnpc, $plname);
## 新規
if($mode eq 'make'){
#  $pc{'birth'} = time;
  if($set::filename) { $file = $pc{'id'}; } else { $file = $pc{'birth'}; }
  open (my $FH, '>>', $set::passfile) or &error('システムエラー','パスワードファイルのオープンに失敗しました。');
  print $FH "$pc{'id'}<>".( ($set::entry_restrict) ? $pc{'pass'} : &e_crypt($pc{'pass'}) )."<>$file<>$pc{'name'}<>$pc{'mail'}<>$pc{'player'}<>\n";
  close ($FH);
}
## 更新
elsif($mode eq 'update'){
  (undef, undef, $file, $charname, $mail, $plname) = getfile($pc{'id'},$pc{'pass'});
  if(!$file){ &error('入力エラー','IDかパスワードが間違っています。'); }
  if($pc{'name'} ne $charname || $pc{'player'} ne $plname){
    open (my $FH, '+<', $set::passfile) or error('システムエラー','パスワードファイルのオープンに失敗しました。');
    my @list = sort { (split(/<>/,$a))[2] cmp (split(/<>/,$b))[2] || (split(/<>/,$a))[5] cmp (split(/<>/,$b))[5] } <$FH>;
    flock($FH, 2);
    seek($FH, 0, 0);
    foreach (@list){
      my($id, $pass, $file, $name, $mail, $pl) = split /<>/;
      if ( ($id eq $pc{'id'} && (&c_crypt($pc{'pass'}, $pass) || $pc{'pass'} eq $set::masterkey)) && ($name ne $pc{'name'} || $pl ne $pc{'player'}) ){
        print $FH "$id<>$pass<>$file<>$pc{'name'}<>$mail<>$pc{'player'}<>\n";
      }else{
        print $FH $_;
      }
    }
    truncate($FH, tell($FH));
    close($FH);
  }
}
### $listfile
  my $l_file = $file;
  my $l_age = $pc{'prof_age'};
     $l_age =~ tr/０-９/0-9/;
  my $l_god;
  my($name, $name_ruby) = split(/:/,$pc{'name'});
  my($codename, $codename_ruby) = split(/:/,$pc{'codename'});
  my $d_lois;
  foreach(1..7){ $d_lois .= ($d_lois ? '/':'').$pc{'lois'.$_.'_name'} if ($pc{'lois'.$_.'_relation'} eq 'Dロイス' || $pc{'lois'.$_.'_relation'} eq 'Ｄロイス'); }
  $name =~ s/&lt;.*?&gt;//g;
  $name_ruby =~ s/&lt;.*?&gt;//g;
  $codename =~ s/&lt;.*?&gt;//g;
  $codename_ruby =~ s/&lt;.*?&gt;//g;
  $d_lois =~ s/&lt;.*?&gt;//g;

  open (my $FH, "+<", $set::listfile) or error('システムエラー','リストファイルのオープンに失敗しました。');
  my @liss = sort { (split(/<>/,$a))[5] cmp (split(/<>/,$b))[5] || (split(/<>/,$a))[0] cmp (split(/<>/,$b))[0] } <$FH>;
  flock($FH, 2);
  seek($FH, 0, 0);
  my $l_new = "$pc{'birth'}<>$pc{'lastupdate'}<>$name<>$pc{'group'}<>$pc{'player'}<>$pc{'exp'}<>$l_age<>$pc{'prof_sex'}<>$pc{'prof_sign'}<>$pc{'prof_blood'}<>$breed<>$pc{'syndrome1'}/$pc{'syndrome2'}/$pc{'syndrome3'}<>$d_lois<>$codename<>$pc{'session_total'}<> $pc{'tag'} <>$pc{'hide'}<>$pc{'works'}<>$pc{'cover'}";
  my $lisshit;
  foreach (@liss){
    my( $file,$birth,$time,$name,$grp,$pl,$exp,$race,$sex,$god,$lv,$age,$honer,$plc,$title ) = split /<>/;
    if ($file eq $l_file){
      print $FH "$file<>$l_new<>\n";
      $lisshit = 1;
    }else{
      print $FH $_;
    }
  }
  if(!$lisshit){
    print $FH "$l_file<>$l_new<>\n";
  }
  truncate($FH, tell($FH));
  close($FH);

### ${file}.cgi更新 ##################################################################################
  use Fcntl;
  
  my $mask = umask 0; # umask値変更＆保存

  my $id = $pc{'id'}; my $pass = $pc{'pass'};
  delete $pc{'submit'}; delete $pc{'id'}; delete $pc{'pass'};

  sysopen (my $FH, "${set::datadir}${file}.cgi", O_WRONLY | O_TRUNC | O_CREAT, 0666);
  print $FH "ver<>".$ver."\n";
  foreach (sort keys %pc){
    if($pc{$_} ne "") { print $FH "$_<>".$pc{$_}."\n"; }
  }
  close($FH);

  ### 置換 ###
  my %replace = (
   );
   
  foreach (keys %pc) {
    $pc{$_} =~ s/&amp;/&/g;
    $pc{$_} =~ s/&quot;/"/g;
    while( my ($key, $value) = each %replace ){ $value = s_eval($value); if(!$value){ $value = 0; } $pc{$_} =~ s/$key/$value/eg; }
    
    if($set::tag_on){
      foreach my $tag ('b','s','i','u','tt','strike','em','strong','big','small','del','center','sup','sub'){
        1 while $pc{$_} =~ s/&lt;$tag&gt;(.*?)&lt;\/$tag&gt;/<$tag>$1<\/$tag>/gi;
      }
      foreach my $tag ('ruby','rb','rp','rt'){
        $pc{$_} =~ s/&lt;$tag&gt;(.*?)&lt;\/$tag&gt;/<$tag>$1<\/$tag>/gi;
      }
      1 while $pc{$_} =~ s/&lt;font size="(.{0,2}?)"&gt;(.*?)&lt;\/font&gt;/<font size="$1">$2<\/font>/gi;
      1 while $pc{$_} =~ s/&lt;font color="([0-9a-z#]*?)"&gt;(.*?)&lt;\/font&gt;/<span style="color:$1">$2<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;inv&gt;(.*?)&lt;\/inv&gt;/<span class="inv">$1<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;hide&gt;(.*?)&lt;\/hide&gt;/<span class="hide">$1<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;left&gt;(.*?)&lt;\/left&gt;/<div style="text-align:left">$1<\/div>/gi;
      1 while $pc{$_} =~ s/&lt;right&gt;(.*?)&lt;\/right&gt;/<div style="text-align:right">$1<\/div>/gi;
      1 while $pc{$_} =~ s/&lt;c:([0-9a-z#]*?)&gt;(.*?)&lt;\/c&gt;/<span style="color:$1">$2<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;bc:([0-9a-z#]*?)&gt;(.*?)&lt;\/bc&gt;/<span style="background-color:$1">$2<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;fs:([0-9]{0,3}?px)&gt;(.*?)&lt;\/fs&gt;/<span style="font-size:$1">$2<\/span>/gi;
      1 while $pc{$_} =~ s/&lt;ff:([0-9a-z \-']+)&gt;(.*?)&lt;\/ff&gt;/<span style="font-family:$1">$2<\/span>/gi;
      $pc{$_} =~ s/&lt;rb:"(.*?)"&gt;(.*?)&lt;\/rb&gt;/<ruby><rb>$2<\/rb><rp>(<\/rp><rt>$1<\/rt><rp>)<\/rp><\/ruby>/gi;
      $pc{$_} =~ s/&lt;rb:(.*?)&gt;(.*?)&lt;\/rb&gt;/<ruby><rb>$2<\/rb><rp>(<\/rp><rt>$1<\/rt><rp>)<\/rp><\/ruby>/gi;
      $pc{$_} =~ s/&lt;hr&gt;(?:&lt;br&gt;)?/<hr>/gi;
      $pc{$_} =~ s/&lt;hr2&gt;(?:&lt;br&gt;)?/<hr class="dot">/gi;
      $pc{$_} =~ s/&lt;hr3&gt;(?:&lt;br&gt;)?/<hr class="das">/gi;
      $pc{$_} =~ s/&lt;hr4&gt;(?:&lt;br&gt;)?/<hr class="gro">/gi;
      $pc{$_} =~ s/&lt;hr5&gt;(?:&lt;br&gt;)?/<hr class="rid">/gi;
      foreach my $url (@set::safeurl){
        next if !$url;
        $pc{$_} =~ s/&lt;a href="($url[^"]+?)"&gt;(.+?)&lt;\/a&gt;/<a href="$1" target="_blank">$2<\/a>/gi;
      }
      $pc{$_} =~ s/&lt;a href="(#[^"]+?)"&gt;(.+?)&lt;\/a&gt;/<a href="$1">$2<\/a>/gi;
      $pc{$_} =~ s/&lt;a href="([^"]+?)"&gt;(.+?)&lt;\/a&gt;/<a href="${set::current}${set::cgi}?jump=$1" target="_blank">$2<\/a>/gi;
    }
    $pc{$_} =~ s/&lt;br&gt;/<br>/gi;
    if($_ =~ /^(?:text_items|text_free|text_history|text_original)$/){
      $pc{$_} =~ s/&lt;\*\*\*(.*?)&gt;/<div class="sub small">$1<\/div>/gi;
      $pc{$_} =~ s/&lt;\*\*(.*?)&gt;/<div class="sub">$1<\/div>/gi;
      $pc{$_} =~ s/\A&lt;\*(.*?)&gt;(?:<br>)?/$pc{"head_$_"} = $1; ''/gie;
      $pc{$_} =~ s/&lt;\*(.*?)&gt;/<\/td><\/tr><tr><th class="L" style="padding-top:2px;">$1<\/th><\/tr><tr><td class="L">/gi;
      if($set::tag_on){
        $pc{$_} =~ s/&lt;table(?:\((.*?)\))?&gt;(.+?)&lt;\/table&gt;/'<table class="txtable"'.&tablestyle($1).'>'.&tablecall($2).'<\/table>'/egi;
        1 while $pc{$_} =~ s/(\A|<br>)\|table(?:\((.*?)\))?\|<br>\|(.+?)\|(<br><br>|(?:<br>)?$)/$1.'<table class="txtable"'.&tablestyle($2).'>'.&tablecall2($3).'<\/table>'.$4/egi;
        1 while $pc{$_} =~ s/(\A|<br>)\|(.+?)\|(<br><br>|(?:<br>)?$)/$1.'<table class="txtable">'.&tablecall2($2).'<\/table>'.$3/egi;
        $pc{$_} =~ s/&lt;box&gt;(.*?)&lt;\/box&gt;/<div class="box">$1<\/div>/gi;
        $pc{$_} =~ s/&lt;box\(([0-9]{1,3}?(?:%|em|px))(?:,([0-9]{1,3}?(?:%|em|px)|auto))?\)&gt;(.*?)&lt;\/box&gt;/<div class="box" style="width:$1;height:$2;">$3<\/div>/gi;
        $pc{$_} =~ s/(<\/?table(?: .*?)?>|<\/?tr(?: .*?)?>|<\/?th(?: .*?)?>|<\/?td(?: .*?)?>|<col(?: .*?)?>|<\/?center>|<div(?: .*?)?>|<\/div>)<br>/$1/gi;
      }
    }
  }
  sub tablestyle {
    my $style;
    my $in = shift;
    my @data = split(/,/, $in);
    foreach(@data){
      if($_ =~ /^[0-9]+(px|em|%)$/){ $style .= 'width:'.$_.';'; }
      if($_ =~ /^#[0-9a-z]+$/i){ $style .= 'background-color:'.$_.';'; }
      if($_ =~ /^(left|center|right)$/i){ $style .= 'text-align:'.$_.';'; }
      if($_ =~ /^none$/i){ $style .= 'border:0;'; }
      if($_ =~ /^dotted$/i){ $style .= 'border-style:dotted;'; }
      if($_ =~ /^hr$/i){ $style .= 'border-width:1px 0px;'; }
      if($_ =~ /^B$/i){ $style .= 'font-weight:bold;'; }
    }
    if($style){ $style = ' style="'.$style.'"'; }
    return $style;
  }
  sub tablecall {
    my $data = shift;
    $data =~ s/&lt;tr&gt;(.*?)&lt;\/tr&gt;/<tr>$1<\/tr>/gi;
    $data =~ s/&lt;col(?:\((.*?)\))?( (?:col|row)span="[0-9]+?")?&gt;/'<col'.&tablestyle($1).$2.'>'/egi;
    $data =~ s/&lt;th(?:\((.*?)\))?( (?:col|row)span="[0-9]+?")?&gt;(.*?)&lt;\/th&gt;/'<th'.&tablestyle($1).$2.'>'.$3.'<\/th>'/egi;
    $data =~ s/&lt;td(?:\((.*?)\))?( (?:col|row)span="[0-9]+?")?&gt;(.*?)&lt;\/td&gt;/'<td'.&tablestyle($1).$2.'>'.$3.'<\/td>'/egi;
    return $data;
  }
  sub tablecall2 {
    my $out;
    my @tr = split(/\|<br>\|/, $_[0]);
    my @col;
    foreach(@tr){
      $_ =~ s/^(.*?)\|c<br>\|/@col = &colcall($1); ''/ei;
      $out .= '<tr>';
      my @td = split(/\|/, $_);
      my $i = 0; my $cs = 0;
      foreach(@td){
        $cs++;
        if($_ eq '&gt;'){ $i++; next; }
        if($_ =~ /^~/){ $_ =~ s/^~//; $out .= '<th'.$col[$i].( $cs?' colspan="'.$cs.'"':'' ).'>'.$_.'</th>'; }
        else { $out .= '<td'.$col[$i].( $cs?' colspan="'.$cs.'"':'' ).'>'.$_.'</td>'; }
        $i++;
        $cs = 0;
      }
      $out .= '</tr>';
    }
    return $out;
  }
  sub colcall {
    my @out;
    my @col = split(/\|/, $_[0]);
    foreach(@col){
      push (@out, &tablestyle($_));
    }
    return @out;
  }

######################################################################################################
### ${file}.html更新 #################################################################################
  my $blank = '&nbsp;';

### バックアップリスト ###############################################################################
my $pr_backlist;
if ($set::backuponoff eq "1"){
  if (!-d "${set::backdir}${file}"){ mkdir "${set::backdir}${file}"; }
  opendir(DIR,"${set::backdir}${file}") or &error('システムエラー',"${set::backdir}${file}/が開けませんでした。");
  my @backlist = readdir(DIR);
  closedir(DIR);
  my $i = 1;
  foreach (reverse sort @backlist) {
    if($i > $set::backupage){ unlink("${set::backdir}${file}/$_"); next; }
    if ($_ =~ /\.html/) {
      $pr_backlist .= "    <option value=\"${set::current}${set::backdir}${file}/$_\">";
      $_ =~ s/\.html//;
      $pr_backlist .= "$_</option>\n";
    }
    $i++;
  }
}
### 画像表示 #########################################################################################
use Image::Magick;
my $image = Image::Magick->new;
my $image_width;

my $pr_img; my $imgdir = $set::current.$set::imgdir;

if (!$pc{'ext_l'} && !$pc{'ext_s'}) { $image_width = 300; $pr_img = '<img src="'.$imgdir.'!none.jpg">'; }
elsif (!$pc{'ext_l'}) { $image->Read($imgdir.$pc{'file'}.'_.'.$pc{'ext_s'}); $pr_img =                                                                    '<img src="'.$imgdir.$pc{'file'}.'_.'.$pc{'ext_s'}.'" alt="キャラクタ画像">'; }
elsif (!$pc{'ext_s'}) { $image->Read($imgdir.$pc{'file'}.'_.'.$pc{'ext_l'}); $pr_img = '<a href="'.$imgdir.$pc{'file'}.'.'.$pc{'ext_l'}.'" target="_blank"><img src="'.$imgdir.$pc{'file'}.'_.'.$pc{'ext_l'}.'" alt="キャラクタ画像"></a>'; }
else                  { $image->Read($imgdir.$pc{'file'}.'_.'.$pc{'ext_s'}); $pr_img = '<a href="'.$imgdir.$pc{'file'}.'.'.$pc{'ext_l'}.'" target="_blank"><img src="'.$imgdir.$pc{'file'}.'_.'.$pc{'ext_s'}.'" alt="キャラクタ画像"></a>'; }
if(!$image_width){
  ($image_width, undef) = $image->Get('width', 'height');
}

### 表示・非表示 #####################################################################################
my $visible_memory;
foreach my $num (1..3){
  if($pc{'memory'.$num.'_name'} || $pc{'memory'.$num.'_relation'} || $pc{'memory'.$num.'_emotion'} || $pc{'memory'.$num.'_note'}){
    $visible_memory = 1;
    last;
  }
}
my $visible_effect_ez;
foreach my $num (1..$pc{'count_effect_ez'}){
  if($pc{'effect_ez'.$num.'_name'}){
    $visible_effect_ez = 1;
    last;
  }
}
my $visible_weapon;
foreach my $num (1..$pc{'count_weapon'}){
  if($pc{'weapon'.$num.'_name'}){
    $visible_weapon = 1;
    last;
  }
}
my $visible_armour;
foreach my $num (1..$pc{'count_armour'}){
  if($pc{'armour'.$num.'_name'}){
    $visible_armour = 1;
    last;
  }
}
my $visible_item;
foreach my $num (1..$pc{'count_armour'}){
  if($pc{'item'.$num.'_name'}){
    $visible_item = 1;
    last;
  }
}

### 履歴 #############################################################################################
my $pr_history;
{
  $pr_history .= <<"HTML";
<div class="table" id="History">
  <table>
  <tr>
    <th class="L" colspan="9">履歴</th>
  </tr>
  <tr class="img">
    <td colspan="6" style="border-width:1px 0;empty-cells:show;"></td>
  </tr>
  <tr>
    <th class="C" style="width:20px;">No.</th>
    <th class="C" style="width:60px;">日付</th>
    <th class="C"><div style="width:150px;margin:auto;">タイトル</div></th>
    <th class="C" style="width:3em;">経験点</th>
    <th class="C">GM</th>
    <th class="C"><div style="width:200px;margin:auto;">参加者</div></th>
  </tr>
  <tr>
    <td class="R">$blank</td>
    <td class="L">@{[ $pc{'make_date'}?$pc{'make_date'}:$blank ]}</td>
    <td class="C">キャラクター作成</td>
    <td class="C">@{[ $pc{'make_exp'}?$pc{'make_exp'}:0 ]}</td>
  </tr>
HTML
  my $hsnum = 0;
  for (my $i = 1; $i <= $pc{'count_history'}; $i++) { 
    if ($pc{"hist_date$i"}){
      if ($set::loglink && $pc{"hist_date$i"} =~ /_/){
        my $hslink = $pc{"hist_date$i"};
        $hslink =~ s/\///g; $pc{"hist_date$i"} =~ s/_[0-9]//g;
        my $hsyear = substr($hslink, 0, 4);
        $hslink =~ /[0-9]{8}(.*)_[0-9]/;
        my $room = $1;
        foreach (@set::logurl){
          if ($room eq @$_[0]) { $pc{"hist_date$i"} = '<a href="'.@$_[2].(@$_[1]?$hsyear.'/':'').$hslink.'.html">'.$pc{"hist_date$i"}.'</a>';  }
        }
      }
    } else { $pc{"hist_date$i"} = $blank; }
    if($set::pllist){
      my $num;
      $pc{"hist_name$i"} =~ s/^#([0-9]+) /$num = $1; ''/e;
      $pc{"hist_name$i"} = '<a href="'.$set::pllist.'session.cgi?page='.$num.'">#'.sprintf("%03d", $num).'</a> '.$pc{"hist_name$i"} if $num;
    }
    if ($pc{"hist_name$i"}  eq '') { $pc{"hist_name$i"}  = $blank; }
    if ($pc{"hist_exp$i"}   eq '') { $pc{"hist_exp$i"}   = $blank; }
    my $hsno = $blank; my $hsf1;
    my $hsgmsize = length($pc{"hist_gm$i"});
    if ($pc{"hist_gm$i"}) { $hsnum++; $hsno = $hsnum; } else { $pc{"hist_gm$i"} = $blank; }
    if(!$pc{"hist_member$i"}){ $pc{"hist_member$i"} = $blank }
    if($hsgmsize > 8) { $hsf1 = " f10"; }
    $pr_history .= <<"HTML";
  <tr @{[ ($i % 2 == 0) ? '' : 'class="rv"' ]}>
    <td class="R" @{[ $pc{"hist_note$i"}?'rowspan="2"':'' ]}>$hsno</td>
    <td class="L" @{[ $pc{"hist_note$i"}?'rowspan="2"':'' ]}>$pc{"hist_date$i"}</td>
    <td class="L" @{[ $pc{"hist_note$i"}?'rowspan="2"':'' ]}>$pc{"hist_name$i"}</td>
    <td class="C">$pc{"hist_exp$i"}</td>
    <td class="C$hsf1 nw">$pc{"hist_gm$i"}</td>
    <td class="L">$pc{"hist_member$i"}</td>
  </tr>
HTML
    if ($pc{"hist_note$i"}){
      my $hsbisize = length($pc{"hist_note$i"});
      my $hsf2;
      if($hsbisize > 80) { $hsf2 = " f10"; }
      $pr_history .= <<"HTML";
  <tr @{[ ($i % 2 == 0) ? '' : 'class="rv"' ]}>
    <td class="L$hsf2" colspan="5" style="padding-left:3px;">$pc{"hist_note$i"}</td>
  </tr>
HTML
    }
  }
  $pr_history .= <<"HTML";
  </table>
</div>
HTML
}
if ($pc{'text_history'}){
  $pr_history .= <<"HTML";
<div class="table" id="HistoryFree">
  <table>
  <tr><th class="L">@{[ $pc{'head_text_history'}?$pc{'head_text_history'}:'履歴' ]}</th></tr>
  <tr><td class="L">$pc{'text_history'}</td></tr>
  </table>
</div>
HTML
}

### プレイヤー名 #####################################################################################
my $player;
if($set::pllist){
  my($ID, undef) = split(/-/, $id);
  $player = '<a href="'.$set::pllist.'?mode=page&id='.$ID.'">'.$pc{'player'}.'</a>';
}
else {
  $player = '<a href="'.$set::current.$set::cgi.'?mode=list2&m=pl&g='.uri_escape_utf8($pc{'player'}).'">'.$pc{'player'}.'</a>';
}

## 
my $p_name;
if($codename_ruby || $name_ruby){
  $p_name = '<div class="name" style="margin:5px 0 -5px 0;"><table class="ruby"><tr><th>'.($codename_ruby ? $codename_ruby : '').'</th></tr>'.
            '<tr><td>'.($codename ? "“${codename}”" : '').'</td></table><table class="ruby"><tr><th>'.$name_ruby.'</th></tr><tr><td>'.$name.'</td></table></div>';
} else {
  $p_name = '<div class="name">'.($codename ? "“${codename}”" : '').$name.'</div>';
}

### 台詞 #############################################################################################
my $word_rb; my $word_rb2;
if($pc{'word'} =~ /<rb|<ruby/){ $word_rb = ' style="height:28px;vertical-align:bottom;"'; $word_rb2 = 'height:28px;padding-top:0px;'; }
elsif(!$pc{'word'}){ $pc{'word'} = $blank }
my $word_lng = $pc{'word'}; $word_lng =~ s/<("[^"]*"|'[^']*'|[^'">])*>//g;
my $wordsize = length($word_lng) ; my $p_wsize; my $j;
if ($pc{'codename_ruby'} || $pc{'name_ruby'}) { $j = 'margin:-1px 0 1px;'; }
if ($word_rb) { $j = 'margin:-2px 0 2px;'; }
if   ($wordsize > 56){ $p_wsize = ' style="'.$j.$word_rb2.'font-size:14px;line-height:12px;"' ; }
elsif($wordsize > 49 || ($word_rb && $wordsize > 43)){ $p_wsize = ' style="'.$j.$word_rb2.'font-size:14px;"' ; }
elsif($wordsize > 43 || ($word_rb && $wordsize > 39)){ $p_wsize = ' style="'.$j.$word_rb2.'font-size:16px;"' ; }
elsif($wordsize > 39 || $word_rb){ $p_wsize = ' style="'.$j.$word_rb2.'font-size:18px;"' ; }
else { $p_wsize = ' style="'.$j.'"' ; }


### タグ #############################################################################################
my $pr_tag;
if($pc{'tag'}){
  my @tags = split(/\ /, $pc{'tag'});
  foreach(@tags){
    $pr_tag .= '<a href="'.$set::current.$set::cgi.'?mode=list2&m=search_t&g='.uri_escape_utf8($_).'">'.$_.'</a>&emsp;';
  }
  $pr_tag = <<"HTML";
<div class="table" id="Tag">
  <table>
  <tr><th class="L" style="width:28px;">タグ</th><td class="L">$pr_tag</td></tr>
</table>
</div>
HTML
}

### myCSS ############################################################################################
  if($pc{'mycss'}){
    foreach('css_frame','css_font1','css_pl','css_cell1','css_cell2','css_font2','css_link'){
      $pc{$_} = uri_escape_utf8($pc{$_});
    }
  }
  $pc{'back_color'} = uri_escape_utf8($pc{'back_color'});

### ページ全体 #######################################################################################
sub pageprint {
  my $prmode = shift;
  my $output = <<"HTML";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
  @{[ $pc{'hide'} ? '<meta name="robots" content="noindex,nofollow">' : '' ]}
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta http-equiv="Cache-Control" content="no-cache">
  <meta http-equiv="Expires" content="0">
HTML
my $cssurl = ''.$set::css_cgi.'?id='.$pc{'CSS'}.'&rad='.$pc{'css_radius'}.
   ($pc{'mycss'} ? '&fb='.$pc{'css_frame'}.'&ft='.$pc{'css_font1'}.'&fl='.$pc{'css_pl'}.'&cb1='.$pc{'css_cell1'}.'&cb2='.$pc{'css_cell2'}.'&ct='.$pc{'css_font2'}.'&cl='.$pc{'css_link'} : '').
   ($pc{'ext_b'} ? '&bi='.$file.'_back.'.$pc{'ext_b'}.'&bi_pox='.$pc{'back_position_x'}.'&bi_poy='.$pc{'back_position_y'}.'&bi_re='.$pc{'back_repeat'} : '').
   '&bc='.$pc{'back_color'};
if($prmode eq 'backup'){
  $output .= <<"HTML";
  <link rel="stylesheet" type="text/css" href="../../$set::css_base">
  <link rel="stylesheet" type="text/css" href="../../$cssurl">
HTML
} else {
  $output .= <<"HTML";
  <link rel="stylesheet" type="text/css" href="../$set::css_base">
  <link rel="stylesheet" type="text/css" href="../$cssurl">
HTML
}
  $output .= <<"HTML";
  <title>@{[ !$name && $codename ? "“${codename}”" : $name ]} － $set::title</title>
</head>
<body>
<div id="base">
<div id="header"><h1>$set::title</h1></div>
HTML
if($prmode ne 'backup'){
  $output .= <<"HTML";
<div id="sub">
<h1>
  <form method="post" action="${set::current}${set::cgi}">
  [ <a href="$set::backurl">TOP</a> ] &nbsp;
  [ <input type="hidden" name="mode" value="edit"><input type="hidden" name="id" value="${id}"> pass:<input type="password" name="pass" style="width:80px;">　<input type="submit" name="pchecck" value=" edit "> ]
  </form>
</h1>
</div>
HTML
}
  $output .= <<"HTML";
<select onchange="location.href = this.options[selectedIndex].value" id="BackUpList">
    <option>backup</option>
$pr_backlist
</select>

<div class="cent">

<div class="table" id="Summary">
  <tbody>
    <table border="1" >
      <tr>
        <td rowspan=3 width="300px">
          $pr_img
        </td>
        <th colspan=2>$p_name</th>
      </tr>
      <tr>
        <td colspan=2><div class="word"$p_wsize>$pc{'word'}</div></td>
      </tr>
      <tr>
        <td class="L other" width="50%">
            $pc{'text_free'}
        </td>
        <td class="L other" width="50%">
          性別：$pc{'prof_sex'}　年齢：$pc{'prof_age'}<br>
HTML
  if ($pc{'hide_syndrome'}) {
    $output .= "ブリード：不明<br>";
    $output .= "シンドローム：不明";
  } else {
    $output .= "ブリード：$breed<br>";
    $output .= "シンドローム：$pc{'syndrome1'}";
    $output .= "／" . $pc{'syndrome2'} if $pc{'syndrome2'};
    $output .= "／" . $pc{'syndrome3'} if $pc{'syndrome3'};
  }
  $output .= <<"HTML";
<br>
          ワークス／カヴァー：$pc{'works'}／$pc{'cover'}<br>
HTML
  if ($pc{'hide_stt'}) {
    $output .= "【肉体】不明 <br>";
    $output .= "【感覚】不明 <br>";
    $output .= "【精神】不明 <br>";
    $output .= "【社会】不明 ";
  } else {
    $output .= "【肉体】$stt_body ";
    $output .= "〈白兵〉$pc{'skill_fight_lv'} " if $pc{'skill_fight_lv'};
    $output .= "〈回避〉$pc{'skill_dodge_lv'} " if $pc{'skill_dodge_lv'};
    $output .= "〈運転:$pc{'skill_drive1_name'}〉$pc{'skill_drive1_lv'} " if $pc{'skill_drive1_lv'};
    $output .= "他" if $pc{'skill_drive2_lv'};
    $output .= "<br>" ;
    $output .= "【感覚】$stt_sense ";
    $output .= "〈射撃〉$pc{'skill_shoot_lv'} " if $pc{'skill_shoot_lv'};
    $output .= "〈知覚〉$pc{'skill_perce_lv'} " if $pc{'skill_perce_lv'};
    $output .= "〈芸術:$pc{'skill_art1_name'}〉$pc{'skill_art1_lv'} " if $pc{'skill_art1_lv'};
    $output .= "他" if $pc{'skill_art2_lv'};
    $output .= "<br>" ;
    $output .= "【精神】$stt_spirit ";
    $output .= "〈RC〉$pc{'skill_RC_lv'} " if $pc{'skill_RC_lv'};
    $output .= "〈意志〉$pc{'skill_will_lv'} " if $pc{'skill_will_lv'};
    $output .= "〈知識:$pc{'skill_know1_name'}〉$pc{'skill_know1_lv'} " if $pc{'skill_know1_name'};
    $output .= "他" if $pc{'skill_know2_lv'};
    $output .= "<br>" ;
    $output .= "【社会】$stt_social ";
    $output .= "〈交渉〉$pc{'skill_nego_lv'} " if $pc{'skill_nego_lv'};
    $output .= "〈調達〉$pc{'skill_raise_lv'} " if $pc{'skill_raise_lv'};
    $output .= "〈情報:$pc{'skill_info1_name'}〉$pc{'skill_info1_lv'} " if $pc{'skill_info1_lv'};
    $output .= "他" if $pc{'skill_info2_lv'};
  }
  $output .= "<br>" ;
  if ($pc{'hide_hpmax'}) {
    $output .= "【HP】不明 ";
  } else {
    $output .= "【HP】$hpmax ";
  }
  if ($pc{'hide_speed'}) {
    $output .= "【行動値】不明 ";
  } else {
    $output .= "【行動値】$speed ";
  }
  if ($pc{'hide_urge_current'}) {
    $output .= "侵蝕率：不明 ";
  } else {
    $output .= "侵蝕率：$pc{'urge_current'}％";
  }
  $output .= <<"HTML";
<br>
          エフェクト：<br>
HTML
  if ($pc{'hide_effect'}) {
  $output .= "不明";
  } else {
    foreach my $num (1..$pc{'count_effect'}){
      next if !$pc{'effect'.$num.'_name'};
      $output .= <<"HTML";
          《$pc{'effect'.$num.'_name'}》$pc{'effect'.$num.'_lv'}、
HTML
      last if $num >= 3;
    }
  }
$output .= <<"HTML";
          他
        </td>
      </tr>
    </table>
  </tbody>
</div>

<div id="hide_description">
<p><input type="button" value="詳細を表示する" style="WIDTH:150px"
   onClick="document.getElementById('description').style.display='block';
            document.getElementById('hide_description').style.display='none'"></p>
</div>
<div id="description" style="display:none">
<p><input type="button" value="詳細を隠す" style="WIDTH:150px"
   onClick="document.getElementById('description').style.display='none';
            document.getElementById('hide_description').style.display='block'"></p>
<p>

<div class="table" id="Title">
  <table>
  <tr>
    <th colspan="2"><div class="word"$p_wsize>$pc{'word'}</div></th>
  </tr>
  <tr>
    <th>
      $p_name
    </th>
    <th style="padding:0px 0px 3px 0px;text-align:right;vertical-align:bottom;font-size:12px;line-height:14px;" nowrap>@{[ ($prmode eq 'backup')?'バックアップ':'最終更新' ]}：$lastupdate<br>プレイヤー：$player</th>
  </tr>
  </table>
</div>

@{[ $set::tag_position ? $pr_tag : '' ]}

<div id="CharaR">
<div class="table" id="Image">
  <div class="img"><table class="imgw" style="max-width:@{[ $image_width + 2 ]}px;"><tr><td>$pr_img</td></tr></table></div>
</div>
</div>

<div id="CharaL">
<div class="table" id="Profile">
  <colgroup>
    <col style="width:33.33%;"><col>
    <col style="width:33.33%;"><col>
    <col style="width:33.33%;">
  </colgroup>
  <table>
  <tr>
    <th class="L">年齢</th>
    <th rowspan="4" class="line"></th>
    <th class="L">性別</th>
    <th rowspan="4" class="line"></th>
    <th class="L">星座</th>
  </tr>
  <tr>
    <td class="C">$pc{'prof_age'}</td>
    <td class="C">$pc{'prof_sex'}</td>
    <td class="C">$pc{'prof_sign'}</td>
  </tr>
  <tr>
    <th class="L">身長</th>
    <th class="L">体重</th>
    <th class="L">血液型</th>
  </tr>
  <tr class="rv">
    <td class="C">$pc{'prof_height'}</td>
    <td class="C">$pc{'prof_weight'}</td>
    <td class="C">$pc{'prof_blood'}</td>
  </tr>
  </table>
</div>

<div class="table" id="WandC">
  <table>
  <tr><th class="L">ワークス</th></tr>
  <tr><td class="C">$pc{'works'}</td></tr>
  <tr><th class="L">カヴァー</th></tr>
  <tr class="rv"><td class="C">$pc{'cover'}</td></tr>
  </table>
</div>

<div class="table" id="Syndrome">
  <table>
  <tr>
    <th class="L" style="width:21%;">ブリード</th>
    <th rowspan="2" class="line"></th>
    <th class="L">シンドローム</th>
    <th class="L"></th>
    <th class="L" style="font-size:82%;">オプショナル</th>
  </tr>
  <tr>
    <td class="C">$breed</td>
    <td class="C">$pc{'syndrome1'}</td>
    <td class="C">$pc{'syndrome2'}</td>
    <td class="C">$pc{'syndrome3'}</td>
  </tr>
  </table>
</div>

<div class="table" id="Exp">
  <table>
  <tr><th class="L">経験点</th></tr>
  <tr><td class="C">$pc{'exp'}</td></tr>
  <tr><th class="L">消費経験点</th></tr>
  <tr class="rv"><td class="C">$exp_use</td></tr>
  </table>
</div>

<div class="table" id="Spec">
  <table>
  <tr>
    <th class="L">HP最大値</th>
    <th rowspan="4" class="line"></th>
    <th class="L">常備化ポイント</th>
    <th rowspan="4" class="line"></th>
    <th class="L">財産ポイント</th>
  </tr>
  <tr>
    <td class="C">@{[ $pc{'sub_hp_add'} ? "+$pc{'sub_hp_add'}=" : '' ]}<b>$hpmax</b></td>
    <td class="C">@{[ $pc{'sub_provide_add'} ? "+$pc{'sub_provide_add'}=" : '' ]}<b>$provide</b></td>
    <td class="C"><b>$money</b></td>
  </tr>
  <tr>
    <th class="L">行動値</th>
    <th class="L">戦闘移動</th>
    <th class="L">全力移動</th>
  </tr>
  <tr class="rv">
    <td class="C">@{[ $pc{'sub_speed_add'} ? "+$pc{'sub_speed_add'}=" : '' ]}<b>$speed</b></td>
    <td class="C">@{[ $pc{'sub_move_add'} ? "+$pc{'sub_move_add'}=" : '' ]}<b>$move</b></td>
    <td class="C"><b>$fullmove</b></td>
  </tr>
  </table>
</div>

<div class="table" id="Lifepath">
  <table>
  <colgroup>
    <col style="width:6em;">
    <col style="width:4em;">
    <col>
  </colgroup>
  <caption>ライフパス</caption>
  <tr><td class="horizon" colspan="3"></td></tr>
  <tr>
    <th class="L">出自</th>
  </tr>
  <tr>
    <td class="C" colspan="2">@{[ $pc{'lifepath_birth'} ? $pc{'lifepath_birth'} : '&nbsp;' ]}</td>
    <td class="L">$pc{'lifepath_birth_note'}</td>
  </tr>
  <tr>
    <th class="L">経験</th>
  </tr>
  <tr class="rv">
    <td class="C" colspan="2">@{[ $pc{'lifepath_exp'} ? $pc{'lifepath_exp'} : '&nbsp;' ]}</td>
    <td class="L">$pc{'lifepath_exp_note'}</td>
  </tr>
  <tr>
    <th class="L">邂逅・欲望</th>
  </tr>
  <tr>
    <td class="C" colspan="2">@{[ $pc{'lifepath_meet'} ? $pc{'lifepath_meet'} : '&nbsp;' ]}</td>
    <td class="L">$pc{'lifepath_meet_note'}</td>
  </tr>
  <tr>
    <th class="L">覚醒</th>
    <th class="C">侵蝕値</th>
  </tr>
  <tr class="rv">
    <td class="C">$pc{'lifepath_awaken'}</td>
    <td class="C">$pc{'lifepath_awaken_invade'}</td>
    <td class="L">$pc{'lifepath_awaken_note'}</td>
  </tr>
  <tr>
    <th class="L">衝動</th>
    <th class="C">侵蝕値</th>
  </tr>
  <tr>
    <td class="C">$pc{'lifepath_urge'}</td>
    <td class="C">$pc{'lifepath_urge_invade'}</td>
    <td class="L">$pc{'lifepath_urge_note'}</td>
  </tr>
  <tr>
    <th></th>
    <th class="L" colspan="2" style="text-indent:-1em;">その他の修正</th>
  </tr>
  <tr class="rv">
    <th></th>
    <td class="C">@{[ $pc{'lifepath_other_invade'} ? $pc{'lifepath_other_invade'} : 0 ]}</td>
    <td class="L">$pc{'lifepath_other_note'}</td>
  </tr>
  <tr>
    <th></th>
    <th class="L" colspan="2" style="text-indent:-.5em;">基本侵蝕値</th>
  </tr>
  <tr>
    <th></th>
    <td class="C B">$stt_invade</td>
  </tr>
  </table>
</div>
</div>

<div style="clear:both;padding-bottom:3px;"></div>

<div class="table" id="Skill">
  <table>
  <caption>能力値</caption>
  <colgroup>
    <col><col style="width:45px;">
    <col><col style="width:45px;">
    <col><col style="width:45px;">
    <col><col style="width:45px;">
  </colgroup>
  <tr><td class="horizon" colspan="8"></td></tr>
  <tr>
    <th class="C">肉体</th>
    <td class="C B">$stt_body</td>
    <th class="C">感覚</th>
    <td class="C B">$stt_sense</td>
    <th class="C">精神</th>
    <td class="C B">$stt_spirit</td>
    <th class="C">社会</th>
    <td class="C B">$stt_social</td>
  </tr>
  <tr>
    <td class="L">白兵</td>
    <td class="R"><b>$pc{'skill_fight_lv'}</b>Lv</td>
    <td class="L">射撃</td>
    <td class="R"><b>$pc{'skill_shoot_lv'}</b>Lv</td>
    <td class="L" style="letter-spacing:.4em;">RC</td>
    <td class="R"><b>$pc{'skill_RC_lv'}</b>Lv</td>
    <td class="L">交渉</td>
    <td class="R"><b>$pc{'skill_nego_lv'}</b>Lv</td>
  </tr>
  <tr class="rv">
    <td class="L">回避</td>
    <td class="R"><b>$pc{'skill_dodge_lv'}</b>Lv</td>
    <td class="L">知覚</td>
    <td class="R"><b>$pc{'skill_perce_lv'}</b>Lv</td>
    <td class="L">意志</td>
    <td class="R"><b>$pc{'skill_will_lv'}</b>Lv</td>
    <td class="L">調達</td>
    <td class="R"><b>$pc{'skill_raise_lv'}</b>Lv</td>
  </tr>
HTML
foreach my $num (1..$pc{'count_skill'}){
  $output .= <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="L">運転：$pc{'skill_drive'.$num.'_name'}</td>
    <td class="R"><b>$pc{'skill_drive'.$num.'_lv'}</b>Lv</td>
    <td class="L">芸術：$pc{'skill_art'.$num.'_name'}</td>
    <td class="R"><b>$pc{'skill_art'.$num.'_lv'}</b>Lv</td>
    <td class="L">知識：$pc{'skill_know'.$num.'_name'}</td>
    <td class="R"><b>$pc{'skill_know'.$num.'_lv'}</b>Lv</td>
    <td class="L">情報：$pc{'skill_info'.$num.'_name'}</td>
    <td class="R"><b>$pc{'skill_info'.$num.'_lv'}</b>Lv</td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="Lois">
  <table>
  <caption>ロイス</caption>
  <colgroup>
    <col style="width:6em;">
    <col style="width:14em;">
    <col style="width:5em;">
    <col style="width:5em;">
    <col>
    <col style="width:1.6em;">
  </colgroup>
  <tr><td class="horizon" colspan="6"></td></tr>
  <tr>
    <th class="L">関係</th>
    <th class="L">名前</th>
    <th class="L">感情:Posi</th>
    <th class="L">感情:Nega</th>
    <th class="R" colspan="2">タイタス</th>
  </tr>
HTML
foreach my $num (1..7){
  $output .= <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C">$pc{'lois'.$num.'_relation'}</td>
    <td class="C B">$pc{'lois'.$num.'_name'}</td>
    <td class="L"><input type="checkbox" @{[ $pc{'lois'.$num.'_check'} eq 'P'?'checked':'' ]} onClick="return false">$pc{'lois'.$num.'_positive'}</td>
    <td class="L"><input type="checkbox" @{[ $pc{'lois'.$num.'_check'} eq 'N'?'checked':'' ]} onClick="return false">$pc{'lois'.$num.'_negative'}</td>
    <td class="L bbR">$pc{'lois'.$num.'_note'}</td>
    <td class="C bbL"><input type="checkbox" $pc{'lois'.$num.'_titus'} onClick="return false"></td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="Memory" @{[ $visible_memory ? '' : 'style="display:none;"' ]}>
  <table>
  <caption>メモリー</caption>
  <colgroup>
    <col style="width:6em;">
    <col style="width:14em;">
    <col style="width:4em;">
    <col>
  </colgroup>
  <tr><td class="horizon" colspan="4"></td></tr>
  <tr>
    <th class="L">関係</th>
    <th class="L">名前</th>
    <th class="L">感情</th>
    <th class="L">備考</th>
  </tr>
  <tr>
  </tr>
HTML
foreach my $num (1..3){
  $output .= <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C">$pc{'memory'.$num.'_relation'}</td>
    <td class="C B">$pc{'memory'.$num.'_name'}</td>
    <td class="C">$pc{'memory'.$num.'_emotion'}</td>
    <td class="L">$pc{'memory'.$num.'_note'}</td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="Effect">
  <table>
  <caption>エフェクト</caption>
  <colgroup>
    <col style="width:2em;">
    <col>
    <col style="width:2em;">
    <col style="width:15.5%;">
    <col style="width:13%;">
    <col style="width:4.5em;">
    <col style="width:10.7%;">
    <col style="width:4em;">
    <col style="width:3.8em;">
    <col style="width:7.6%;">
  </colgroup>
  <tr><td class="horizon" colspan="10"></td></tr>
  <tr>
    <th class="C">No.</th>
    <th class="C">名称</th>
    <th class="C lv">Lv</th>
    <th class="C">タイミング</th>
    <th class="C">技能</th>
    <th class="C">難易度</th>
    <th class="C">対象</th>
    <th class="C">射程</th>
    <th class="C">侵蝕値</th>
    <th class="C">制限</th>
  </tr>
  <tr>
    <td class="C B" rowspan="2">―</td>
    <td class="C B">リザレクト</td>
    <td class="C lv">1</td>
    <td class="C">オートアクション</td>
    <td class="C">―</td>
    <td class="C">自動成功</td>
    <td class="C">自身</td>
    <td class="C">至近</td>
    <td class="C"><small>効果参照</small></td>
    <td class="C">―</td>
  </tr>
  <tr><td class="L" colspan="9">(Lv)D点HP回復、侵蝕値上昇</td></tr>
  <tr class="rv">
    <td class="C B" rowspan="2">―</td>
    <td class="C B">ワーディング</td>
    <td class="C lv">1</td>
    <td class="C">オートアクション</td>
    <td class="C">―</td>
    <td class="C">自動成功</td>
    <td class="C">シーン</td>
    <td class="C">視界</td>
    <td class="C">0</td>
    <td class="C">―</td>
  </tr><tr class="rv"><td class="L" colspan="9">非オーヴァードをエキストラ化</td></tr>
HTML
foreach my $num (1..$pc{'count_effect'}){
  next if !$pc{'effect'.$num.'_name'};
  $output .= <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C B" rowspan="2">$num</td>
    <td class="C B">$pc{'effect'.$num.'_name'}</td>
    <td class="C lv">$pc{'effect'.$num.'_lv'}</td>
    <td class="C">$pc{'effect'.$num.'_timing'}</td>
    <td class="C">$pc{'effect'.$num.'_skill'}</td>
    <td class="C">$pc{'effect'.$num.'_diffi'}</td>
    <td class="C">$pc{'effect'.$num.'_target'}</td>
    <td class="C">$pc{'effect'.$num.'_range'}</td>
    <td class="C">$pc{'effect'.$num.'_point'}</td>
    <td class="C">$pc{'effect'.$num.'_limit'}</td>
  </tr><tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}><td class="L" colspan="9">$pc{'effect'.$num.'_note'}</td></tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="EffectEz" @{[ $visible_effect_ez ? '' : 'style="display:none;"' ]}>
  <table>
  <caption>イージーエフェクト</caption>
  <colgroup>
    <col style="width:2em;">
    <col>
    <col style="width:2em;">
    <col style="width:15.5%;">
    <col style="width:13%;">
    <col style="width:4.5em;">
    <col style="width:10.7%;">
    <col style="width:4em;">
    <col style="width:3.8em;">
    <col style="width:7.6%;">
  </colgroup>
  <tr><td class="horizon" colspan="10"></td></tr>
  <tr>
    <th class="C">No.</th>
    <th class="C">名称</th>
    <th class="C lv">Lv</th>
    <th class="C">タイミング</th>
    <th class="C">技能</th>
    <th class="C">難易度</th>
    <th class="C">対象</th>
    <th class="C">射程</th>
    <th class="C">侵蝕値</th>
    <th class="C">制限</th>
  </tr>
HTML
foreach my $num (1..$pc{'count_effect_ez'}){
  next if !$pc{'effect_ez'.$num.'_name'};
  $output .= <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C B" rowspan="2">$num</td>
    <td class="C B">$pc{'effect_ez'.$num.'_name'}</td>
    <td class="C lv">$pc{'effect_ez'.$num.'_lv'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_timing'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_skill'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_diffi'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_target'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_range'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_point'}</td>
    <td class="C">$pc{'effect_ez'.$num.'_limit'}</td>
  </tr><tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}><td class="L" colspan="9">$pc{'effect_ez'.$num.'_note'}</td></tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="Combo">
  <table>
  <caption>コンボデータ</caption>
  <colgroup>
    <col>
    <col style="width:13%;">
    <col style="width:4.5em;">
    <col style="width:10.7%;">
    <col style="width:7.8%;">
    <col style="width:4.9em;">
    <col style="width:7.8%;">
    <col style="width:7.8%;">
    <col style="width:7.8%;">
    <col style="width:3.8em;">
  </colgroup>
HTML
foreach my $num (1..$pc{'count_combo'}){
  next if !$pc{'combo'.$num.'_name'};
  $output .= <<"HTML";
  <tr><td class="horizon" colspan="10"></td></tr>
  <tr><td class="horizonB"></td></tr>
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C B" rowspan="2" colspan="2">$pc{'combo'.$num.'_name'}</td>
    <th class="C" colspan="8">組み合わせ</th>
  </tr>
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C" colspan="8">$pc{'combo'.$num.'_set'}</td>
  </tr>
  <tr>
    <th class="C">タイミング</th>
    <th class="C">技能</th>
    <th class="C">難易度</th>
    <th class="C">対象</th>
    <th class="C">射程</th>
    <th class="C">条件</th>
    <th class="C">ダイス</th>
    <th class="C"><small>クリティカル</small></th>
    <th class="C">攻撃力</th>
    <th class="C">侵蝕値</th>
  </tr>
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C" rowspan="2">$pc{'combo'.$num.'_timing'}</td>
    <td class="C" rowspan="2">$pc{'combo'.$num.'_skill'}</td>
    <td class="C" rowspan="2">$pc{'combo'.$num.'_diffi'}</td>
    <td class="C" rowspan="2">$pc{'combo'.$num.'_target'}</td>
    <td class="C" rowspan="2">$pc{'combo'.$num.'_range'}</td>
    <th class="C f11">100%未満</th>
    <td class="C num">$pc{'combo'.$num.'_under_dice'}</td>
    <td class="C num">$pc{'combo'.$num.'_under_crit'}</td>
    <td class="C num">$pc{'combo'.$num.'_under_power'}</td>
    <td class="C num" rowspan="2">$pc{'combo'.$num.'_point'}</td>
  </tr>
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <th class="C f11">100%以上</th>
    <td class="C num">$pc{'combo'.$num.'_over_dice'}</td>
    <td class="C num">$pc{'combo'.$num.'_over_crit'}</td>
    <td class="C num">$pc{'combo'.$num.'_over_power'}</td>
  </tr>
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}><td class="L" colspan="10">$pc{'combo'.$num.'_note'}</td></tr>
  <tr><td class="horizonB"></td></tr>
HTML
}
$output .= <<"HTML";
  </table>
</div>

<div class="table" id="Item" @{[ $visible_weapon || $visible_armour || $visible_item ? '' : 'style="display:none;"' ]}>
  <table>
  <caption>アイテム</caption>
  <colgroup>
    <col style="width:23%;">
    <col style="width:3.5em;">
    <col style="width:3.5em;">
    <col style="width:8%;">
    <col style="width:10%;">
    <col style="width:3.4em;">
    <col style="width:3.4em;">
    <col style="width:3.4em;">
    <col style="width:3.4em;">
    <col>
  </colgroup>
  <tr><td class="horizon" colspan="10"></td></tr>
  <tr @{[ $visible_weapon ? '' : 'style="display:none;"' ]}>
    <th class="C">武器</th>
    <th class="C">常備化</th>
    <th class="C">経験点</th>
    <th class="C">種別</th>
    <th class="C">技能</th>
    <th class="C">命中</th>
    <th class="C">攻撃力</th>
    <th class="C"><small>ガード値</small></th>
    <th class="C">射程</th>
    <th class="L" style="text-indent:1em">解説</th>
  </tr>
HTML
foreach my $num (1..$pc{'count_weapon'}){
  next if !$pc{'weapon'.$num.'_name'};
  $output .= <<"HTML";
  <tr>
    <td class="B">$pc{'weapon'.$num.'_name'}</td>
    <td class="C">$pc{'weapon'.$num.'_point'}</td>
    <td class="C">$pc{'weapon'.$num.'_exp'}</td>
    <td class="C">$pc{'weapon'.$num.'_type'}</td>
    <td class="C">$pc{'weapon'.$num.'_skill'}</td>
    <td class="C">$pc{'weapon'.$num.'_hit'}</td>
    <td class="C">$pc{'weapon'.$num.'_power'}</td>
    <td class="C">$pc{'weapon'.$num.'_guard'}</td>
    <td class="C">$pc{'weapon'.$num.'_range'}</td>
    <td class="L">$pc{'weapon'.$num.'_note'}</td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>
  
  <table @{[ $visible_armour ? '' : 'style="display:none;"' ]}>
  <colgroup>
    <col style="width:23%;">
    <col style="width:3.5em;">
    <col style="width:3.5em;">
    <col style="width:8%;">
    <col style="width:10%;">
    <col style="width:3.4em;">
    <col style="width:3.4em;">
    <col style="width:3.4em;">
    <col>
  </colgroup>
  <tr><td class="horizonB" colspan="8"></td></tr>
  <tr>
    <th class="C">防具</th>
    <th class="C">常備化</th>
    <th class="C">経験点</th>
    <th class="C">種別</th>
    <th class="C"></th>
    <th class="C">ドッジ</th>
    <th class="C">行動</th>
    <th class="C">装甲値</th>
    <th class="L" style="text-indent:1em">解説</th>
  </tr>
HTML
foreach my $num (1..$pc{'count_armour'}){
  next if !$pc{'armour'.$num.'_name'};
  $output .= <<"HTML";
  <tr>
    <td class="B">$pc{'armour'.$num.'_name'}</td>
    <td class="C">$pc{'armour'.$num.'_point'}</td>
    <td class="C">$pc{'armour'.$num.'_exp'}</td>
    <td class="C">$pc{'armour'.$num.'_type'}</td>
    <th class="C"></th>
    <td class="C">$pc{'armour'.$num.'_dodge'}</td>
    <td class="C">$pc{'armour'.$num.'_speed'}</td>
    <td class="C">$pc{'armour'.$num.'_guard'}</td>
    <td class="L">$pc{'armour'.$num.'_note'}</td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>

  <table @{[ $visible_item ? '' : 'style="display:none;"' ]}>
  <colgroup>
    <col style="width:23%;">
    <col style="width:3.5em;">
    <col style="width:3.5em;">
    <col style="width:8%;">
    <col style="width:10%;">
    <col>
  </colgroup>
  <tr><td class="horizonB" colspan="6"></td></tr>
  <tr>
    <th class="C">一般アイテム</th>
    <th class="C">常備化</th>
    <th class="C">経験点</th>
    <th class="C">種別</th>
    <th class="C">技能</th>
    <th class="L" style="text-indent:1em">解説</th>
  </tr>
HTML
foreach my $num (1..$pc{'count_item'}){
  next if !$pc{'item'.$num.'_name'};
  $output .= <<"HTML";
  <tr>
    <td class="B">$pc{'item'.$num.'_name'}</td>
    <td class="C">$pc{'item'.$num.'_point'}</td>
    <td class="C">$pc{'item'.$num.'_exp'}</td>
    <td class="C">$pc{'item'.$num.'_type'}</td>
    <td class="C">$pc{'item'.$num.'_skill'}</td>
    <td class="L">$pc{'item'.$num.'_note'}</td>
  </tr>
HTML
}
$output .= <<"HTML";
  </table>
  
  <table>
  <colgroup>
    <col style="width:23%;">
    <col style="width:3.5em;">
    <col style="width:3.5em;">
    <col>
  </colgroup>
  <tr><td class="horizonB" colspan="4"></td></tr>
  <tr><td class="horizon" colspan="4"></td></tr>
  <tr>
    <th class="R" style="padding-right:1em">常備化合計</th>
    <td class="C">$item_total_point</td>
    <th></th>
    <th></th>
  </tr>
  </table>
</div>

<div class="table" id="FreeArea" @{[ $pc{'text_free'} ? '' : 'style="display:none;"' ]}>
  <table>
    <tr><th class="L">設定・その他メモ</th></tr>
    <tr><td class="L">$pc{'text_free'}</td></tr>
  </table>
</div>

$pr_history

<div class="table" id="HistoryFree" @{[ $pc{'text_history'} ? '' : 'style="display:none;"' ]}>
  <table>
    <tr><th class="L">履歴</th></tr>
    <tr><td class="L">$pc{'text_history'}</td></tr>
  </table>
</div>

@{[ !$set::tag_position ? $pr_tag : '' ]}

<div Style="clear:both;"></div>

</div>
</div>
<a href="#header" class="backurl">▲ページの先頭へ</a>
<div id="footer">
  「ダブルクロス The 3rd Edition」は矢野俊策及び有限会社F.E.A.R.の著作物です。<br>
  　ゆとシート for DX3rd ver.$ver - <a href="http://yutorize.2-d.jp/">ゆとらいず工房</a>
</div>
</body>
</html>
HTML
  
  return $output;
}

### ページ出力 #######################################################################################
sysopen (my $OUT, "${set::datadir}${file}.html", O_WRONLY | O_TRUNC | O_CREAT, 0666);
print $OUT &pageprint;
close($OUT);

### バックアップ作成 #################################################################################
my $date;
if ($set::backuponoff eq "1" ){
  $date = sprintf("%04d%02d%02d",$year,$mon,$day);

  sysopen (my $OUT, "${set::backdir}${file}/${date}.html", O_WRONLY | O_TRUNC | O_CREAT, 0666);
  print $OUT &pageprint('backup');
  close($OUT);
}

######################################################################################################
if($mode eq 'make'){
  my $url = url();
     $url =~ s/[\/][^\/]*$//g;
  my $dir = $set::datadir;
     $dir =~ s/^\.\///;
  my $text = <<"TXT";
キャラクターデータが登録されました。
名前：$pc{'name'}
ID　：$id
URL ：${url}/${dir}${file}.html
TXT
  &sendmail($pc{'mail'}, $set::title.' : 新規登録', $text);

  if ($set::notice) {
    my $text = <<"TXT";
$pc{'player'}さんがキャラクターデータを登録しました。
名前：$pc{'name'}
ID　：$id
URL ：${url}/${dir}${file}.html
TXT
    &sendmail($set::admimail, $set::title.' : 新規登録', $text);
  }
}

our $save_message;
if($mode ne 'make'){
  $save_message = <<"HTML";
データを更新しました。<br>
⇒
<form name="page_jump1" method="post" action="${set::cgi}" style="display:inline;" target="_self">
<input type="hidden" name="page" value="$file">
<input type="submit" value="更新したシートへ移動" class="link">
</form>
<form name="page_jump2" method="post" action="${set::cgi}" style="display:inline;">
<input type="submit" value="（新しいウィンドウで開く）" class="link">
<input type="hidden" name="page" value="$file">
</form>
<br>
⇒
<a href="${set::cgi}" target="_self">一覧へ戻る</a>
HTML
  require $set::lib_edit; exit;
}
else { print "Location: ${set::datadir}${file}.html\n\n"; }
1;
#!/usr/local/bin/perl
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use CGI qw/:cgi/;
use CGI::Carp qw(fatalsToBrowser);

my $id = param('id');

require './config.cgi';
require './colorset.cgi';

my (
  $frame_bg,
  $frame_text,
  $frame_outside,
  $frame_inside,
  $cell_bg1,
  $cell_bg2,
  $cell_text,
  $link1_link,
  $link1_link_bg,
  $link1_hover,
  $link1_hover_bg,
  $link2_link,
  $link2_hover,
  $link2_hover_bg,
  $hr_solid,
  $hr_groove1,
  $hr_ridge1,
  $hr_groove2,
  $hr_ridge2,
  $table_border,
  $th_bg,
  $th_text,
  $td_bg,
  $td_text,
  $head2_bg,
  $head2_border,
  $head2_text,
  $head3_bg,
  $head3_border,
  $head3_text,
);

sub colorset {
  my $id = $_[0];
  if($id){
    $frame_bg      = $set::color{$id}{'frame'}{'back'};
    $frame_text    = $set::color{$id}{'frame'}{'text'};
    $frame_outside = $set::color{$id}{'frame'}{'out'};
    $frame_inside  = $set::color{$id}{'frame'}{'in'};
    $link2_link    = $set::color{$id}{'frame'}{'link'};
    $link2_hover   = $set::color{$id}{'frame'}{'link_hover'};
    $link2_hover_bg= $set::color{$id}{'frame'}{'link_hover_back'};
    $cell_bg1      = $set::color{$id}{'cell'}{'back1'};
    $cell_bg2      = $set::color{$id}{'cell'}{'back2'};
    $cell_text     = $set::color{$id}{'cell'}{'text'};
    $link1_link    = $set::color{$id}{'cell'}{'link'};
    $link1_link_bg = $set::color{$id}{'cell'}{'link_back'};
    $link1_hover   = $set::color{$id}{'cell'}{'link_hover'};
    $link1_hover_bg= $set::color{$id}{'cell'}{'link_hover_back'};
    $hr_solid    = $set::color{$id}{'hr'}{'solid'};
    $hr_groove1  = $set::color{$id}{'hr'}{'groove1'};
    $hr_ridge1   = $set::color{$id}{'hr'}{'ridge1'};
    $hr_groove2  = $set::color{$id}{'hr'}{'groove2'};
    $hr_ridge2   = $set::color{$id}{'hr'}{'ridge2'};
    $table_border= $set::color{$id}{'table'}{'border'};
    $th_bg       = $set::color{$id}{'table'}{'th_back'};
    $th_text     = $set::color{$id}{'table'}{'th_text'};
    $td_bg       = $set::color{$id}{'table'}{'td_back'};
    $td_text     = $set::color{$id}{'table'}{'td_text'};
    $head2_bg    = $set::color{$id}{'h2'}{'back'};
    $head2_border= $set::color{$id}{'h2'}{'border'};
    $head2_text  = $set::color{$id}{'h2'}{'text'};
    $head3_bg    = $set::color{$id}{'h3'}{'back'};
    $head3_border= $set::color{$id}{'h3'}{'border'};
    $head3_text  = $set::color{$id}{'h3'}{'text'};
  }
  if(param('fb')) { $frame_bg   = param('fb'); }
  if(param('ft')) { $frame_text = param('ft'); }
  if(param('fl')) { $link2_link = param('fl'); }
  if(param('cb1')){ $cell_bg1   = param('cb1'); }
  if(param('cb2')){ $cell_bg2   = param('cb2'); }
  if(param('ct')) { $cell_text  = param('ct'); }
  if(param('cl')) { $link1_link = param('cl'); }

  {
    if(!$frame_bg) { $frame_bg = '#555555'; }
    my($re, $gr, $bl) = apart($frame_bg);
    my $luminance = ( $re * 0.3 + $gr * 0.60 + $bl * 0.1 );
    if(!$frame_text) { $frame_text = ( $luminance > 150 ? '#000000' : '#dddddd' ); }
    if(!$frame_outside || !$frame_inside) {
      my $rel = $re + 51; if($rel > 255){ $rel = 255; }
      my $grl = $gr + 51; if($grl > 255){ $grl = 255; }
      my $bll = $bl + 51; if($bll > 255){ $bll = 255; }
      my $red = $re - 51; if($red < 0)  { $red = 0; }
      my $grd = $gr - 51; if($grd < 0)  { $grd = 0; }
      my $bld = $bl - 51; if($bld < 0)  { $bld = 0; }
      my $css_light = sprintf("#%02x%02x%02x",$rel,$grl,$bll);
      my $css_dark  = sprintf("#%02x%02x%02x",$red,$grd,$bld);
      if(!$frame_outside){ $frame_outside = "$css_light $css_dark $css_dark $css_light"; }
      if(!$frame_inside) { $frame_inside  = "$css_dark $css_light $css_light $css_dark"; }
    }
    if(!$cell_bg1) {
      my $min = min($re, $gr, $bl);
      if($re eq $gr && $gr eq $bl){
        $cell_bg1 = "#c5c5c5";
      }
      else {
        my $re = ($re-$min)*0.3+187;
        my $gr = ($gr-$min)*0.3+187;
        my $bl = ($bl-$min)*0.3+187;
        $cell_bg1 = sprintf("#%02x%02x%02x",$re,$gr,$bl);
      }
    }
    if(!$cell_bg2 || !$cell_text) {
      my($re, $gr, $bl) = apart($cell_bg1);
      my $luminance = ( $re * 0.3 + $gr * 0.60 + $bl * 0.1 );
      if(!$cell_bg2) {
        my $re = $re - 30; if($re < 0) { $re = 0; }
        my $gr = $gr - 30; if($gr < 0) { $gr = 0; }
        my $bl = $bl - 30; if($bl < 0) { $bl = 0; }
        $cell_bg2 = sprintf("#%02x%02x%02x",$re,$gr,$bl);
      }
      if(!$cell_text){ $cell_text = ( $luminance > 150 ? '#000000' : '#cccccc' ); }
    }
    
    if(!$link1_link){
      my $max = max($re, $gr, $bl);
      my $min = min($re, $gr, $bl);
      my $num;
      if($max - $min) { $num = 255 / ($max - $min); } else { $num = 0; }
      my $re = ($re-$min) * $num;
      my $gr = ($gr-$min) * $num;
      my $bl = ($bl-$min) * $num;
      $link1_link = sprintf("#%02x%02x%02x",$re,$gr,$bl);
    }
    if(!$link1_link_bg) { $link1_link_bg  = 'transparent'; }
    if(!$link1_hover)   { $link1_hover    = $cell_bg1; }
    if(!$link1_hover_bg){ $link1_hover_bg = $link1_link; }
    if(!$link2_link){
      my($re1, $gr1, $bl1) = apart($frame_bg);
      my($re2, $gr2, $bl2) = apart($frame_text);
      $link2_link = sprintf("#%02x%02x%02x", ($re1+$re2*2) / 3, ($gr1+$gr2*2) / 3, ($bl1+$bl2*2) / 3);
    }
    if(!$link2_hover)   { $link2_hover = $frame_bg; }
    if(!$link2_hover_bg){ $link2_hover_bg = $link2_link; }
  }
  
  if(!$hr_solid){ $hr_solid = $cell_text; }
  {
    my($re, $gr, $bl) = apart($cell_bg1);
    my $rel = $re + 51; if($rel > 255){ $rel = 255; }
    my $grl = $gr + 51; if($grl > 255){ $grl = 255; }
    my $bll = $bl + 51; if($bll > 255){ $bll = 255; }
    my $red = $re - 51; if($red < 0)  { $red = 0; }
    my $grd = $gr - 51; if($grd < 0)  { $grd = 0; }
    my $bld = $bl - 51; if($bld < 0)  { $bld = 0; }
    my $css_light = sprintf("#%02x%02x%02x",$rel,$grl,$bll);
    my $css_dark  = sprintf("#%02x%02x%02x",$red,$grd,$bld);
    if(!$hr_groove1){ $hr_groove1 = "$css_dark $css_light $css_light $css_dark"; }
    if(!$hr_ridge1) { $hr_ridge1  = "$css_light $css_dark $css_dark $css_light"; }
  }
  {
    my($re, $gr, $bl) = apart($cell_bg2);
    my $rel = $re + 51; if($rel > 255){ $rel = 255; }
    my $grl = $gr + 51; if($grl > 255){ $grl = 255; }
    my $bll = $bl + 51; if($bll > 255){ $bll = 255; }
    my $red = $re - 51; if($red < 0)  { $red = 0; }
    my $grd = $gr - 51; if($grd < 0)  { $grd = 0; }
    my $bld = $bl - 51; if($bld < 0)  { $bld = 0; }
    my $css_light = sprintf("#%02x%02x%02x",$rel,$grl,$bll);
    my $css_dark  = sprintf("#%02x%02x%02x",$red,$grd,$bld);
    if(!$hr_groove2){ $hr_groove2 = "$css_dark $css_light $css_light $css_dark"; }
    if(!$hr_ridge2) { $hr_ridge2  = "$css_light $css_dark $css_dark $css_light"; }
  }
  
  if(!$head2_bg){
    my($re1, $gr1, $bl1) = apart($frame_bg);
    my($re2, $gr2, $bl2) = apart($cell_bg1);
    $head2_bg = sprintf("#%02x%02x%02x", ($re1 *7 + $re2) / 8, ($gr1 *7 + $gr2) / 8, ($bl1 *7 + $bl2) / 8);
    if(!$head2_text){ $head2_text = $frame_text; }
  }
  if(!$head2_border){
    my($re1, $gr1, $bl1) = apart($cell_text);
    my($re2, $gr2, $bl2) = apart($head2_bg);
    $head2_border = sprintf("#%02x%02x%02x", ($re1 *3 + $re2) / 4, ($gr1 *3 + $gr2) / 4, ($bl1 *3 + $bl2) / 4);
  }
  if(!$head2_text){
    my($re, $gr, $bl) = apart($head2_bg);
    my $luminance = ( $re * 0.3 + $gr * 0.60 + $bl * 0.1 );
    $head2_text = ( $luminance > 150 ? '#000000' : '#dddddd' );
  }
  if(!$head3_bg){
    my($re1, $gr1, $bl1) = apart($head2_bg);
    my($re2, $gr2, $bl2) = apart($cell_bg1);
    $head3_bg = sprintf("#%02x%02x%02x", ($re1 *5 + $re2) / 6, ($gr1 *5 + $gr2) / 6, ($bl1 *5 + $bl2) / 6);
    if(!$head3_text){ $head3_text = $head2_text; }
  }
  if(!$head3_border){
    my($re1, $gr1, $bl1) = apart($head2_border);
    my($re2, $gr2, $bl2) = apart($head3_bg);
    $head3_border = sprintf("#%02x%02x%02x", ($re1 *3 + $re2) / 4, ($gr1 *3 + $gr2) / 4, ($bl1 *3 + $bl2) / 4);
  }
  if(!$head3_text){
    my($re, $gr, $bl) = apart($head3_bg);
    my $luminance = ( $re * 0.3 + $gr * 0.60 + $bl * 0.1 );
    $head3_text = ( $luminance > 150 ? '#000000' : '#dddddd' );
  }
  
  if(!$table_border){
    my($re1, $gr1, $bl1) = apart($cell_text);
    my($re2, $gr2, $bl2) = apart($cell_bg1);
    $table_border = sprintf("#%02x%02x%02x", ($re1 *4 + $re2) / 5, ($gr1 *4 + $gr2) / 5, ($bl1 *4 + $bl2) / 5);
  }
  if(!$th_bg){
    my($re1, $gr1, $bl1) = apart($frame_bg);
    my($re2, $gr2, $bl2) = apart($cell_bg1);
    $th_bg = sprintf("#%02x%02x%02x", ($re1 *5 + $re2) / 6, ($gr1 *5 + $gr2) / 6, ($bl1 *5 + $bl2) / 6);
    if(!$th_text){ $th_text = $frame_text; }
  }
  if(!$th_text){
    my($re, $gr, $bl) = apart($th_bg);
    my $luminance = ( $re * 0.3 + $gr * 0.60 + $bl * 0.1 );
    if(!$th_text) { $th_text = ( $luminance > 140 ? '#000000' : '#cccccc' ); }
  }
  if(!$td_bg){ $td_bg = 'transparent'; }
  if(!$td_text){ $td_text = $cell_text; }
}


if(param('mode') eq 'preview' || param('mode') eq 'list') {
  print "Content-type: text/html\n\n";
  print <<"HTML";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>シートカラー見本</title>
  <style type="text/css">
  * { margin: 0px; padding: 0px; font-family:"ＭＳ ゴシック","Osaka-等幅" }
  body { background-color:@{[ param('mode') ne'list' ? 'transparent' : ($set::design{'base_back'} ? '#eee' : '#000') ]}; padding:0px 5px 5px 0px; }
  .table {
    width:@{[ param('mode') eq 'list' ? '200' : '260' ]}px;
    margin:0px;
    padding:0px;
    border-width:2px;
    border-style:solid;
    float:left;
  }
  table {
    width:@{[ param('mode') eq 'list' ? '196' : '256' ]}px;
    margin: 0px 2px 2px 2px;
    padding: 0px; border: 0px;
    empty-cells:show;
    border-collapse:separate;
  }
  th {
    padding: 1px 0px 0px 0px;
    border : 0px;
    text-align:left;
    line-height:12px;
    font-size:12px;
    font-weight:normal;
    font-family:"ヒラギノ丸ゴ ProN W4","Hiragino Maru Gothic ProN","ヒラギノ丸ゴ Pro W4","Hiragino Maru Gothic Pro","メイリオ","Meiryo","ＭＳ Ｐゴシック","MS PGothic";
  }
  td {
    padding:2px 5px;
    border:1px solid;
    text-align:left;
    line-height:12px;
    font-size:12px;
    font-family:"Arial","ＭＳ Ｐゴシック","MS PGothic",Osaka;
  }
HTML
  if(param('rad')){
    print <<"HTML";
.table { border-radius:6px; }
.table tr:first-child td:first-child{ border-top-left-radius : 4px; }
.table tr:first-child td:last-child { border-top-right-radius: 4px; }
.table tr:last-child td:first-child { border-bottom-left-radius : 4px; }
.table tr:last-child td:last-child  { border-bottom-right-radius: 4px; }
HTML
  }
  print <<"HTML";
  </style>
</head>
<body>
HTML
  if (param('mode') eq 'list') {
    foreach my $id (sort keys %set::color){
      &colorset($id);
      print <<"HTML";
  <div class="table" style="background-color:${frame_bg}; border-color:${frame_outside}; margin:5px 0px 0px 5px;">
    <table cellspacing="0">
      <tr><th style="background-color:transparent; color:${frame_text};">$set::color{$id}{'name'}</th></tr>
      <tr><td style="background-color:${cell_bg1}; color:${cell_text}; border-color:${frame_inside};">$set::color{$id}{'name_ja'}</td></tr>
      <tr><td style="background-color:${cell_bg2}; color:${cell_text}; border-color:${frame_inside};">&nbsp;</td></tr>
    </table>
  </div>
HTML
    }
  } else {
    &colorset($id);
    print <<"HTML";
  <div class="table" style="background-color:${frame_bg}; border-color:${frame_outside};">
    <table cellspacing="0">
      <tr><th style="background-color:transparent; color:${frame_text};">$set::color{$id}{'name'}</th><th style="color:${link2_link};text-align:right;">ゆとらいず工房</th></tr>
      <tr><td colspan="2" style="background-color:${cell_bg1}; color:${cell_text}; border-color:${frame_inside};">$set::color{$id}{'name_ja'}</td></tr>
      <tr><td colspan="2" style="background-color:${cell_bg2}; color:${cell_text}; border-color:${frame_inside};">&nbsp;</td></tr>
    </table>
  </div>
HTML
  }
  print <<"HTML";
</body>
</html>
HTML
}
else { 
  &colorset($id);
  my $back = ($set::design{'base_back'} ? 238 : 0);
  print "Content-type: text/css\n\n";
  if(param('bi')){
    $set::design{'body_imag'} = $set::imgdir . param('bi');
    $set::design{'body_repe'} = param('bi_re');
    $set::design{'body_posi'} = param('bi_pox') . ' ' . param('bi_poy');
    $set::design{'body_atta'} = 'fixed';
  }
  $set::design{'body_back'} = param('bc') if param('bc');
  print <<"TEXT";
/* base */
body {
  color:$set::design{'body_text'};
  background-color     :$set::design{'body_back'};
  background-image     :url("$set::design{'body_imag'}");
  background-repeat    :$set::design{'body_repe'};
  background-attachment:$set::design{'body_atta'};
  background-position  :$set::design{'body_posi'};
}
#base {
  background: url("./img/translucent_@{[ $back?'white':'black' ]}50.png");
  background: rgba($back, $back, $back, 0.5);
  background:         linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.5) 5%, rgba($back,$back,$back,0.5));
  background:      -o-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.5) 5%, rgba($back,$back,$back,0.5));
  background:    -moz-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.5) 5%, rgba($back,$back,$back,0.5));
  background: -webkit-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.5) 5%, rgba($back,$back,$back,0.5));
}
#footer {
  background: url("./img/translucent_@{[ $back?'white':'black' ]}50.png");
  background: rgba($back, $back, $back, 0.5);
}

a        { color:$set::design{'link_text'}; }
a:visited{ color:$set::design{'link_visi'}; }
a:hover  { color:$set::design{'link_hove'}; }

#header,
#header:before,
#header:after,
#sub:before,
#sub:after,
#sub h1:before,
#sub h1:after,
#footer {
  color:$set::design{'head_text'};
  border-color:$set::design{'head_line'};
}
a.backurl {
  background: url("./img/translucent_@{[ $back?'white':'black' ]}50.png");
  background: rgba($back, $back, $back, 0.5);
  border-color:$set::design{'body_text'};
  color:$set::design{'body_text'};
}
a.backurl:hover {
  background-color:$set::design{'body_text'};
  color:$set::design{'body_back'};
}

#BackUpList {
  border-color:$set::design{'body_text'};
  background-color:@{[ $set::design{'base_back'} ? '#eee' : '#000' ]};
  color:$set::design{'body_text'};
}

#sub input[type="password"] {
  background-color:$set::design{'input_back'};
  border-color:$set::design{'body_text'};
  color:$set::design{'input_text'};
}

/* $set::color{$id}{'name'} */
.table    { background-color:${frame_bg}; border-color:${frame_outside}; }
.table th,
.table caption{ background-color:transparent; color:${frame_text}; }
.table td     { background-color:${cell_bg1}; color:${cell_text}; border-color:${frame_inside}; }
.table .rv td { background-color:${cell_bg2}; }

.item,
.item td,
.item th,
.txtable,
.txtable td,
.txtable th
      { border-color:${table_border}; }
.item th,
.txtable th
      { background-color:${th_bg}; color:${th_text}; }
.item td,
.txtable td
      { background-color:${td_bg}; color:${td_text}; }

.table td a       { color:${link1_link}; background-color:${link1_link_bg}; @{[ $link1_link eq $cell_text ? 'text-decoration:underline;' : '' ]} }
.table td a:hover { color:${link1_hover}; background-color:${link1_hover_bg}; }

.table th a       { color:${link2_link}; }
.table th a:hover { color:${link2_hover}; background-color:${link2_hover_bg}; }

    hr    { border-color:${hr_solid}; }
    hr.gro{ border-color:${hr_groove1}; }
    hr.rid{ border-color:${hr_ridge1}; }
.rv hr.gro{ border-color:${hr_groove2}; }
.rv hr.rid{ border-color:${hr_ridge2}; }

.sub       { background-color:${head2_bg}; border-color:${head2_border}; color:${head2_text}; }
.sub.small { background-color:${head3_bg}; border-color:${head3_border}; color:${head3_text}; }

.table     th .inv { color:${frame_bg}; }
.table     td .inv { color:${cell_bg1}; }
.table .rv td .inv { color:${cell_bg2}; }
.item    th .inv,
.txtable th .inv { color:${th_bg}; }
.item    td .inv,
.txtable td .inv { color:${td_bg}; }
.sub       .inv { color:${head2_bg}; }
.sub.small .inv { color:${head3_bg}; }
TEXT
  if(param('rad')){
    print <<"TEXT";
.table { border-radius:6px; }
.table tr:first-child td:first-child { border-top-left-radius    :4px; }
.table tr:first-child td:last-child  { border-top-right-radius   :4px; }
.table tr:last-child  td:first-child { border-bottom-left-radius :4px; }
.table tr:last-child  td:last-child  { border-bottom-right-radius:4px; }
#Effect tr:last-child td:first-child        { border-bottom-left-radius:0px; }
#Effect tr:nth-last-child(2) td:first-child { border-bottom-left-radius:4px; }
#EffectEz tr:last-child td:first-child        { border-bottom-left-radius:0px; }
#EffectEz tr:nth-last-child(2) td:first-child { border-bottom-left-radius:4px; }
#Lifepath tr:last-child td:last-child         { border-bottom-right-radius:0px; }
.item    td,
.txtable td { border-radius:0px !important; }
TEXT
  }
}

sub apart {
  (my $base = $_[0]) =~ s/\#//;
  my($re, $gr, $bl) = $base =~ /.{2}/g;
  return (hex($re), hex($gr), hex($bl));
}
sub max { return(  (sort {$b <=> $a} @_)[0]  ); }
sub min { return(  (sort {$a <=> $b} @_)[0]  ); }


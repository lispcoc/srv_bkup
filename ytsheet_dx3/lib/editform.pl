################## 更新フォーム ##################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use Encode;

my $mode = param('mode');
my $id;
my $pass;
my $file;
our %pc = ();

if($main::make_error) {
  $mode = 'entry';
  for (param()){ $pc{$_} = param($_); }
  $id = $pc{'id'};
}
if($main::save_message){
  $mode = 'edit';
}

if($mode eq 'edit'){
  $id = param('id');
  $pass = param('pass');
  (undef, undef, $file, undef) = &getfile($id,$pass);
  &error('記入エラー',"IDかパスワードが間違っています。") if !$file;
  open(my $IN, "${set::datadir}${file}.cgi") or &error('システムエラー',"キャラクターファイル($file)が開けません。");
  $_ =~ s/(.*?)<>(.*?)\n/$pc{$1} = $2;/egi while <$IN>;
  close($IN);
}

### ## ###############################################################################################
sub options {
  my ($selected, $list) = @_;
  my $out;
  foreach(@$list){
    $out .= '<option'.($selected eq $_ ? ' selected' : '').'>'.$_.'</option>';
  }
  return $out;
}
sub syndrome {
  my $selected = $_[0];
  my $out;
  foreach (sort { $set::syndrome{$a}{'s'} <=> $set::syndrome{$b}{'s'} } keys %set::syndrome){
    $out .= '<option'.($selected eq $_ ? ' selected' : '').'>'.$_.'</option>';
  }
  return $out;
}

### 初期値 ###########################################################################################
if($mode eq 'entry' && !$main::make_error){
  $pc{'player'} =  Encode::decode('utf8', param('player')) if $set::entry_restrict;
  
  my($day,$mon,$year) = (localtime(time))[3..5];
  $year += 1900; $mon++;
  $pc{'make_date'} = sprintf("%04d/%02d/%02d",$year,$mon,$day);
  $pc{'make_exp'}   = $set::make_exp;
  $pc{'exp'} = $set::make_exp;
  
  $pc{'exp_auto'} = 1;
}

  $pc{'count_effect'}    = 10 if !$pc{'count_effect'};
  $pc{'count_effect_ez'} = 5  if !$pc{'count_effect_ez'};
  $pc{'count_combo'}  = 3 if !$pc{'count_combo'};
  $pc{'count_weapon'} = 2 if !$pc{'count_weapon'};
  $pc{'count_armour'} = 2 if !$pc{'count_armour'};
  $pc{'count_item'}   = 4 if !$pc{'count_item'};
  $pc{'count_skill'}  = 2 if !$pc{'count_skill'};
  $pc{'count_history'}= 1 if !$pc{'count_history'};

### 他 ###############################################################################################
  my($name, $name_ruby) = split(/:/,$pc{'name'});
  my($codename, $codename_ruby) = split(/:/,$pc{'codename'});

### 改行処理 #########################################################################################
  $pc{'text_items'} =~ s/&lt;br&gt;/\n/g;
  $pc{'text_free'} =~ s/&lt;br&gt;/\n/g;
  $pc{'text_history'} =~ s/&lt;br&gt;/\n/g;
  $pc{'text_original'} =~ s/&lt;br&gt;/\n/g;
  $pc{'fami_note'} =~ s/&lt;br&gt;/\n/g;

### 基礎ステータス算出 ###############################################################################

### サブステータス ###################################################################################

### フォーム表示 #####################################################################################
my $back = ($set::design{'base_back'} ? 255 : 0);
print <<"HTML";
Content-type: text/html\n
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<title>@{[ ($mode eq 'entry')?"新規登録":"編集｜$name" ]}</title>
<link rel="stylesheet" type="text/css" href="$set::css_base">
<link rel="stylesheet" type="text/css" href="$set::css_edit">
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
  background: url("../img/translucent_@{[ $back?'white':'black' ]}70.png");
  background: rgba($back, $back, $back, 0.7);
  background:         linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
  background:      -o-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
  background:    -moz-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
  background: -webkit-linear-gradient(top, rgba($back,$back,$back,0.9), rgba($back,$back,$back,0.7) 5%, rgba($back,$back,$back,0.7));
}
#footer {
  background: rgb($back, $back, $back);
  background: rgba($back, $back, $back, 0.3);
}

a        { color:$set::design{'link_text'}; }
a:visited{ color:$set::design{'link_visi'}; }
a:hover  { color:$set::design{'link_hove'}; }
input.link { color:$set::design{'link_text'}; }

#header,
#header:before,
#header:after,
#sub:before,
#sub:after,
#sub h1:before,
#sub h1:after {
  color:$set::design{'head_text'};
  border-color:$set::design{'head_line'};
}

.message {
  background: url("../img/translucent_@{[ $back?'white':'black' ]}50.png");
  background: rgba($back, $back, $back, 0.5);
}
</style>
<script type="text/javascript">
var Syn = {
HTML
foreach (keys %set::syndrome){
  print '"'.$_.'" : ['.$set::syndrome{$_}{'stt'}[0].','.$set::syndrome{$_}{'stt'}[1].','.$set::syndrome{$_}{'stt'}[2].','.$set::syndrome{$_}{'stt'}[3].'],'."\n";
}
print <<"HTML";
};

var CountSkill   = $pc{'count_skill'};
var CountEffect  = $pc{'count_effect'};
var CountEffectEz= $pc{'count_effect_ez'};
var CountWeapon  = $pc{'count_weapon'};
var CountArmour  = $pc{'count_armour'};
var CountItem    = $pc{'count_item'};
var CountHistory = $pc{'count_history'};
</script>
<base target="_blank">
</head>
<body>
<div id="base">
<div id="header"><h1>@{[ ($mode eq 'entry')?"新規登録":"編集｜$pc{'name'}" ]}</h1></div>
<div id="sub"><h1>&nbsp;</h1></div>
@{[ ($main::save_message) ? "<div class=\"message\">$main::save_message</div>" : '' ]}
@{[ ($main::make_error) ? "<div class=\"error\">$main::make_error</div>" : '' ]}
<form name="chr" method="post" action="${set::current}${set::cgi}" enctype="multipart/form-data" target="_self">
<div class="cent" style="margin-top:10px;">
HTML
if ($mode eq 'edit') {
  print '<input type="hidden" name="mode" value="update"><input type="hidden" name="id" value="',$id,'">';
  print '<input type="hidden" name="pass" value="',$pass,'"><input type="hidden" name="mail" value="',$pc{'mail'},'">';
}
elsif($mode eq 'entry' && $set::entry_restrict) {
  print '<input type="hidden" name="mode" value="make">';
#  print 'ID:<input type="text" name="id" value="',param('id'),'" style="width:100px;" readonly>';
  print '<input type="hidden" name="pass" value="',param('pass'),'" style="width:100px;">';
  print '<input type="hidden" name="confirm" value="',param('pass'),'" style="width:100px;">';
#  print '<input type="hidden" name="mail" value="',param('mail'),'" style="width:180px;">';
  print ($set::registkey?'<input type="hidden" name="registkey" value="'.param('key').'">':''),'<hr>';
}
elsif($mode eq 'entry' && !$set::entry_restrict){
  print '<input type="hidden" name="mode" value="make">';
#  print ' ID:<input type="text" name="id" style="width:100px;">';
  print ' pass:<input type="password" name="pass" style="width:100px;">';
  print ' pass(再入力):<input type="password" name="confirm" style="width:100px;">';
#  print ' mail:<input type="text" name="mail" style="width:180px;">';
  print ($set::registkey?' 登録キー:<input type="text" name="registkey" style="width:100px;">':''),'<hr>';
}
print <<"HTML";

<div style="margin:15px 0px; text-align:center;">
<span style="color:#CC6666;">※数値類は<b>半角</b>推奨</span>／<a href="./help.html">取扱説明書</a>
</div>
HTML
if($set::hide_button){
  print <<"HTML";
<div class="table" id="Hide" style="width:270px;margin:-30px 0px 8px auto;">
<h2><input type="checkbox" name="hide" value="1" @{[ $pc{'hide'}?'checked':'' ]}> 一覧に表示しない</h2>
<div class="R">※タグ検索結果に合致した場合は表示されます</div>
</div>
HTML
}
print <<"HTML";
<div class="table" id="Taxa" style="margin:0px 0px 10px 0px;">
  <table>
  <tr>
    <th class="L" style="width:202px;">グループ</th>
    <th rowspan="2" style="width:5px;"></th>
    <th class="L">タグ <small>(複数設定する場合はスペースで区切ってください)</small></th>
  </td>
  </tr>
  <tr>
  <td class="inp">
    <select name="group">
HTML
foreach (@set::groups){
  my $num  = @$_[0];
  my $name = @$_[2];
  if($set::groupauto){
    my $flag1;
    foreach(@set::grades){
      if ($pc{'lv'} <= @$_[1] && $pc{'exp_total'} <=  @$_[2]){ $flag1 = @$_[0]; last; }
    }
    if($flag1 ne ''){
      my $flag2;
      foreach(@set::grades){
        if (@$_[0] eq $num && $flag1 ne $num){ $flag2 = 1; last; }
      }
      next if $flag2;
    }
  }
  print '<option value="',$num,'"',($pc{'group'} eq $num)?' selected':'','>',$name,'</option>';
}
print <<"HTML";
    </select>
  </td>
  <td class="inp"><input type="text" name="tag" value="$pc{'tag'}"></td>
  </tr>
  </table>
</div>

<div class="table" style="margin:0px 0px 10px 0px;">
  <table>
  <tr>
    <th class="L" style="width:30%;">コードネーム</th>
    <th rowspan="2" style="width:5px;"></th>
    <th class="L" style="width:45%;">キャラクター名</th>
    <th rowspan="2" style="width:5px;"></th>
    <th class="L">プレイヤー名</th>
  </tr>
  <tr>
  <td class="inp"><input type="text" name="codename" value="$pc{'codename'}"></td>
  <td class="inp"><input type="text" name="name" value="$pc{'name'}"></td>
  <td class="inp"><input type="text" name="player" value="$pc{'player'}"></td>
  </tr>
  </table>
  <div style="margin-left:10px;text-align:left;color:#dddddd;">コードネーム・キャラクター名にルビを振りたい場合「漢字:ルビ」と入力してください</div>
</div>

<div id="CharaR">
HTML
my $img_l; my $img_s; my $img_b;
if($pc{'ext_l'}){ $img_l = "<img src=\"${set::imgdir}${file}__.$pc{'ext_l'}\" style=\"vertical-align:top;\">".'<input type="checkbox" name="del_file" value="1">削除'; }
if($pc{'ext_s'}){ $img_s = "<img src=\"${set::imgdir}${file}___.$pc{'ext_s'}\" style=\"vertical-align:top;\">".'<input type="checkbox" name="del_thum" value="1">削除'; }
if($pc{'ext_b'}){ $img_b = "<img src=\"${set::imgdir}${file}_back_.$pc{'ext_b'}\" style=\"vertical-align:top;\">".'<input type="checkbox" name="del_back" value="1">削除'; }
print <<"HTML";
<div class="table">
  <table>
  <tr>
  <th class="L">キャラクター画像</th>
  </tr>
  <tr>
  <td>
    <input type="hidden" name="ext_l" value="$pc{'ext_l'}">
    <input type="hidden" name="ext_s" value="$pc{'ext_s'}">
    大画像：<input type="file" name="upload_file" style="width:150px;">$img_l
    <hr class="dot">
    小画像：<input type="file" name="upload_thum" style="width:150px;">$img_s
    <hr class="dot">
    <div style="line-height:1;">
    ※小画像をクリックすると大画像を表示する仕様です。<br>
    　大画像だけだと、自動的に縮小して小画像を作ります。<br>
    　ファイルサイズは500kbまでです。
    </div>
  </td>
  </tr>
  </table>
</div>

<div class="table" id="Exp">
  <table>
  <tr><th class="L">経験点</th><th class="L">消費経験点</th></tr>
  <tr><td class="inp"><input type="text" name="exp" value="$pc{'exp'}"></td><td class="C" id="ExpUse"></td></tr>
  </table>
</div>

<div class="table" id="Urge">
  <table>
  <tr><th class="L">侵蝕率現在値</th></tr>
  <tr><td class="inp"><input type="text" name="urge_current" value="$pc{'urge_current'}">％</td></tr>
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
    <td class="inp">+<input type="text" name="sub_hp_add" value="$pc{'sub_hp_add'}" style="width:30px;" onChange="calc()">=<b id="SubHpTotal"></b></td>
    <td class="inp">+<input type="text" name="sub_provide_add" value="$pc{'sub_provide_add'}" style="width:30px;" onChange="calc()">=<b id="SubProvideTotal"></b></td>
    <td class="inp"><b id="SubMoneyTotal"></b></td>
  </tr>
  <tr>
    <th class="L">行動値</th>
    <th class="L">戦闘移動</th>
    <th class="L">全力移動</th>
  </tr>
  <tr>
    <td class="inp">+<input type="text" name="sub_speed_add" value="$pc{'sub_speed_add'}" style="width:30px;" onChange="calc()">=<b id="SubSpeedTotal"></b></td>
    <td class="inp">+<input type="text" name="sub_move_add" value="$pc{'sub_move_add'}" style="width:30px;" onChange="calc()">=<b id="SubMoveTotal"></b></td>
    <td class="inp"><b id="SubFullMoveTotal"></b></td>
  </tr>
  </table>
</div>
</div>

<div id="CharaL">
<div class="table">
  <table>
  <tr>
    <th class="L">台詞</th>
  </tr>
  <tr>
    <td class="inp"><input type="text" name="word" value="$pc{'word'}"></td>
  </tr>
  </table>
</div>

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
    <td class="inp"><input type="text" name="prof_age" value="$pc{'prof_age'}"></td>
    <td class="inp"><input type="text" name="prof_sex" value="$pc{'prof_sex'}"></td>
    <td class="inp"><input type="text" name="prof_sign" value="$pc{'prof_sign'}"></td>
  </tr>
  <tr>
    <th class="L">身長</th>
    <th class="L">体重</th>
    <th class="L">血液型</th>
  </tr>
  <tr>
    <td class="inp"><input type="text" name="prof_height" value="$pc{'prof_height'}"></td>
    <td class="inp"><input type="text" name="prof_weight" value="$pc{'prof_weight'}"></td>
    <td class="inp"><input type="text" name="prof_blood" value="$pc{'prof_blood'}"></td>
  </tr>
  </table>
</div>

<div class="table" id="WandC">
  <table>
  <tr><th class="L">ワークス</th></tr>
  <tr><td class="inp"><input type="text" name="works" value="$pc{'works'}"></td></tr>
  <tr><th class="L">カヴァー</th></tr>
  <tr><td class="inp"><input type="text" name="cover" value="$pc{'cover'}"></td></tr>
  </table>
</div>

<div class="table" id="Status">
  <table>
  <caption>シンドローム／能力値 (<span id="SttTotalExp"></span>)</caption>
  <colgroup>
    <col style="width:6.5em;">
    <col style="width:13em;">
    <col>
    <col>
    <col>
    <col>
  </colgroup>
  <tr><td class="horizon" colspan="6"></td></tr>
  <tr>
    <th class="C"></th>
    <th class="C"></th>
    <th class="C">肉体</th>
    <th class="C">感覚</th>
    <th class="C">精神</th>
    <th class="C">社会</th>
  </tr>
  <tr>
    <th class="C" rowspan="2">シンドローム</th>
    <td class="inp"><select name="syndrome1" onChange="calc()"><option></option>@{[ &syndrome("$pc{'syndrome1'}") ]}</select></td>
    <td class="C" id="SttSyn1Body"></td>
    <td class="C" id="SttSyn1Sense"></td>
    <td class="C" id="SttSyn1Spirit"></td>
    <td class="C" id="SttSyn1Social"></td>
  </tr>
  <tr>
    <td class="inp"><select name="syndrome2" onChange="calc()"><option></option>@{[ &syndrome("$pc{'syndrome2'}") ]}</select></td>
    <td class="C" id="SttSyn2Body"></td>
    <td class="C" id="SttSyn2Sense"></td>
    <td class="C" id="SttSyn2Spirit"></td>
    <td class="C" id="SttSyn2Social"></td>
  </tr>
  <tr>
    <th class="C f11">オプショナル</th>
    <td class="inp"><select name="syndrome3" onChange="calc()"><option></option>@{[ &syndrome("$pc{'syndrome3'}") ]}</select></td>
  </tr>
  <tr>
    <th class="C"></th>
    <th class="C">ワークスによる修正</th>
    <th class="C"><input type="radio" name="stt_works" value="body" @{[ $pc{'stt_works'} eq 'body' ? 'checked' : '' ]} onChange="calc()"></th>
    <th class="C"><input type="radio" name="stt_works" value="sense" @{[ $pc{'stt_works'} eq 'sense' ? 'checked' : '' ]} onChange="calc()"></th>
    <th class="C"><input type="radio" name="stt_works" value="spirit" @{[ $pc{'stt_works'} eq 'spirit' ? 'checked' : '' ]} onChange="calc()"></th>
    <th class="C"><input type="radio" name="stt_works" value="social" @{[ $pc{'stt_works'} eq 'social' ? 'checked' : '' ]} onChange="calc()"></th>
  </tr>
  <tr>
    <th class="C"></th>
    <th class="C">成長</th>
    <td class="inp"><input type="text" name="stt_grow_body" value="$pc{'stt_grow_body'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_grow_sense" value="$pc{'stt_grow_sense'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_grow_spirit" value="$pc{'stt_grow_spirit'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_grow_social" value="$pc{'stt_grow_social'}" onChange="calc()"></td>
  </tr>
  <tr>
    <th class="C"></th>
    <th class="C">その他の修正</th>
    <td class="inp"><input type="text" name="stt_add_body" value="$pc{'stt_add_body'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_add_sense" value="$pc{'stt_add_sense'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_add_spirit" value="$pc{'stt_add_spirit'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="stt_add_social" value="$pc{'stt_add_social'}" onChange="calc()"></td>
  </tr>
  <tr>
    <th class="C"></th>
    <th class="C">合計</th>
    <td class="C" id="SttBody"></td>
    <td class="C" id="SttSense"></td>
    <td class="C" id="SttSpirit"></td>
    <td class="C" id="SttSocial"></td>
  </tr>
  </table>
</div>

</div>

<div style="clear:both;padding-bottom:3px;"></div>

<div class="table" id="Skill">
  <table id="SkillTable">
  <caption>技能 (<span id="SkillTotalExp"></span>)</caption>
  <colgroup>
    <col style="width:3.6em;"><col><col style="width:45px;">
    <col style="width:3.6em;"><col><col style="width:45px;">
    <col style="width:3.6em;"><col><col style="width:45px;">
    <col style="width:3.6em;"><col><col style="width:45px;">
  </colgroup>
  <tr><td class="horizon" colspan="12"></td></tr>
  <tr>
    <th class="C" colspan="2">肉体</th>
    <td class="C B" id="SkillBody"></td>
    <th class="C" colspan="2">感覚</th>
    <td class="C B" id="SkillSense"></td>
    <th class="C" colspan="2">精神</th>
    <td class="C B" id="SkillSpirit"></td>
    <th class="C" colspan="2">社会</th>
    <td class="C B" id="SkillSocial"></td>
  </tr>
  <tr>
    <td class="L" colspan="2">白兵</td>
    <td class="inp C"><input type="text" name="skill_fight_lv" value="$pc{'skill_fight_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2">射撃</td>
    <td class="inp C"><input type="text" name="skill_shoot_lv" value="$pc{'skill_shoot_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2" style="letter-spacing:.4em;">RC</td>
    <td class="inp C"><input type="text" name="skill_RC_lv" value="$pc{'skill_RC_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2">交渉</td>
    <td class="inp C"><input type="text" name="skill_nego_lv" value="$pc{'skill_nego_lv'}" style="width:30px;" onChange="calc()">Lv</td>
  </tr>
  <tr>
    <td class="L" colspan="2">回避</td>
    <td class="inp C"><input type="text" name="skill_dodge_lv" value="$pc{'skill_dodge_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2">知覚</td>
    <td class="inp C"><input type="text" name="skill_perce_lv" value="$pc{'skill_perce_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2">意志</td>
    <td class="inp C"><input type="text" name="skill_will_lv" value="$pc{'skill_will_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L" colspan="2">調達</td>
    <td class="inp C"><input type="text" name="skill_raise_lv" value="$pc{'skill_raise_lv'}" style="width:30px;" onChange="calc()">Lv</td>
  </tr>
HTML
foreach my $num (1..$pc{'count_skill'}){
  print <<"HTML";
  <tr>
    <td class="L bbR">運転：</td>
    <td class="inp bbL"><input type="text" name="skill_drive${num}_name" value="$pc{'skill_drive'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="skill_drive${num}_lv" value="$pc{'skill_drive'.$num.'_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L bbR">芸術：</td>
    <td class="inp bbL"><input type="text" name="skill_art${num}_name" value="$pc{'skill_art'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="skill_art${num}_lv" value="$pc{'skill_art'.$num.'_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L bbR">知識：</td>
    <td class="inp bbL"><input type="text" name="skill_know${num}_name" value="$pc{'skill_know'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="skill_know${num}_lv" value="$pc{'skill_know'.$num.'_lv'}" style="width:30px;" onChange="calc()">Lv</td>
    <td class="L bbR">情報：</td>
    <td class="inp bbL"><input type="text" name="skill_info${num}_name" value="$pc{'skill_info'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="skill_info${num}_lv" value="$pc{'skill_info'.$num.'_lv'}" style="width:30px;" onChange="calc()">Lv</td>
  </tr>
HTML
}
  print <<"HTML";
  </table>
  <input type="button" value="　▼　" onClick="AddSkill();"> ／ <input type="button" value="　▲　" onClick="DelSkill('');">
</div>

<div class="table" id="Effect">
  <table id="EffectTable">
  <caption>エフェクト (<span id="EffectTotalExp"></span>)</caption>
  <colgroup>
    <col style="width:2em;">
    <col>
    <col style="width:3em;">
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
  </tr><tr><td class="horizonB" colspan="9"></td></tr>
HTML
for my $num (1..$pc{'count_effect'}){
  print <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C B" rowspan="2">$num</td>
    <td class="inp"><input type="text" name="effect${num}_name" value="$pc{'effect'.$num.'_name'}"></td>
    <td class="inp lv"><input type="text" name="effect${num}_lv" value="$pc{'effect'.$num.'_lv'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="effect${num}_timing" value="$pc{'effect'.$num.'_timing'}"></td>
    <td class="inp"><input type="text" name="effect${num}_skill" value="$pc{'effect'.$num.'_skill'}"></td>
    <td class="inp"><input type="text" name="effect${num}_diffi" value="$pc{'effect'.$num.'_diffi'}"></td>
    <td class="inp"><input type="text" name="effect${num}_target" value="$pc{'effect'.$num.'_target'}"></td>
    <td class="inp"><input type="text" name="effect${num}_range" value="$pc{'effect'.$num.'_range'}"></td>
    <td class="inp"><input type="text" name="effect${num}_point" value="$pc{'effect'.$num.'_point'}"></td>
    <td class="inp"><input type="text" name="effect${num}_limit" value="$pc{'effect'.$num.'_limit'}" onChange="calc()"></td>
  </tr><tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}><td class="inp" colspan="9"><input type="text" name="effect${num}_note" value="$pc{'effect'.$num.'_note'}"></td></tr>
  </tr><tr><td class="horizonB" colspan="9"></td></tr>
HTML
  if($num % 10 == 0){
    print <<"HTML";
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
  }
}
print <<"HTML";
  <tr><td class="horizon" colspan="10"></td></tr>
  </table>
  <input type="button" value="　▼　" onClick="AddEffect('');"> ／ <input type="button" value="　▲　" onClick="DelEffect('');">
</div>

<div class="table" id="EffectEz">
  <table id="EffectEzTable">
  <caption>イージーエフェクト (<span id="EffectEzTotalExp"></span>)</caption>
  <colgroup>
    <col style="width:2em;">
    <col>
    <col style="width:3em;">
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
for my $num (1..$pc{'count_effect_ez'}){
print <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="C B" rowspan="2">$num</td>
    <td class="inp"><input type="text" name="effect_ez${num}_name" value="$pc{'effect_ez'.$num.'_name'}"></td>
    <td class="inp lv"><input type="text" name="effect_ez${num}_lv" value="$pc{'effect_ez'.$num.'_lv'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_timing" value="$pc{'effect_ez'.$num.'_timing'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_skill" value="$pc{'effect_ez'.$num.'_skill'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_diffi" value="$pc{'effect_ez'.$num.'_diffi'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_target" value="$pc{'effect_ez'.$num.'_target'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_range" value="$pc{'effect_ez'.$num.'_range'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_point" value="$pc{'effect_ez'.$num.'_point'}"></td>
    <td class="inp"><input type="text" name="effect_ez${num}_limit" value="$pc{'effect_ez'.$num.'_limit'}"></td>
  </tr><tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}><td class="inp" colspan="9"><input type="text" name="effect_ez${num}_note" value="$pc{'effect_ez'.$num.'_note'}"></td></tr>
  </tr><tr><td class="horizonB" colspan="9"></td></tr>
HTML
}
print <<"HTML";
  </table>
  <input type="button" value="　▼　" onClick="AddEffect('Ez');"> ／ <input type="button" value="　▲　" onClick="DelEffectEz();">
</div>

<div class="table" id="HideData">
  <table>
  <tr><th class="L">データを不明にする</th></tr>
  <tr>
    <td class="L"><input type="checkbox" name="hide_syndrome" value="checked" $pc{'hide_syndrome'}>シンドローム</td>
    <td class="L"><input type="checkbox" name="hide_stt" value="checked" $pc{'hide_stt'}>能力値</td>
    <!--
      <td class="L"><input type="checkbox" name="hide_skill" value="checked" $pc{'hide_skill'}>技能</td>
    -->
    <td class="L"><input type="checkbox" name="hide_hpmax" value="checked" $pc{'hide_hpmax'}>HP</td>
    <td class="L"><input type="checkbox" name="hide_speed" value="checked" $pc{'hide_speed'}>行動値</td>
    <td class="L"><input type="checkbox" name="hide_urge_current" value="checked" $pc{'hide_urge_current'}>侵蝕率現在値</td>
    <td class="L"><input type="checkbox" name="hide_effect" value="checked" $pc{'hide_effect'}>エフェクト</td>
  </tr>
  </table>
</div>

<div class="table" id="FreeArea">
  <table>
    <tr><th class="L">設定・その他メモ</th></tr>
    <tr><td class="inp"><textarea name="text_free" style="height:320px;">$pc{'text_free'}</textarea></td></tr>
  </table>
</div>

<label>
  <input type="checkbox" value="off"
     onclick="if (this.checked) document.getElementById('description').style.display='block';
              else document.getElementById('description').style.display='none';">詳細な設定を表示
</label>：

<div id="description" style="display:none">

<div class="table">
<h2><a href="./help.html#growcount" style="float:right;">※</a>初期レギュレーション</h2>
<div id="Regulation">
  <hr>
  <table>
  <tr>
    <th class="C" style="width:85px;">作成日</th>
    <th class="C" style="width:75px;">経験点</th>
    <th></th>
  </tr>
  <tr>
    <td class="inp"><input type="text" name="make_date" value="$pc{'make_date'}"></td>
    <td class="inp"><input type="text" name="make_exp" value="$pc{'make_exp'}" onchange="exp_calc()" @{[ ($set::make_fix)?'readonly':'' ]}></td>
  </tr>
</table>
</div>
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
    <td class="inp C" colspan="2"><input type="text" name="lifepath_birth" value="$pc{'lifepath_birth'}"></td>
    <td class="inp"><input type="text" name="lifepath_birth_note" value="$pc{'lifepath_birth_note'}"></td>
  </tr>
  <tr>
    <th class="L">経験</th>
  </tr>
  <tr>
    <td class="inp C" colspan="2"><input type="text" name="lifepath_exp" value="$pc{'lifepath_exp'}"></td>
    <td class="inp"><input type="text" name="lifepath_exp_note" value="$pc{'lifepath_exp_note'}"></td>
  </tr>
  <tr>
    <th class="L">邂逅・欲望</th>
  </tr>
  <tr>
    <td class="inp C" colspan="2"><input type="text" name="lifepath_meet" value="$pc{'lifepath_meet'}"></td>
    <td class="inp"><input type="text" name="lifepath_meet_note" value="$pc{'lifepath_meet_note'}"></td>
  </tr>
  <tr>
    <th class="L">覚醒</th>
    <th class="C">侵蝕値</th>
  </tr>
  <tr>
    <td class="inp C"><input type="text" name="lifepath_awaken" value="$pc{'lifepath_awaken'}"></td>
    <td class="inp C"><input type="text" name="lifepath_awaken_invade" value="$pc{'lifepath_awaken_invade'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="lifepath_awaken_note" value="$pc{'lifepath_awaken_note'}"></td>
  </tr>
  <tr>
    <th class="L">衝動</th>
    <th class="C">侵蝕値</th>
  </tr>
  <tr>
    <td class="inp C"><input type="text" name="lifepath_urge" value="$pc{'lifepath_urge'}"></td>
    <td class="inp C"><input type="text" name="lifepath_urge_invade" value="$pc{'lifepath_urge_invade'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="lifepath_urge_note" value="$pc{'lifepath_urge_note'}"></td>
  </tr>
  <tr>
    <th></th>
    <th class="L" colspan="2" style="text-indent:-1em;">その他の修正</th>
  </tr>
  <tr>
    <th></th>
    <td class="inp C"><input type="text" name="lifepath_other_invade" value="$pc{'lifepath_other_invade'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="lifepath_other_note" value="$pc{'lifepath_other_note'}"></td>
  </tr>
  <tr>
    <th></th>
    <th class="L" colspan="2" style="text-indent:-.5em;">基本侵蝕値</th>
  </tr>
  <tr>
    <th></th>
    <td class="C B" id="SttInvade"></td>
  </tr>
  
  </table>
</div>

<div class="table" id="Lois">
  <table>
  <caption>ロイス</caption>
  <colgroup>
    <col style="width:6em;">
    <col style="width:14em;">
    <col style="width:1em;">
    <col style="width:4em;">
    <col style="width:1em;">
    <col style="width:4em;">
    <col>
    <col style="width:1.6em;">
  </colgroup>
  <tr><td class="horizon" colspan="8"></td></tr>
  <tr>
    <th class="L">関係</th>
    <th class="L">名前</th>
    <th class="L" colspan="2">感情:Posi</th>
    <th class="L" colspan="2">感情:Nega</th>
    <th class="R" colspan="2">タイタス</th>
  </tr>
HTML
for my $num (1..7){
print <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="inp"><input type="text" name="lois${num}_relation" value="$pc{'lois'.$num.'_relation'}"></td>
    <td class="inp"><input type="text" name="lois${num}_name" value="$pc{'lois'.$num.'_name'}"></td>
    <td class="inp bbR"><input type="checkbox" name="lois${num}_check" id="LoisP${num}" value="P" @{[ $pc{'lois'.$num.'_check'} eq 'P'?'checked':'' ]} onClick="emoP(${num})"></td><td class="inp bbL"><input type="text" name="lois${num}_positive" value="$pc{'lois'.$num.'_positive'}"></td>
    <td class="inp bbR"><input type="checkbox" name="lois${num}_check" id="LoisN${num}" value="N" @{[ $pc{'lois'.$num.'_check'} eq 'N'?'checked':'' ]} onClick="emoN(${num})"></td><td class="inp bbL"><input type="text" name="lois${num}_negative" value="$pc{'lois'.$num.'_negative'}"></td>
    <td class="inp"><input type="text" name="lois${num}_note" value="$pc{'lois'.$num.'_note'}"></td>
    <td class="inp"><input type="checkbox" name="lois${num}_titus" value="checked" $pc{'lois'.$num.'_titus'}></td>
  </tr>
HTML
}
print <<"HTML";
  </table>
</div>

<div class="table" id="Memory">
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
for my $num (1..3){
print <<"HTML";
  <tr@{[ $num % 2 == 1 ? '' : ' class="rv"' ]}>
    <td class="inp"><input type="text" name="memory${num}_relation" value="$pc{'memory'.$num.'_relation'}"></td>
    <td class="inp"><input type="text" name="memory${num}_name" value="$pc{'memory'.$num.'_name'}"></td>
    <td class="inp"><input type="text" name="memory${num}_emotion" value="$pc{'memory'.$num.'_emotion'}"></td>
    <td class="inp"><input type="text" name="memory${num}_note" value="$pc{'memory'.$num.'_note'}"></td>
  </tr>
HTML
}
print <<"HTML";
  </table>
</div>

<div class="table" id="Combo">
  <table>
  <caption>コンボデータ</caption>
  <colgroup>
    <col>
    <col style="width:13%;">
    <col style="width:5em;">
    <col style="width:10.7%;">
    <col style="width:7.8%;">
    <col style="width:4.9em;">
    <col style="width:7.8%;">
    <col style="width:7.8%;">
    <col style="width:7.8%;">
    <col style="width:3.8em;">
  </colgroup>
HTML
for my $num (1..$pc{'count_combo'}){
print <<"HTML";
  <tr><td class="horizon" colspan="10"></td></tr>
  <tr><td class="horizonB"></td></tr>
  <tr>
    <td class="inp" rowspan="2" colspan="2"><input type="text" name="combo${num}_name" value="$pc{'combo'.$num.'_name'}"></td>
    <th class="C" colspan="8">組み合わせ</th>
  </tr>
  <tr>
    <td class="inp" colspan="8"><input type="text" name="combo${num}_set" value="$pc{'combo'.$num.'_set'}"></td>
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
  <tr>
    <td class="inp"><input type="text" name="combo${num}_timing" value="$pc{'combo'.$num.'_timing'}"></td>
    <td class="inp"><input type="text" name="combo${num}_skill" value="$pc{'combo'.$num.'_skill'}"></td>
    <td class="inp"><input type="text" name="combo${num}_diffi" value="$pc{'combo'.$num.'_diffi'}"></td>
    <td class="inp"><input type="text" name="combo${num}_target" value="$pc{'combo'.$num.'_target'}"></td>
    <td class="inp"><input type="text" name="combo${num}_range" value="$pc{'combo'.$num.'_range'}"></td>
    <th class="C f11">100%未満</th>
    <td class="inp num"><input type="text" name="combo${num}_under_dice" value="$pc{'combo'.$num.'_under_dice'}"></td>
    <td class="inp num"><input type="text" name="combo${num}_under_crit" value="$pc{'combo'.$num.'}_under_crit'}"></td>
    <td class="inp num"><input type="text" name="combo${num}_under_power" value="$pc{'combo'.$num.'_under_power'}"></td>
    <td class="inp num" rowspan="2"><input type="text" name="combo${num}_point" value="$pc{'combo'.$num.'_point'}"></td>
  </tr>
  <tr>
    <th colspan="5"></th>
    <th class="C f11">100%以上</th>
    <td class="inp num"><input type="text" name="combo${num}_over_dice" value="$pc{'combo'.$num.'_over_dice'}"></td>
    <td class="inp num"><input type="text" name="combo${num}_over_crit" value="$pc{'combo'.$num.'_over_crit'}"></td>
    <td class="inp num"><input type="text" name="combo${num}_over_power" value="$pc{'combo'.$num.'_over_power'}"></td>
  </tr>
  <tr><td class="inp" colspan="10"><input type="text" name="combo${num}_note" value="$pc{'combo'.$num.'_note'}"></td></tr>
  <tr><td class="horizonB"></td></tr>
HTML
}
print <<"HTML";
  </table>
</div>

<div class="table" id="Item">
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
  <tr>
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
for my $num (1..$pc{'count_weapon'}){
  print <<"HTML";
  <tr>
    <td class="inp"><input type="text" name="weapon${num}_name" value="$pc{'weapon'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="weapon${num}_point" value="$pc{'weapon'.$num.'_point'}" onChange="calc()"></td>
    <td class="inp C"><input type="text" name="weapon${num}_exp" value="$pc{'weapon'.$num.'_exp'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="weapon${num}_type" value="$pc{'weapon'.$num.'_type'}"></td>
    <td class="inp"><input type="text" name="weapon${num}_skill" value="$pc{'weapon'.$num.'_skill'}"></td>
    <td class="inp C"><input type="text" name="weapon${num}_hit" value="$pc{'weapon'.$num.'_hit'}"></td>
    <td class="inp C"><input type="text" name="weapon${num}_power" value="$pc{'weapon'.$num.'_power'}"></td>
    <td class="inp C"><input type="text" name="weapon${num}_guard" value="$pc{'weapon'.$num.'_guard'}"></td>
    <td class="inp"><input type="text" name="weapon${num}_range" value="$pc{'weapon'.$num.'_range'}"></td>
    <td class="inp"><input type="text" name="weapon${num}_note" value="$pc{'weapon'.$num.'_note'}"></td>
  </tr>
HTML
}
print <<"HTML";
  </table>
  
  <table>
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
for my $num (1..$pc{'count_armour'}){
  print <<"HTML";
  <tr>
    <td class="inp"><input type="text" name="armour${num}_name" value="$pc{'armour'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="armour${num}_point" value="$pc{'armour'.$num.'_point'}" onChange="calc()"></td>
    <td class="inp C"><input type="text" name="armour${num}_exp" value="$pc{'armour'.$num.'_exp'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="armour${num}_type" value="$pc{'armour'.$num.'_type'}"></td>
    <td class="inp"></td>
    <td class="inp C"><input type="text" name="armour${num}_dodge" value="$pc{'armour'.$num.'_dodge'}"></td>
    <td class="inp C"><input type="text" name="armour${num}_speed" value="$pc{'armour'.$num.'_speed'}"></td>
    <td class="inp C"><input type="text" name="armour${num}_guard" value="$pc{'armour'.$num.'_guard'}"></td>
    <td class="inp"><input type="text" name="armour${num}_note" value="$pc{'armour'.$num.'_note'}"></td>
  </tr>
HTML
}
print <<"HTML";
  </table>
  
  <table>
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
for my $num (1..$pc{'count_item'}){
  print <<"HTML";
  <tr>
    <td class="inp"><input type="text" name="item${num}_name" value="$pc{'item'.$num.'_name'}"></td>
    <td class="inp C"><input type="text" name="item${num}_point" value="$pc{'item'.$num.'_point'}" onChange="calc()"></td>
    <td class="inp C"><input type="text" name="item${num}_exp" value="$pc{'item'.$num.'_exp'}" onChange="calc()"></td>
    <td class="inp"><input type="text" name="item${num}_type" value="$pc{'item'.$num.'_type'}"></td>
    <td class="inp"><input type="text" name="item${num}_skill" value="$pc{'item'.$num.'_skill'}"></td>
    <td class="inp"><input type="text" name="item${num}_note" value="$pc{'item'.$num.'_note'}"></td>
  </tr>
HTML
}
print <<"HTML";
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
    <th></th>
    <td class="C" id="ItemTotalPoint"></td>
    <td class="C" id="ItemTotalExp"></td>
    <th></th>
  </tr>
  </table>
</div>

<div class="table" id="History">
<h2>履歴 <a onclick="visible('History_view');">▼表示／非表示</a></h2>
<div id="History_view" @{[ ($mode eq 'entry')?'style="display:none;"':'']}>
<hr>
  <table id="table_history">
  <tr>
    <th class="C" style="width:85px;">日付</th>
    <th class="C" style="width:170px;">タイトル</th>
    <th class="C" style="width:75px;">経験点</th>
    <th class="C" style="width:75px;">GM</th>
    <th class="C">参加者</th>
  </tr>
HTML
  for (my $i = 1; $i <= $pc{'count_history'}; $i++) {
print <<"HTML";
  <tr>
    <td class="inp"><input type="text" name="hist_date$i" value="$pc{"hist_date$i"}"></td>
    <td class="inp"><input type="text" name="hist_name$i" value="$pc{"hist_name$i"}"></td>
    <td class="inp"><input type="text" name="hist_exp$i" value="$pc{"hist_exp$i"}" onchange="exp_calc()"></td>
    <td class="inp"><input type="text" name="hist_gm$i" value="$pc{"hist_gm$i"}"></td>
    <td class="inp"><input type="text" name="hist_member$i" value="$pc{"hist_member$i"}"></td>
  </tr>
  <tr>
    <th class="L R" colspan="2">備考</th>
    <td class="inp" colspan="8"><input type="text" name="hist_note$i" value="$pc{"hist_note$i"}"></td>
  </tr>
HTML
  }
print <<"HTML";
  <tr class="rv">
    <td class="inp"><input type="text" readonly value="2017/05/01"></td>
    <td class="inp"><input type="text" readonly value="キャンペーン第一話「記入例」"></td>
    <td class="inp"><input type="text" readonly value="10+5+1"></td>
    <td class="inp"><input type="text" readonly value="GMtest"></td>
    <td class="inp"><input type="text" readonly value="一浦青磁　二ノ瀬紫織　三上茜"></td>
  </tr>
  <tr class="rv">
    <th class="C"><a onClick="AddHistory();">▼</a> ／ <a onClick="DelHistory();">▲</a></th>
    <th class="L R">備考</th>
    <td class="inp" colspan="8"><input type="text" readonly value=""></td>
  </tr>
  <tr>
    <th class="C"></th>
    <th class="L R">解説</th>
    <td class="L" colspan="5">
      　経験点欄四則演算が有効です。<br>
    </td>
  </tr>
  </table>
  <div class="L"><input type="checkbox" name="exp_auto" value="1" @{[ $set::auto_calc ? 'checked onClick="return false"' : $pc{'exp_auto'} ? 'checked' : '' ]} onchange="exp_calc()">経験点自動計算をONにする</div>
</div>
</div>

<div class="table" id="HistoryFree">
  <table>
    <tr><th class="L">履歴</th></tr>
    <tr><td class="inp"><textarea name="text_history" style="height:320px;">$pc{'text_history'}</textarea></td></tr>
  </table>
</div>

<div style="clear:both;"></div>

<div class="table" style="float:left;">
  <table>
  <tr><th class="L" colspan="2"><a href="./help.html#sheetcolor" style="float:right;">※</a>シートカラー（<a href="./color.cgi?mode=list">一覧</a>）</th></tr>
  <tr>
  <td class="inp">
    <select name="CSS" onChange="jump()">
HTML
require './colorset.cgi';
foreach (sort keys %set::color){
  if($set::color{$_}{'frame'}{'back'} && !$set::color{$_}{'frame'}{'text'}) {
    (my $base = $set::color{$_}{'frame'}{'back'}) =~ s/\#//;
    my($re, $gr, $bl) = $base =~ /.{2}/g;
    my $luminance = ( hex($re) * 0.3 + hex($gr) * 0.60 + hex($bl) * 0.1 );
    $set::color{$_}{'frame'}{'text'} = ( $luminance > 150 ? '#000000' : '#dddddd' );
  }
  print '<option value="',$_,'" style="background-color:'.$set::color{$_}{'frame'}{'back'}.';color:'.$set::color{$_}{'frame'}{'text'}.';"',($pc{'CSS'} eq $_)?' selected':'','>',$set::color{$_}{'name'},'</option>';
}

my %out;
if($pc{'mycss'}){
  foreach('css_frame','css_font1','css_pl','css_cell1','css_cell2','css_font2','css_link'){
    $out{$_} = uri_escape_utf8($pc{$_});
  }
}
print <<"HTML";
    </select>
  </td>
  </tr>
  </table>
  <div class="L"><input type="checkbox" name="css_radius" value="1" @{[ $pc{'css_radius'}?'checked':'']} onchange="jump()">角丸<small> (IE8以下未対応)</small></div>
</div>

<iframe src="$set::css_cgi?mode=preview&id=$pc{'CSS'}&rad=$pc{'css_radius'}@{[ $pc{'mycss'} ? "&fb=$out{'css_frame'}&ft=$out{'css_font1'}&fl=$out{'css_pl'}&cb1=$out{'css_cell1'}&cb2=$out{'css_cell2'}&ct=$out{'css_font2'}&cl=$out{'css_link'}" :'' ]}" name="css" style="margin-left:5px;width:264px;height:60px;float:left;" frameborder="0" scrolling="no">
この部分はインラインフレームを使用しています。
</iframe>

<div style="clear:both;"></div>

<div class="table" style="float:left;width:70%;">
  <h2>
    <a href="./help.html#sheetcolor" style="float:right;">※</a>
    <input type="checkbox" name="mycss" value="1" @{[ $pc{'mycss'}?'checked':'']} onchange="jump()">キャラシートをカスタムする<br>　上記で選択したものがベースになります。 ／ 16進数のカラーコードで入力してください。
  </h2>
  <hr class="gro">
  <table>
  <tr><th>フレーム<br>背景色</th><th>フレーム<br>文字色</th><th>セル<br>背景色</th><th>セル<br>背景色2</th><th>セル<br>文字色</th><th>リンク色</th><th>リンク色<br>(PL名)</th></tr>
  <tr>
    <td class="inp"><input type="text" maxlength="7" name="css_frame" value="$pc{'css_frame'}" onchange="tbcolorcheck(this,1,1);"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_font1" value="$pc{'css_font1'}" onchange="tbcolorcheck(this,0,0);"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_cell1" value="$pc{'css_cell1'}" onchange="tbcolorcheck(this,2,1);"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_cell2" value="$pc{'css_cell2'}" onchange="tbcolorcheck(this,2,1);"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_font2" value="$pc{'css_font2'}" onchange="tbcolorcheck(this,2,0);"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_link" value="$pc{'css_link'}"></td>
    <td class="inp"><input type="text" maxlength="7" name="css_pl" value="$pc{'css_pl'}"></td>
  </tr>
  <tr><th colspan="7" class="R"><input type="button" value=" preview " onClick="jump()"></th></tr>
  </table>
  <hr class="gro">
  <div class="L">
    指定できる色は限定されています。<br>
    指定できない色を入力すると、入力欄の色が変わります。<br>
    （赤＝数値が大きい、青＝数値が小さい、黄＝彩度が高い）
  </div>
</div>

<div class="table" style="float:left;width:70%;">
  <h2>背景画像</h2>
  <table>
  <tr>
    <td class="L" colspan="2">
      <input type="hidden" name="ext_b" value="$pc{'ext_b'}"><input type="file" name="upload_back">$img_b<br>
      ファイルサイズは@{[ int(( $set::image_maxsize ? $set::image_maxsize : 1024 * 512 ) / 1024 ) ]}KBまでです。
    </td>
  </tr>
  <tr>
    <th class="C" style="width:7.5em;">背景画像の位置</th>
    <td class="L">
      横方向:
      <input type="radio" name="back_position_x" value="left"   @{[ $pc{'back_position_x'} eq 'left'  ? 'checked' : '' ]}>左
      <input type="radio" name="back_position_x" value="center" @{[ $pc{'back_position_x'} eq 'center'? 'checked' : '' ]}>中央
      <input type="radio" name="back_position_x" value="right"  @{[ $pc{'back_position_x'} eq 'right' ? 'checked' : '' ]}>右
      <br>
      縦方向:
      <input type="radio" name="back_position_y" value="top"    @{[ $pc{'back_position_y'} eq 'top'   ? 'checked' : '' ]}>上
      <input type="radio" name="back_position_y" value="middle" @{[ $pc{'back_position_y'} eq 'middle'? 'checked' : '' ]}>中央
      <input type="radio" name="back_position_y" value="bottom" @{[ $pc{'back_position_y'} eq 'bottom'? 'checked' : '' ]}>下
    </td>
  </tr>
  <tr>
    <th class="C">背景のリピート</th>
    <td class="L">
      <input type="radio" name="back_repeat" value="no-repeat" @{[ $pc{'back_repeat'} eq 'no-repeat'? 'checked' : '' ]}>しない
      <input type="radio" name="back_repeat" value="repeat"    @{[ $pc{'back_repeat'} eq 'repeat'   ? 'checked' : '' ]}>する
      <input type="radio" name="back_repeat" value="repeat-x"  @{[ $pc{'back_repeat'} eq 'repeat-x' ? 'checked' : '' ]}>横だけ
      <input type="radio" name="back_repeat" value="repeat-y"  @{[ $pc{'back_repeat'} eq 'repeat-y' ? 'checked' : '' ]}>縦だけ
    </td>
  </tr>
  <tr>
    <th class="C">背景色</th>
    <td class="inp">
      <input type="text" maxlength="7" name="back_color" value="$pc{'back_color'}">
    </td>
  </tr>
  </table>
</div>

</div>

<div style="clear:both;"></div>

<input type="hidden" name="file" value="${file}">
<input type="hidden" name="birth" value="$pc{'birth'}">
<input type="hidden" name="count_skill" value="$pc{'count_skill'}">
<input type="hidden" name="count_effect" value="$pc{'count_effect'}">
<input type="hidden" name="count_effect_ez" value="$pc{'count_effect_ez'}">
<input type="hidden" name="count_combo" value="$pc{'count_combo'}">
<input type="hidden" name="count_weapon" value="$pc{'count_weapon'}">
<input type="hidden" name="count_armour" value="$pc{'count_armour'}">
<input type="hidden" name="count_item" value="$pc{'count_item'}">
<input type="hidden" name="count_history" value="$pc{'count_history'}">

<p>
  <input style="margin-top:30px;padding:3px 0px;width:120px;text-indent:2em;letter-spacing:2em;" type="submit" value="@{[ ($mode eq 'entry')?'登録':'更新' ]}">
</p>
</div>

</form>

HTML
if($set::del_on || $pass eq $set::masterkey){
  print <<"HTML";
<hr style="margin:1.5em 0;border-top:1px solid #777;">

<form name="del" method="post" action="${set::current}${set::cgi}" enctype="multipart/form-data" target="_self">
<p style="text-align:right;">
  <input type="hidden" name="mode" value="form">
  <input type="hidden" name="m" value="delete">
  <input type="hidden" name="id" value="${id}">
  pass:<input type="password" name="pass" style="width:10em">
  <input type="submit" value="データ削除" style="padding:3px;">
</p>
</form>
HTML
}
print <<"HTML";

<p></p>

<script type="text/javascript" language="JavaScript" src="./lib/editform.js"></script>
<div id="footer">
  「ダブルクロス The 3rd Edition」は矢野俊策及び有限会社F.E.A.R.の著作物です。<br>
  ゆとシート for DX3rd ver.$main::ver - <a href="http://yutorize.2-d.jp/">ゆとらいず工房</a>
</div>
</div>
</body>
</html>
HTML

1;
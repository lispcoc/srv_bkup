#!/usr/local/bin/perl
###################################
#####    ゆとシート for DX3rd #####
#####             version2.00 #####
#####           by ゆとらいず #####
#####  http://yutorize.2-d.jp #####
###########################################################
##### 参考 : Itsuki氏 ( http://www.new-f.com/ ) の    #####
#####        ソードワールドキャラクター管理プログラム #####
###########################################################
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:all/;
use Encode;

################### バージョン ###################

our $ver = "2.00";

#################### 設定読込 ####################

require './config.cgi';
require './setting.cgi';
require './file.cgi';

##################################################

my $mode = param('mode');

   if($mode eq 'form')   { require $set::lib_form; }   #フォーム
elsif($mode eq 'entry')  { require $set::lib_edit; }   #キャラ登録フォーム
elsif($mode eq 'edit')   { require $set::lib_edit; }   #キャラ更新フォーム
elsif($mode eq 'update') { require $set::lib_update; } #キャラデータ保存
elsif($mode eq 'make')   { require $set::lib_update; } #キャラデータ保存(作成時)
elsif($mode eq 'list1')  { require $set::lib_list1; }  #キャラリスト(簡易)
elsif($mode eq 'list2')  { require $set::lib_list2; }  #キャラリスト(詳細)
elsif($mode eq 'remind') { require $set::lib_remind; } #パスワードリマインダ
elsif($mode eq 'forget') { require $set::lib_forget; }
elsif($mode eq 'change') { require $set::lib_change; } #パスワードの変更
elsif($mode eq 'delete') { require $set::lib_delete; } #データ削除
elsif($mode eq 'tags')   { &taglist; } #タグリスト
elsif(param('jump')){ &jump; }
elsif(param('page')){ print 'Location: '.$set::datadir.(param('page')).'.html'."\n\n"; }
 else { require $set::lib_list1; }
exit;

##################################################

### ファイル名取得 ###
sub getfile {
  open (my $FH, '<', $set::passfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
  while (<$FH>) {
    my ($id, $pass, $file, $name, $mail, $pl) = (split /<>/, $_)[0..5];
    if ($_[0] eq $id && (&c_crypt($_[1], $pass) || $_[1] eq $set::masterkey)) {
      close($FH);
      return ($id, $pass, $file, $name, $mail, $pl);
    }
  }
  close($FH);
  return 0;
}

### メール送信 ###
sub sendmail{
#  my $to      = shift;
#  my $subject = Encode::encode_utf8(shift);
#  my $message = Encode::encode_utf8(shift);
#
#  Encode::from_to($subject, "utf-8", "iso-2022-jp" );
#  Encode::from_to($message, "utf-8", "iso-2022-jp" );
#  encode('MIME-Header-ISO_2022_JP', $subject);
#
#  open (my $MA, "|$set::sendmail -t") or &error('システムエラー',"sendmailの起動に失敗しました。");
#  print $MA "To: $to\n";
#  print $MA "From: ゆとシート for SW2.0 <$set::admimail>\n";
#  print $MA "Subject: $subject\n";
#  print $MA "Content-Transfer-Encoding: 7bit\n";
#  print $MA "Content-Type: text/plain; charset=iso-2022-jp\n\n";
#  print $MA $message;
#  close($MA);
}

### タグリスト ###
sub taglist {
  my %tags;
  open (my $FH, '<', $set::listfile) or &error('システムエラー','一覧データのオープンに失敗しました。');
  while (<$FH>) {
    my @data2 = (split /<>/, $_);
    my $tag = (split /<>/, $_)[16];
    my @tag = (split /\s/, $tag);
    foreach (@tag){
      $_ =~ /\s/;
      next if(!$_);
      $tags{$_} += 1;
    }
  }
  close($FH);

  my $header_head = <<"TMP";
    <style type="text/css">
    #TagList { width:700px; }
    #TagList a {
      margin-right:1em;
      white-space:nowrap;
    }
    </style>
TMP
  
  require $set::lib_template;
  print "Content-type: text/html\n\n";
  print &template::_header('タグリスト',$header_head);
  print <<"HTML";
<div class="chara" id="TagList">
  <div class="box">
    <div class="text">
HTML
  foreach my $tag (sort { $tags{$b} <=> $tags{$a} }  keys( %tags ) ) {
    my $log = log($tags{$tag});
    my $height = sprintf("%3.2f", (12 + $log * $log));
    print '<a href="',${set::cgi},'?g=',uri_escape_utf8($tag),'&mode=list2&m=search_t" style="font-size:',$height,'px;line-height:',($height + 5),'px;">',$tag,'(',$tags{$tag},')</a> ';
  }
  print <<"HTML";
      <br>
    </div>
  </div>
</div>
HTML
  print &template::_footer;
}

### ジャンプ ###
sub jump {
  require $set::lib_template;
  my $url;
  if ($ENV{'REQUEST_METHOD'} eq "POST"){
    read(STDIN, $url, $ENV{'CONTENT_LENGTH'});
  }
  else{
    $url = $ENV{'QUERY_STRING'};
  }
  $url =~ s/^jump=//;
  print "Content-type: text/html\n\n";
  print &template::_header;
  print <<"HTML";
<div class="chara" style="width:600px;">
  <div class="box">
    <h2>下記のURLにジャンプします</h2>
    <div class="text" style="word-wrap:break-word;">
      <br>
      <a href="$url">$url</a><br>
      <br>
    </div>
  </div>
</div>
HTML
  print &template::_footer;
}

### エラー ###
sub error {
  require $set::lib_template;
  print "Content-type: text/html\n\n";
  print &template::_header($_[0]);
  print <<"EOM";
<div class="chara" style="width:500px;">
  <div class="box">
    <h2>$_[0]</h2>
    <div class="text">
      <br>
      $_[1]<br>
      <br>
      ブラウザの[戻る]ボタンを押して前の画面に移動してください<br>
      <br>
    </div>
  </div>
</div>
EOM
  print &template::_footer;
  exit(1);
}

### 暗号化 ###
sub e_crypt {
  my $plain = shift;
  my $s;
  my @salt = ('0'..'9','A'..'Z','a'..'z','.','/');
  1 while (length($s .= $salt[rand(@salt)]) < 8);
  return crypt($plain,index(crypt('a','$1$a$'),'$1$a$') == 0 ? '$1$'.$s.'$' : $s);
}

sub c_crypt {
  my($plain,$crypt) = @_;
  return ($plain ne '' && $crypt ne '' && crypt($plain,$crypt) eq $crypt);
}

### eval ###
sub s_eval {
  my $i = shift;
  if($i =~ /[^0-9\+\-\*\/ ]/){ $i = 0; }
  return eval($i);
}

### URIエスケープ ###
sub uri_escape_utf8 {
  my($tmp) = @_;
  $tmp = Encode::encode('utf8',$tmp);
  $tmp =~ s/([^\w])/'%'.unpack("H2", $1)/ego;
  $tmp =~ tr/ /+/;
  $tmp = Encode::decode('utf8',$tmp);
  return($tmp);
}

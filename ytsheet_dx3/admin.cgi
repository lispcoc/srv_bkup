#!/usr/local/bin/perl
use strict;
#use warnings;
use utf8;
use open ":utf8";
use open ":std";
use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:all/;
use Encode;

##################################################

our $ver = 'admin';

#################### 設定読込 ####################

require './config.cgi';
require './file.cgi';
require $set::lib_template;

##################################################

my $admincgi = main::url(-relative, 1);
my $mode = param('mode');

if(param('pass') eq $set::masterkey)
     { &list; }
else { &form; }

exit;

##################################################

### フォーム ###
sub form {
  print "Content-type: text/html\n\n";
  print &template::_header('管理モード');
  print <<"HTML";
<div class="chara" style="width:400px;">
  <div class="box">
		<h2>管理モード</h2>
		<div class="text" style="text-align:center;">
    	<form method="post" action="./${admincgi}">
    	pass:
    	<input type="password" name="pass">
    	<input type="submit" value=" ログイン ">
  	</div>
	</div>
  </form>
</div>
HTML
  print &template::_footer;
}

### リスト ###
sub list {
  require $set::lib_template;
  print "Content-type: text/html\n\n";
  my $head_style = <<"HTML";
	<style type="text/css">
	  .chara { text-align:center; }
	  .chara .box { display:inline-block; width:auto; margin:auto; }
	  table.group { width:auto; margin:auto; }
	  table.group th { padding:5px; }
	  table.group td { padding:5px; }
	  table.group td a { margin:-5px; padding:5px; }
	  th[onclick]{ cursor:pointer; }
	</style>
  <script language="JavaScript">
  var table_sort = {
    exec: function(tid,idx,type){
      var table = document.getElementById(tid);
      var tbody = table.getElementsByTagName('tbody')[0];
      var rows = tbody.getElementsByTagName('tr');
      var sbody = document.createElement('tbody');
      
      //save array
      var srows = new Array();
      for(var i=0;i<rows.length;i++){
      srows.push({
        row: rows[i],
        cel: rows[i].getElementsByTagName('td')[idx].innerHTML,
        idx: i
      });
    }
    
    //sort array
    srows.sort(function(a,b){
      if(type == 'str')
      return a.cel < b.cel ? 1 : -1;
      else
      return b.cel - a.cel;
    });
    if(this.flag == 1) srows.reverse();
    
    //replace
    for(var i=0;i<srows.length;i++){
      sbody.appendChild(srows[i].row)
    }
    table.replaceChild(sbody,tbody);
    
    //set flag
    this.flag = this.flag > 0 ? 0 : 1;
    }
  }
  </script>
HTML
  print &template::_header('管理モード',$head_style);
  print <<"HTML";
<div class="chara">
  <div class="box">
  <table class="group" id="chara">
  <thead>
  <tr>
    <th onclick="table_sort.exec('chara',0,'num');return false;">No.</th>
    <th>シート</th>
    <th onclick="table_sort.exec('chara',2,'str');return false;">ID</th>
    <th onclick="table_sort.exec('chara',3,'str');return false;">名前</th>
    <th onclick="table_sort.exec('chara',4,'str');return false;">PL</th>
    <th onclick="table_sort.exec('chara',5,'str');return false;">更新日時</th>
  </tr>
  <thead>
  <tbody>
HTML
  my $num = 0;
  
  my %time;
  open (my $FH, '<', $set::listfile) or &error('システムエラー','データのオープンに失敗しました。');
  while (<$FH>) {
    my ($file, $time) = (split /<>/, $_)[0,2];
    $time{$file} = $time;
  }
  close($FH);
  open (my $FH, '<', $set::passfile) or &error('システムエラー','データのオープンに失敗しました。');
  while (<$FH>) {
    my ($id, undef, $url, $name, undef, $player) = split(/<>/, $_);
    $num++;
    print '<tr',($num % 2 == 0 ? ' class="rv"' : ''),'>';
    print '  <td class="R">',$num,'</td>';
    print '  <td class="C"><a target="_blank" href="',$set::datadir,$url,'.html">&#x25B6;</a></td>';
    print '  <td>',$id,'</td>';
    print '  <td class="C">',$name,'</td>';
    print '  <td>',$player,'</td>';
    my ($min,$hour,$day,$mon,$year) = (localtime($time{$url}))[1..5];
    print '  <td>',sprintf("%04d/%02d/%02d-%02d:%02d",$year+1900,$mon+1,$day,$hour,$min),'</td>';
    print '</tr>',"\n";
  }
  close($FH);
  print <<"HTML";
  </tbody>
  </table>
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

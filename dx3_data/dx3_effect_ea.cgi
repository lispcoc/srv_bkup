#!/usr/bin/perl
use FindBin;
use lib "$FindBin::Bin/../../perl5/lib/perl5";
use Text::CSV_XS; 
use utf8;
#use LWP::Simple;
use CGI;
use URI::Escape;
use Encode;
use MIME::Base64;
require "./dx3_lib.cgi";

{
  package Dx3Effect;
  
  sub new {
    my $self;              # メンバ変数を保持する連想配列
    my $class = shift;     # 第１パラメータの内容はクラス名
    my %param = @_;
    $self->{modified} = '';
    $self->{syndrome} = '';
    $self->{name} = '';
    $self->{type} = '';
    $self->{max_lv} = '';
    $self->{timing} = '';
    $self->{skill} = '';
    $self->{value} = '';
    $self->{difficulty} = '';
    $self->{target} = '';
    $self->{range} = '';
    $self->{dummy} = '';
    $self->{limit} = '';
    $self->{effect} = '';
    
    my $self = bless {
      # ハッシュに初期値を設定する。
      modified   => $param{modified},
      syndrome   => $param{syndrome},
      name       => $param{name},
      type       => $param{type},
      max_lv     => $param{max_lv},
      timing     => $param{timing},
      skill      => $param{skill},
      value      => $param{value},
      difficulty => $param{difficulty},
      target     => $param{target},
      range      => $param{range},
      dummy      => $param{dummy},
      limit      => $param{limit},
      effect     => $param{effect},
    }, $class;
    # 生成したハッシュのリファレンスを返す。
    return $self;
  }
  
  sub is_valid {
      my $self = shift;
      if ($self->{modified} eq "-" || $self->{modified} eq "新規"
          || $self->{modified} eq "改定" || $self->{modified} eq "旧") {
        return 1;
      }
      else {
        return 0;
      }
  }
  
  sub modified {
    my $self = shift;
    return $self->replace_html($self->{modified});
  }
  
  sub syndrome {
    my $self = shift;
    return $self->replace_html($self->{syndrome});
  }
  
  sub name {
    my $self = shift;
    return $self->replace_html($self->{name});
  }
  
  sub type {
    my $self = shift;
    return $self->replace_html($self->{type});
  }
  
  sub max_lv {
      my $self = shift;
      return $self->replace_html($self->{max_lv});
  }
  
  sub timing {
      my $self = shift;
      return $self->replace_html($self->{timing});
  }
  
  sub skill {
      my $self = shift;
      return $self->replace_html($self->{skill});
  }
  
  sub skill_raw {
      my $self = shift;
      return $self->{skill};
  }
  
  sub value {
      my $self = shift;
      return $self->replace_html($self->{value});
  }
  
  sub difficulty {
      my $self = shift;
      return $self->replace_html($self->{difficulty});
  }
  
  sub target {
      my $self = shift;
      return $self->replace_html($self->{target});
  }
  
  sub range {
      my $self = shift;
      return $self->replace_html($self->{range});
  }
  
  sub limit {
      my $self = shift;
      return $self->replace_html($self->{limit});
  }
  
  sub effect {
      my $self = shift;
      return $self->replace_html($self->{effect});
  }

  sub effect_raw {
      my $self = shift;
      return $self->{effect};
  }
  
  sub replace_html {
      my $self = shift;
      my $str = shift;
      $str =~ s/&/&amp;/g;
      $str =~ s/</&lt;/g;
      $str =~ s/>/&gt;/g;
      return $str;
  }
  
}

my $q = new CGI;
my $view_mode = $q->param('view_mode');
my $key = decode_utf8($q->param('key'));
my $simple = $q->param('simple');

my $url  = "https://docs.google.com/spreadsheets/d/1JnCyspi76_ZVL7wgGLOVwP2gjJ65_NT16oF4zChwKfY/export?format=csv&gid=898517267";
my $file = "data_ea.csv";
my @filestat = stat $file;
my $last_update = $filestat[9];
#my $ua = LWP::UserAgent->new;
my $csv_is_update = 0;

#if (time - $last_update > 300) {
#  my $res = $ua->get($url);
#  open (OUT, ">$file");
#  if (flock(OUT, 6)) {
#    print OUT $res->content;
#  }
#  close (OUT);
#  $csv_is_update = 1;
#}

binmode(STDOUT, ":utf8");

#my $file = 'data.csv';
my %effects;

open (IN, "<style.css");
@css = <IN>;
close (IN);

open ($fh, "<$file");

my $csv = Text::CSV_XS->new({binary => 1, eol => $/});

while (my $row = $csv->getline($fh)) {
  my ($modified, $syndrome, $name, $type, $max_lv, $timing, $skill, $value, $difficulty, $target, $range, $limit, $effect) = @$row;
  my $new_effect = Dx3Effect->new (
                 modified => $modified,
                 syndrome => $syndrome,
                 name => $name,
                 type => $type,
                 max_lv => $max_lv,
                 timing => $timing,
                 skill => $skill,
                 value => $value,
                 difficulty => $difficulty,
                 target => $target,
                 range => $range,
                 dummy => $dummy,
                 limit => $limit,
                 effect => $effect
                 );
                 
  if ($new_effect->is_valid) {
    if (!$effects{$syndrome}) {
      my @array;
      $effects{$syndrome} = \@array;
    }
    push (@{$effects{$syndrome}}, $new_effect) ;
  }
}

print "Content-Type: text/html; charset=UTF-8\n\n";
print <<"EOF";
<html>
<body>
<head>
<meta name="viewport" content="width=480" />
<title>ダブルクロス The 3rd Edition エフェクト一覧</title>
<style type="text/css">
EOF
foreach (@css) {
  print;
}
print <<"EOF";
</style>
</head>
EOF

print "<p><a href=http://ik1-329-24633.vs.sakura.ne.jp/onj/dx3_data/>データ置き場に戻る</a></p>";
print "". (&last_update ($file)) . "<br>\n";

if ($view_mode ne "new") {
  print "<b>";
}
print "<a href=dx3_effect_ea.cgi?view_mode=old&simple=$simple>基本ルルブ版</a>";
if ($view_mode ne "new") {
  print "</b>";
}
print " / ";
if ($view_mode eq "new") {
  print "<b>";
}
print "<a href=dx3_effect_ea.cgi?view_mode=new&simple=$simple>エフェクトアーカイブ版</a><br>";
if ($view_mode eq "new") {
  print "</b>";
}

print "<a href=dx3_effect_ea.cgi?view_mode=$view_mode&simple=$simple>すべて</a> / ";
foreach my $key_syndrome (sort keys (%effects)) {
  print "<a href=dx3_effect_ea.cgi?key=$key_syndrome&view_mode=$view_mode&simple=$simple>$key_syndrome</a> / ";
}
print "<br>\n";
if ($simple eq "yes") {
  print "<b>";
}
print "<a href=dx3_effect_ea.cgi?key=$key&view_mode=old&simple=yes>簡易表示</a>";
if ($simple eq "yes") {
  print "</b>";
}
print " / ";
if ($simple ne "yes") {
  print "<b>";
}
print "<a href=dx3_effect_ea.cgi?key=$key&view_mode=old&simple=no>通常表示</a>";
if ($simple ne "yes") {
  print "</b>";
}

foreach my $key_syndrome (sort keys (%effects)) {
  if ($key) {
    if ($key ne $key_syndrome) {
      next;
    }
  }
  @effects_in_syndrome = @{$effects{$key_syndrome}};
  print "<hr>\n";
  print "<h3><a name=$key_syndrome>$key_syndrome</a></h3>\n";
  if ($simple eq "yes") {
    print "<table class='type02'>\n";
    print "<tbody>\n";
  }
  foreach $effect (@effects_in_syndrome) {
    my $title_color = "#eee";
    if (!$effect->is_valid) {
      next;
    }
    my $display_name = $effect->name;
    if ($view_mode eq "new") {
      if ($effect->modified ne "-") {
        $display_name .= "(" . $effect->modified . ")";
      }
      if ($effect->modified eq "新規") {
        $display_name = "<font color=red>" . $display_name . "</font>";
      }
      if ($effect->modified eq "改定") {
        $display_name = "<font color=blue>" . $display_name . "</font>";
      }
      if ($effect->modified eq "旧") {
        $display_name = "<font color=gray>" . $display_name . "</font>";
      }
    }
    else {
      if ($effect->modified eq "新規" || $effect->modified eq "改定") {
        next;
      }
    }
    
    if ($effect->type eq "イージー") {
      $title_color = "lightgreen";
    }
    if ($effect->type eq "エネミー") {
      $title_color = "LightPink";
    }
    if ($simple eq "yes") {
      print "<tr><th rowspan=3 bgcolor=$title_color>".$display_name.
      "<br><br><font size=-1>" . $key_syndrome. "/" .$effect->type ."</font></th>";
      print "<td>".$effect->max_lv."</td>";
      print "<td>".$effect->timing."</td>";
      print "<td>".$effect->skill."</td>";
      print "<td>".$effect->difficulty."</td></tr>";
      print "<tr><td>".$effect->target."</td>";
      print "<td>".$effect->range."</td>";
      print "<td>".$effect->value."</td>";
      print "<td>".$effect->limit."</td></tr>";
      print "<tr><td colspan=8>".$effect->effect."</td></tr>";
    }
    else {
      print "<table class='type02'>\n";
      print "<tbody>\n";
      print "<tr><th rowspan=6 bgcolor=$title_color>".$display_name."<br><br><font size=-1>" . $key_syndrome. "/" .$effect->type ."</font></th><td colspan=2>最大Lv:".$effect->max_lv."</td></tr>";
      print "<tr><td colspan=2>タイミング:".$effect->timing."</td></tr>";
      print "<tr><td>技能:".$effect->skill."</td><td>難易度:".$effect->difficulty."</td></tr>";
      print "<tr><td>対象:".$effect->target."</td><td>射程:".$effect->range."</td></tr>\n";
      print "<tr><td>侵蝕率:".$effect->value."</td><td>制限:".$effect->limit."</td></tr>";
      print "<tr><td colspan=2>".$effect->effect."</td></tr>\n";
  #    print "<tr><td rowspan=2>". $effect->type ."</td><th>".$display_name."</th><td>".$effect->timing."</td><td>".$effect->max_lv."</td><td>".$effect->skill."</td><td>".$effect->value."</td><td>".$effect->difficulty."</td><td>".$effect->target."</td><td>".$effect->range."</td><td>".$effect->limit."</td></tr>\n";
  #    print "<tr><td colspan=100>".$effect->effect."</td></tr>\n";
      print "</tbody>\n";
      print "</table>\n";
    }
  }
  if ($simple eq "yes") {
    print "</tbody>\n";
    print "</table>\n";
  }
}
  
print <<"EOF";
<p>
<script type="text/javascript">
document.write('<scr'+'ipt type="text/javascript" src="http://ad.ddo.jp/728x90.js.php?ddo_id=lisp-trpg&ddo_i='+Math.floor((new Date()).getTime()/1000/60)+'"><'+'/scr'+'ipt>');
</script>
</p>
</body>
</html>
EOF

close (OUT);

if ($csv_is_update) {
  generate_js (\%effects, "auto_ea.js");
}

sub last_update{
  my ($sec, $min, $hour, $mday, $mon, $year) = localtime((stat shift)[9]); 
  $year = $year + 1900;
  $mon= $mon + 1;
  return "Last update : ".$year."/".$mon."/".$mday." ".$hour.":".$min.":".$sec;
}

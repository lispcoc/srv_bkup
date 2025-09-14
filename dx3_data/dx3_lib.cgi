#!/usr/bin/perl
use utf8;
use MIME::Base64;
use FindBin;
use lib "$FindBin::Bin/../../perl5/lib/perl5";

sub generate_js {
  my $debug = 0;

  my ($arg1, $arg2) = @_;
  my $tmp = $arg1;
  my $file = $arg2;
  my %effects = %{$tmp};
  my @csv;
  foreach my $key_syndrome (sort keys (%effects)) {
    my @effects_in_syndrome = @{$effects{$key_syndrome}};
    foreach my $effect (@effects_in_syndrome) {
      if ($effect->{modified} eq "旧") {
        next;
      }
      my $enc_desc = encode_base64(encode_utf8($effect->{effect}));
      my $line = "  " . '{ "name" : "' . $effect->{name} . '", "skill" : "' . $effect->{skill} . '", "timing" : "' . $effect->{timing} . '", "difficulty" : "' . $effect->{difficulty} . '", "target" : "' . $effect->{target} . '", "range" : "' . $effect->{range} . '", "cost" : "' . $effect->{value} . '", "limit" : "' . $effect->{limit} . '", "desctiption" : "' . $enc_desc . '", },';
      $line =~ s/(\r\n|\r|\n)//g;
      push (@csv, $line);
    }
  }
  open (OUT, ">" . $file);
  if ($debug) {
    print OUT "var data =[\n";
  }
  foreach my $line (@csv) {
    print OUT "$line\n";
  }
  if ($debug) {
    print OUT "];\n";
    print OUT <<'EOF';
var arts = document.getElementById("arts").tBodies[0].rows;

for (var i = 0, l = arts.length; i < l; i++) {
  data.forEach (
    function(value) {
      if (document.getElementById(arts[i].id + SEP + "name").value == value.name) {
        document.getElementById(arts[i].id + SEP + "type").value   = value.skill;
        document.getElementById(arts[i].id + SEP + "timing").value = value.timing;
        document.getElementById(arts[i].id + SEP + "judge").value  = value.difficulty;
        document.getElementById(arts[i].id + SEP + "target").value = value.target;
        document.getElementById(arts[i].id + SEP + "range").value  = value.range;
        document.getElementById(arts[i].id + SEP + "cost").value   = value.cost;
        document.getElementById(arts[i].id + SEP + "limit").value  = value.limit;
        document.getElementById(arts[i].id + SEP + "notes").value  = value.desctiption;
        if (value.type == "イージー") {
          document.getElementById(arts[i].id + SEP + "check").value = 3;
        }
        else if (value.type == "エネミー") {
          document.getElementById(arts[i].id + SEP + "check").value = 5;
        }
      }
    }
  )
}
EOF
  }
  close (OUT);
}

1;

@effs;
push(@effs, get_txt("auto_ea.js"));
push(@effs, get_txt("auto_joukyu.js"));
push(@effs, get_txt("auto_other.js"));

$json = join("", @effs);

print <<"EOF";
var data = [
$json
];

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
        document.getElementById(arts[i].id + SEP + "notes").value  = decodeURIComponent(escape(window.atob(value.desctiption)));
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

sub get_txt {
    $file = shift;
    open(IN, "<" . $file);
    @in = <IN>;
    close(IN);
    return join("", @in);
}

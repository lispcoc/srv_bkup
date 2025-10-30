const fs = require('fs')
const csv = require('csv-parser')

const files = [
  { out: 'ea', in: 'ea.csv' },
  { out: 'advanced', in: 'advanced.csv' },
  { out: 'others', in: 'others.csv' }
]

var endedFiles = 0
var effects = []

files.forEach(file => {
  var results = []
  fs.createReadStream(file.in)
    .pipe(csv())
    .on('headers', headers => {
      // Store headers for later use
      results.headers = headers
    })
    .on('data', data => {
      results.push(data)
    })
    .on('end', () => {
      results.forEach((item, index) => {
        for (key in item) {
          item[key] = item[key].replace(/</g, '〈').replace(/>/g, '〉')
        }
        // Convert "簡略効果" field to Buffer and back to string
        if (item['簡略効果'] === undefined) {
          item['簡略効果'] = ''
        }
        item['簡略効果'] = Buffer.from(item['簡略効果']).toString('base64')
      })
      var res = `var ${file.out} = \n` + JSON.stringify(results, null, 0)
      fs.writeFileSync(file.out + '.js', res)
      effects = effects.concat(results)
      endedFiles++
      if (endedFiles === files.length) {
        console.log(effects.length + ' effects processed.')
        gen_autoeffectinput(effects)
      }
    })
})

function gen_autoeffectinput (effects) {
  effects = effects.map(effect => {
	//{ "name" : "雷鳴の申し子", "skill" : "シンドローム", "timing" : "メジャー", "difficulty" : "対決", "target" : "-", "range" : "-", "cost" : "5", "limit" : "ピュアブリード", "desctiption" : "組み合わせた攻撃の攻撃力+[最大HP-現在HP] メインプロセス終了後にHP0 1シナリオLv回", },
    _effect = {}
    _effect['name'] = effect['エフェクト名']
    _effect['skill'] = effect['技能']
    _effect['timing'] = effect['タイミング']
    _effect['difficulty'] = effect['難易度']
    _effect['target'] = effect['対象']
    _effect['range'] = effect['射程']
    _effect['cost'] = effect['侵蝕値']
    _effect['limit'] = effect['制限']
    _effect['desctiption'] = effect['簡略効果']
    return _effect
  })

  var aui = `
var data = ${JSON.stringify(effects, null, 0)};
function autoeffectinput() {
  var arts = [];
  if(document.getElementById("arts")){
    arts = document.getElementById("arts").tBodies[0].rows;
  }
  for (var i = 0, l = arts.length; i < l; i++) {
    data.forEach (
      function(value) {
        console.log(value["name"]);
        if (document.getElementById(arts[i].id + SEP + "name").value == value["name"]) {
          document.getElementById(arts[i].id + SEP + "type").value   = value["skill"];
          document.getElementById(arts[i].id + SEP + "timing").value = value["timing"];
          document.getElementById(arts[i].id + SEP + "judge").value  = value["difficulty"];
          document.getElementById(arts[i].id + SEP + "target").value = value["target"];
          document.getElementById(arts[i].id + SEP + "range").value  = value["range"];
          document.getElementById(arts[i].id + SEP + "cost").value   = value["cost"];
          document.getElementById(arts[i].id + SEP + "limit").value  = value["limit"];
          document.getElementById(arts[i].id + SEP + "notes").value  = decodeURIComponent(escape(window.atob(value["desctiption"])));
          if (value["種別"] == "イージー") {
            document.getElementById(arts[i].id + SEP + "check").value = 3;
          }
          else if (value["種別"] == "エネミー") {
            document.getElementById(arts[i].id + SEP + "check").value = 5;
          }
        }
      }
    )
  }
  
  for (var i = 1; document.getElementsByName("effect" + i + "Name"); i++) {
    if(document.getElementsByName("effect" + i + "Name")){
      data.forEach (
        function(value) {
          console.log(value["name"]);
          if (document.getElementsByName("effect" + i + "Name")[0].value == value["name"]) {
            document.getElementsByName("effect" + i + "Skill")[0].value   = value["skill"];
            document.getElementsByName("effect" + i + "Timing")[0].value = value["timing"];
            document.getElementsByName("effect" + i + "Dfclty")[0].value  = value["difficulty"];
            document.getElementsByName("effect" + i + "Target")[0].value = value["target"];
            document.getElementsByName("effect" + i + "Range")[0].value  = value["range"];
            document.getElementsByName("effect" + i + "Encroach")[0].value   = value["cost"];
            document.getElementsByName("effect" + i + "Restrict")[0].value  = value["limit"];
            document.getElementsByName("effect" + i + "Note")[0].value  = decodeURIComponent(escape(window.atob(value["desctiption"])));
            var options = document.getElementsByName("effect" + i + "Type")[0].options;
            for(var j = 0; j < options.length; j++){
              if (options[j].label == value["種別"]) options[j].selected = true;
            }
          }
        }
      )
    }
  }
}

autoeffectinput();
`
  fs.writeFileSync('autoeffectinput.js', aui)
}

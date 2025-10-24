const fs = require('fs')
const csv = require('csv-parser')

const files = [
    {out: "ea", in: "ダブルクロス エフェクト - 基本ルルブ＆エフェクトアーカイブ版.csv"},
    {out: "advanced", in: "ダブルクロス エフェクト - 上級ルールブック.csv"},
    {out: "others", in: "ダブルクロス エフェクト - その他サプリ.csv"},
]

files.forEach(file => {
    var results = [];
    
    fs.createReadStream(file.in)
        .pipe(csv())
        .on('headers', (headers) => {
            // Store headers for later use
            results.headers = headers;
        })
        .on('data', (data) => {
            results.push(data);
        })
        .on('end', () => {
            results.forEach((item, index) => {
                for(key in item) {
                    item[key] = item[key].replace(/</g, '〈').replace(/>/g, '〉')
                }
                // Convert "簡略効果" field to Buffer and back to string
                item["簡略効果"] = Buffer.from(item["簡略効果"]).toString('base64');
            });
            var res = `var ${file.out} = \n` + JSON.stringify(results, null, 2);
            fs.writeFileSync(file.out + ".js", res);
        });
})

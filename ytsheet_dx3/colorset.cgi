###################### 設定 ######################
use strict;
use utf8;

package set;

our %color = (
  'chara01' => {
    'name' => 'DEFAULT GRAY',
    'name_ja' => 'デフォルトグレー',
    'frame' => {
      'back'  => '',
      'text'  => '',
      'out'   => '',
      'in'    => '',
      'link'  => '',
      'link_hover'     => '',
      'link_hover_back'=> '',
    },
    'cell' => {
      'back1' => '',
      'back2' => '',
      'text'  => '',
      'link'  => '',
      'link_back'      => '',
      'link_hover'     => '',
      'link_hover_back'=> '',
    },
    'hr' => {
      'solid'  => '',
      'groove1' => '',
      'ridge1'  => '',
      'groove2' => '',
      'ridge2'  => '',
    },
    'table' => {
      'border'  => '',
      'th_back' => '',
      'th_text' => '',
      'td_back' => '',
      'td_text' => '',
    },
    'h2' => {
      'back'   => '',
      'border' => '',
      'text'   => '',
    },
    'h3' => {
      'back'   => '',
      'border' => '',
      'text'   => '',
    }
  },

  'chara02' => {
    'name' => 'DARK CYAN',
    'name_ja' => 'ダークシアン',
    'frame' => {
      'back'  => '#307b7b',
      'text'  => '#e1ebeb',
      'link'  => '#61ebeb',
    },
    'cell' => {
      'link'  => '#224455',
    },
    'hr' => {
      'solid'  => '#203b3b',
    },
  },

  'chara03' => {
    'name' => 'DEEP PURPL',
    'name_ja' => 'ディープパープル',
    'frame' => {
      'back'  => '#403666',
      'text'  => '#d0d7df',
      'link'  => '#aa77ff',
    },
    'cell' => {
      'back1' => '#b8bbd7',
      'link'  => '#331166',
    },
    'hr' => {
      'solid'  => '#403666',
    },
  },

  'chara04' => {
    'name' => 'DARK GOLD',
    'name_ja' => 'ダークゴールド',
    'frame' => {
      'back'  => '#5e5230',
      'text'  => '#ccccbb',
      'link'  => '#efd055',
    },
    'cell' => {
      'back1' => '#cbc5a9',
      'link'  => '#553300',
    },
    'hr' => {
      'solid'  => '#5e5230',
    },
  },

  'chara05' => {
    'name' => 'ROYAL BLUE',
    'name_ja' => 'ロイヤルブルー',
    'frame' => {
      'back'  => '#4160b1',
      'link'  => '#88bbff',
    },
    'cell' => {
      'link'  => '#0033dd',
    },
    'hr' => {
      'solid'  => '#4160b1',
    }
  },

  'chara06' => {
    'name' => 'BURGUNDY',
    'name_ja' => 'バーガンディ',
    'frame' => {
      'back'  => '#6c2735',
      'link'  => '#ff5566',
    },
    'cell' => {
      'link'  => '#990011',
    },
    'hr' => {
      'solid'  => '#6c2735',
    },
  },

  'chara07' => {
    'name' => 'CERULEAN BLUE',
    'name_ja' => 'セルリアンブルー',
    'frame' => {
      'back'  => '#3470a0',
      'text'  => '#e1e7eb',
      'link'  => '#66ccff',
    },
    'cell' => {
      'link'  => '#006699',
    },
    'hr' => {
      'solid'  => '#346790',
    },
  },

  'chara08' => {
    'name' => 'BURNT UMBER',
    'name_ja' => 'バーントアンバー',
    'frame' => {
      'back'  => '#695036',
      'text'  => '#ddd7cc',
      'link'  => '#ee8844',
    },
    'cell' => {
      'back1' => '#c8b59c',
      'link'  => '#663300',
    },
    'hr' => {
      'solid'  => '#695036',
    },
  },

  'chara09' => {
    'name' => 'LOTUS PINK',
    'name_ja' => 'ロータスピンク',
    'frame' => {
      'back'  => '#be7287',
      'text'  => '#2b1020',
      'link'  => '#880022',
    },
    'cell' => {
      'back1' => '#debecc',
      'back2' => '#cea7b5',
      'link'  => '#990011',
    },
    'hr' => {
      'solid'  => '#6f3644',
    },
    'table' => {
      'th_back' => '#c68699',
    },
  },

  'chara10' => {
    'name' => 'MARVELOUS ORANGE',
    'name_ja' => 'マーベラスオレンジ',
    'frame' => {
      'back'  => '#b07750',
      'text'  => '#1b1000',
      'link'  => '#990000',
    },
    'cell' => {
      'link'  => '#884400',
    },
    'hr' => {
      'solid'  => '#b07750',
    },
    'table' => {
      'th_back' => '#b98b6c',
      'th_text' => '#000000',
    },
  },

  'chara11' => {
    'name' => 'FOREST GREEN',
    'name_ja' => 'フォレストグリーン',
    'frame' => {
      'back'  => '#3c7150',
      'link'  => '#44ee77',
    },
    'cell' => {
      'link'  => '#006622',
    },
    'hr' => {
      'solid'  => '#3c7150',
    },
  },

  'chara12' => {
    'name' => 'BLOODY RED',
    'name_ja' => 'ブラッディレッド',
    'frame' => {
      'back'  => '#6c2027',
      'text'  => '#ddd0d0',
      'link'  => '#ee7777',
    },
    'cell' => {
      'back1' => '#332222',
      'back2' => '#221111',
      'text'  => '#c0bbbb',
      'link'  => '#d05057',
    },
    'hr' => {
      'solid'  => '#766060',
    },
    'table' => {
      'border' => '#766060',
      'th_back' => '#221111',
      'th_text' => '#c0bbbb',
    },
  },

  'chara13' => {
    'name' => 'HEAVENLY BLUE',
    'name_ja' => 'ヘブンリーブルー',
    'frame' => {
      'back'  => '#68a4d9',
      'text'  => '#002030',
      'link'  => '#0055aa',
    },
    'cell' => {
      'back1' => '#bbd3e0',
      'back2' => '#95b7d0',
      'link'  => '#005599',
    },
    'hr' => {
      'solid'  => '#68a4d9',
    },
    'table' => {
      'th_back' => '#7eb0da',
    },
  },

  'chara14' => {
    'name' => 'SILVER WHITE',
    'name_ja' => 'シルバーホワイト',
    'frame' => {
      'back'  => '#a8b0b8',
      'out'   => '#ebf4fb #646c74 #646c74 #ebf4fb',
      'in'    => '#646c74 #ebf4fb #ebf4fb #646c74',
      'link'  => '#004488',
      'link_hover'     => '#ffffff',
      'link_hover_back'=> '#506070',
    },
    'cell' => {
      'back1' => '#c2c7cf',
      'back2' => '#b0b5bd',
      'link'  => '#004488',
      'link_hover'     => '#ffffff',
      'link_hover_back'=> '#506070',
    },
    'hr' => {
      'solid'  => '#506070',
    },
  },

  'chara15' => {
    'name' => 'FUCHSIA',
    'name_ja' => 'フクシア',
    'frame' => {
      'back'  => '#693a7f',
      'text'  => '#d4c3d4',
      'link'  => '#ff55ff',
    },
    'cell' => {
      'back1' => '#daa1c2',
      'back2' => '#b288b2',
      'link'  => '#990055',
    },
    'hr' => {
      'solid'  => '#693a7f',
    },
    'table' => {
      'th_back' => '#c579a6',
      'th_text' => '#000000',
    },
    'h2' => {
      'back'   => '#994477',
    },
  },

  'chara16' => {
    'name' => 'BOUGAINVILLAEA',
    'name_ja' => 'ブーゲンビリア',
    'frame' => {
      'back'  => '#973f70',
      'text'  => '#eedde0',
      'link'  => '#ff88cc',
    },
    'cell' => {
      'back1' => '#d6aabf',
      'back2' => '#cc91ad',
      'link'  => '#990044',
    },
    'hr' => {
      'solid'  => '#973f70',
    },
  },

  'chara17' => {
    'name' => 'EVER BLUE',
    'name_ja' => 'エバーブルー',
    'frame' => {
      'back'  => '#204988',
      'text'  => '#ccd2dd',
      'link'  => '#66aaee',
    },
    'cell' => {
      'back1' => '#202c50',
      'back2' => '#101f45',
      'link'  => '#66aaee',
    },
    'hr' => {
      'solid'  => '#707880',
    },
    'table' => {
      'border'  => '#707880',
      'th_back' => '#122146',
    },
    'h2' => {
      'border' => '#7080b0',
    },
  },

  'chara18' => {
    'name' => 'VIRIDIAN',
    'name_ja' => 'ヴィリディアン',
    'frame' => {
      'back'  => '#006047',
      'text'  => '#ccddd5',
      'link'  => '#00ee88',
    },
    'cell' => {
      'back1' => '#103025',
      'back2' => '#002515',
      'link'  => '#00dd99',
    },
    'hr' => {
      'solid'  => '#006047',
    },
    'table' => {
      'border'  => '#507067',
      'th_back' => '#002515',
    },
    'h2' => {
      'border' => '#509077',
    },
  },

  'chara19' => {
    'name' => 'MINT GREEN',
    'name_ja' => 'ミントグリーン',
    'frame' => {
      'back'  => '#599969',
      'text'  => '#001109',
      'link'  => '#88dd99',
    },
    'cell' => {
      'back1' => '#aaccbb',
      'back2' => '#88bba0',
      'link'  => '#007722',
    },
    'hr' => {
      'solid'  => '#599969',
    },
  },

  'chara20' => {
    'name' => 'BLACK',
    'name_ja' => 'ブラック',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#99aacc',
    },
    'cell' => {
      'back1' => '#1a1a1a',
      'back2' => '#101010',
      'link'  => '#99aacc',
    },
    'hr' => {
      'solid'  => '#666666',
    },
    'table' => {
      'border'  => '#666666',
      'th_back' => '#101010',
    },
    'h2' => {
      'border' => '#666666',
    },
  },

  'chara21' => {
    'name' => 'WISTARIA',
    'name_ja' => 'ウィスタリア',
    'frame' => {
      'back'  => '#6d70a8',
      'link'  => '#adb0ff',
    },
    'cell' => {
      'back1' => '#bbbfdd',
      'back2' => '#a0a4d0',
      'link'  => '#220077',
    },
    'hr' => {
      'solid'  => '#6d70a8',
    },
    'table' => {
      'th_back' => '#999dd0',
    },
  },

  'chara22' => {
    'name' => 'IRON BLUE',
    'name_ja' => 'アイアンブルー',
    'frame' => {
      'back'  => '#445566',
      'link'  => '#88aadd',
    },
    'cell' => {
      'back1' => '#203040',
      'back2' => '#102030',
      'link'  => '#88b4dd',
    },
    'hr' => {
      'solid'  => '#667788',
    },
    'table' => {
      'border'  => '#667788',
      'th_back' => '#334455',
    },
  },

  'chara23' => {
    'name' => 'SCARLET',
    'name_ja' => 'スカーレット',
    'frame' => {
      'back'  => '#994037',
      'text'  => '#ddd7d0',
      'link'  => '#ff8800',
    },
    'cell' => {
      'link'  => '#aa2200',
    },
    'hr' => {
      'solid'  => '#994037',
    },
    'table' => {
      'th_back' => '#bb8077',
    },
  },

  'chara24' => {
    'name' => 'GRASS GREEN',
    'name_ja' => 'グラスグリーン',
    'frame' => {
      'back'  => '#5b6d32',
      'text'  => '#dfe5d8',
      'link'  => '#88dd22',
    },
    'cell' => {
      'back1' => '#c0c7a9',
      'link'  => '#335500',
    },
    'hr' => {
      'solid'  => '#5b6d32',
    },
    'table' => {
      'th_back' => '#99aa70',
    },
  },

  'chara25' => {
    'name' => 'CHOCOLATE',
    'name_ja' => 'チョコレート',
    'frame' => {
      'back'  => '#553024',
      'text'  => '#ddd5d0',
      'link'  => '#dd6660',
    },
    'cell' => {
      'back1' => '#392520',
      'back2' => '#291410',
      'text'  => '#ddd0cc',
      'link'  => '#dd6660',
    },
    'hr' => {
      'solid'  => '#805544',
    },
    'table' => {
      'border'  => '#805544',
      'th_back' => '#2d1512',
      'th_text' => '#ddd0cc',
    },
    'h2' => {
      'border' => '#906655',
    },
  },

  'chara26' => {
    'name' => 'SLATE GRAY',
    'name_ja' => 'スレイトグレー',
    'frame' => {
      'back'  => '#556677',
      'link'  => '#88bbff',
    },
    'cell' => {
      'link'  => '#003377',
    },
    'hr' => {
      'solid'  => '#556677',
    },
    'table' => {
      'th_back' => '#8899aa',
    },
  },

  'chara27' => {
    'name' => 'GRAY ROSE',
    'name_ja' => 'グレイローズ',
    'frame' => {
      'back'  => '#775566',
      'link'  => '#ff99bb',
    },
    'cell' => {
      'link'  => '#770033',
    },
    'hr' => {
      'solid'  => '#775566',
    },
    'table' => {
      'th_back' => '#aa8899',
    },
  },

  'chara28' => {
    'name' => 'GREGE',
    'name_ja' => 'グレージュ',
    'frame' => {
      'back'  => '#776655',
      'link'  => '#ffbb99',
    },
    'cell' => {
      'link'  => '#773300',
    },
    'hr' => {
      'solid'  => '#776655',
    },
    'table' => {
      'th_back' => '#a09080',
    },
  },

  'chara29' => {
    'name' => 'ASH GREEN',
    'name_ja' => 'アッシュグリーン',
    'frame' => {
      'back'  => '#556666',
      'link'  => '#88ddbb',
    },
    'cell' => {
      'link'  => '#004422',
    },
    'hr' => {
      'solid'  => '#556666',
    },
    'table' => {
      'th_back' => '#819292',
    },
  },

  'chara30' => {
    'name' => 'LIGHT PURPLE',
    'name_ja' => 'ライトパープル',
    'frame' => {
      'back'  => '#665577',
      'link'  => '#bbaaff',
    },
    'cell' => {
      'link'  => '#330077',
    },
    'hr' => {
      'solid'  => '#665577',
    },
    'table' => {
      'th_back' => '#9281a3',
    },
  },

  'chara31' => {
    'name' => 'FIRE RED',
    'name_ja' => 'ファイアレッド',
    'frame' => {
      'back'  => '#994444',
      'text'  => '#eeddcc',
      'link'  => '#ff9911',
    },
    'cell' => {
      'back1' => '#dd9988',
      'back2' => '#dda770',
      'link'  => '#993300',
    },
    'hr' => {
      'solid'  => '#5b2826',
    },
    'table' => {
      'th_back' => '#cc7060',
      'th_text' => '#000000',
    },
  },

  'chara32' => {
    'name' => 'BLUE SKY',
    'name_ja' => 'ブルースカイ',
    'frame' => {
      'back'  => '#3344aa',
      'text'  => '#ccddee',
      'link'  => '#55bbff',
    },
    'cell' => {
      'back1' => '#99bbdd',
      'back2' => '#bbccdd',
      'link'  => '#0011ff',
    },
    'hr' => {
      'solid'  => '#3344aa',
    },
    'table' => {
      'th_back' => '#bbccdd',
    },
    'h2' => {
      'back'   => '#ccddee',
      'border' => '#3344aa',
    },
  },

  'chara33' => {
    'name' => 'LEAF GREEN',
    'name_ja' => 'リーフグリーン',
    'frame' => {
      'back'  => '#337733',
      'text'  => '#ddeecc',
      'link'  => '#55ee11',
    },
    'cell' => {
      'back1' => '#a0cc90',
      'back2' => '#b0cc90',
      'link'  => '#116600',
    },
    'hr' => {
      'solid'  => '#337733',
    },
    'table' => {
      'th_back' => '#80b070',
    },
  },

  'chara34' => {
    'name' => 'FLOWER PINK',
    'name_ja' => 'フラワーピンク',
    'frame' => {
      'back'  => '#a0505f',
      'text'  => '#eed0dd',
      'link'  => '#ffaabb',
    },
    'cell' => {
      'back1' => '#c5bbcd',
      'back2' => '#a3bba5',
      'link'  => '#442200',
      'link_back'      => '#ccc090',
      'link_hover'     => '#ffffff',
      'link_hover_back'=> '#77ccdd',
    },
    'hr' => {
      'solid'  => '#a0203f',
    },
    'table' => {
      'th_back' => '#a3bba5',
    },
    'h2' => {
      'back'   => '#b07080',
      'border' => '#a0203f',
    },
  },

  'chara35' => {
    'name' => 'IRON HEAT',
    'name_ja' => 'アイアンヒート',
    'frame' => {
      'back'  => '#442222',
      'text'  => '#ccbbbb',
      'out'   => '#555555 #000000 #000000 #555555',
      'in'    => '#000000 #555555 #555555 #000000',
      'link'  => '#ff6655',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#332222',
      'link'  => '#ff4039',
      'link_hover'     => '#ffdd77',
      'link_hover_back'=> '#ff4039',
    },
    'hr' => {
      'solid'  => '#cc4039',
    },
    'table' => {
      'border'  => '#666666',
      'th_back' => '#332222',
    },
    'h2' => {
      'border' => '#b04039',
    },
  },

  'chara36' => {
    'name' => 'BLACK SARENA',
    'name_ja' => 'ブラックサレナ',
    'frame' => {
      'back'  => '#222222',
      'text'  => '#cc88aa',
      'link'  => '#d53395',
    },
    'cell' => {
      'back1' => '#333333',
      'back2' => '#44222f',
      'link'  => '#d56695',
    },
    'hr' => {
      'solid'  => '#777777',
    },
    'table' => {
      'border'  => '#777777',
      'th_back' => '#404040',
    },
    'h2' => {
      'border' => '#777777',
      'text'   => '#cccccc',
    },
  },

  'chara37' => {
    'name' => 'PLUM',
    'name_ja' => 'プラム',
    'frame' => {
      'back'  => '#693049',
      'link'  => '#ff66aa',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#332029',
      'link'  => '#dd5599',
    },
    'hr' => {
      'solid'  => '#693049',
    },
    'table' => {
      'border'  => '#693049',
      'th_back' => '#332029',
    },
    'h2' => {
      'back'   => '#592c41',
      'border' => '#8b5f74',
    },
  },

  'chara38' => {
    'name' => 'DARK FOREST',
    'name_ja' => 'ダークフォレスト',
    'frame' => {
      'back'  => '#304930',
      'link'  => '#ccc066',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#302925',
      'link'  => '#ccc066',
    },
    'hr' => {
      'solid'  => '#556655',
    },
    'table' => {
      'border'  => '#556655',
      'th_back' => '#253325',
    },
    'h2' => {
      'border' => '#667766',
    },
  },

  'chara39' => {
    'name' => 'DEEP ROYAL PURPLE',
    'name_ja' => 'ディープロイヤルパープル',
    'frame' => {
      'back'  => '#403062',
      'link'  => '#aa66ff',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#252039',
      'link'  => '#a088ee',
    },
    'hr' => {
      'solid'  => '#664488',
    },
    'table' => {
      'border'  => '#664488',
      'th_back' => '#332744',
    },
    'h2' => {
      'border' => '#665f77',
    },
  },

  'chara40' => {
    'name' => 'DEEP SEA',
    'name_ja' => 'ディープシー',
    'frame' => {
      'back'  => '#304069',
      'text'  => '#c0cdcf',
      'link'  => '#77bbff',
    },
    'cell' => {
      'back1' => '#19202c',
      'back2' => '#202f39',
      'link'  => '#66aaff',
    },
    'hr' => {
      'solid'  => '#556077',
    },
    'table' => {
      'border'  => '#556077',
      'th_back' => '#293555',
    },
    'h2' => {
      'border' => '#667088',
    },
  },

  'chara41' => {
    'name' => 'SEA GREEN',
    'name_ja' => 'シーグリーン',
    'frame' => {
      'back'  => '#305549',
      'text'  => '#c0cdcf',
      'link'  => '#66eeaa',
    },
    'cell' => {
      'back1' => '#19202c',
      'back2' => '#202f39',
      'link'  => '#66ccbb',
    },
    'hr' => {
      'solid'  => '#557766',
    },
    'table' => {
      'border'  => '#557766',
      'th_back' => '#29453c',
    },
    'h2' => {
      'border' => '#668877',
    },
  },

  'chara42' => {
    'name' => 'BRASS GOLD',
    'name_ja' => 'ブラスゴールド',
    'frame' => {
      'back'  => '#554930',
      'link'  => '#eeaa66',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#302a20',
      'link'  => '#ccaa66',
    },
    'hr' => {
      'solid'  => '#706655',
    },
    'table' => {
      'border'  => '#706655',
      'th_back' => '#403a29',
    },
    'h2' => {
      'border' => '#807766',
    },
  },

  'chara43' => {
    'name' => 'DARK CORAL',
    'name_ja' => 'ダークコーラル',
    'frame' => {
      'back'  => '#603035',
      'link'  => '#ee5555',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#332025',
      'link'  => '#cc3333',
    },
    'hr' => {
      'solid'  => '#775555',
    },
    'table' => {
      'border'  => '#775555',
      'th_back' => '#49292d',
    },
    'h2' => {
      'border' => '#886666',
    },
  },

  'chara44' => {
    'name' => 'LAMP BLACK',
    'name_ja' => 'ランプブラック',
    'frame' => {
      'back'  => '#352925',
      'text'  => '#cccccc',
      'link'  => '#ee6055',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#291c19',
      'link'  => '#cc5033',
    },
    'hr' => {
      'solid'  => '#776055',
    },
    'table' => {
      'border'  => '#776055',
      'th_back' => '#302522',
    },
    'h2' => {
      'border' => '#887066',
    },
  },

  'chara45' => {
    'name' => 'MAUVE',
    'name_ja' => 'モーブ',
    'frame' => {
      'back'  => '#553955',
      'link'  => '#ee60ee',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#291b29',
      'link'  => '#cc50cc',
    },
    'hr' => {
      'solid'  => '#776677',
    },
    'table' => {
      'border'  => '#776677',
      'th_back' => '#403040',
    },
    'h2' => {
      'border' => '#887888',
    },
  },

  'chara46' => {
    'name' => 'DARK SLATE GRAY',
    'name_ja' => 'ダークスレイトグレー',
    'frame' => {
      'back'  => '#394955',
      'link'  => '#77ccee',
    },
    'cell' => {
      'back1' => '#191c22',
      'back2' => '#1b2229',
      'link'  => '#77aacc',
    },
    'hr' => {
      'solid'  => '#667077',
    },
    'table' => {
      'border'  => '#667077',
      'th_back' => '#2c3740',
    },
    'h2' => {
      'border' => '#778088',
    },
  },

  'chara47' => {
    'name' => 'BLACK + RED',
    'name_ja' => 'ブラック＋レッド',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#dd5555',
    },
    'cell' => {
      'back1' => '#d3b1b1',
      'back2' => '#cd8989',
      'link'  => '#880000',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#cd8989',
    },
  },

  'chara48' => {
    'name' => 'BLACK + ORANGE',
    'name_ja' => 'ブラック＋オレンジ',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#dd9955',
    },
    'cell' => {
      'back1' => '#c9b8a7',
      'back2' => '#b99775',
      'link'  => '#743a00',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#b99775',
    },
  },

  'chara49' => {
    'name' => 'BLACK + YELLOW',
    'name_ja' => 'ブラック＋イエロー',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#dddd55',
    },
    'cell' => {
      'back1' => '#bfbf9d',
      'back2' => '#a5a561',
      'link'  => '#555500',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#a5a561',
    },
  },

  'chara50' => {
    'name' => 'BLACK + LEAF',
    'name_ja' => 'ブラック＋リーフ',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#99dd55',
    },
    'cell' => {
      'back1' => '#b3c4a2',
      'back2' => '#8daf6b',
      'link'  => '#336600',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#8daf6b',
    },
  },

  'chara51' => {
    'name' => 'BLACK + GREEN',
    'name_ja' => 'ブラック＋グリーン',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#55dd55',
    },
    'cell' => {
      'back1' => '#a7c9a7',
      'back2' => '#75b975',
      'link'  => '#005500',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#75b975',
    },
  },

  'chara52' => {
    'name' => 'BLACK + TURQUOISE',
    'name_ja' => 'ブラック＋ターコイズ',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#55dd99',
    },
    'cell' => {
      'back1' => '#a5c7b6',
      'back2' => '#71b593',
      'link'  => '#006633',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#71b593',
    },
  },

  'chara53' => {
    'name' => 'BLACK + CYAN',
    'name_ja' => 'ブラック＋シアン',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#55dddd',
    },
    'cell' => {
      'back1' => '#a3c5c5',
      'back2' => '#6cb0b0',
      'link'  => '#006666',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#6cb0b0',
    },
  },

  'chara54' => {
    'name' => 'BLACK + BLUE',
    'name_ja' => 'ブラック＋ブルー',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#5599dd',
    },
    'cell' => {
      'back1' => '#adbecf',
      'back2' => '#82a4c6',
      'link'  => '#004488',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#82a4c6',
    },
  },

  'chara55' => {
    'name' => 'BLACK + WISTARIA',
    'name_ja' => 'ブラック＋ウィスタリア',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#5555dd',
    },
    'cell' => {
      'back1' => '#b7b7d9',
      'back2' => '#9696da',
      'link'  => '#0000bb',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#9696da',
    },
  },

  'chara56' => {
    'name' => 'BLACK + VIOLET',
    'name_ja' => 'ブラック＋バイオレット',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#9955dd',
    },
    'cell' => {
      'back1' => '#c3b2d4',
      'back2' => '#ad8bcf',
      'link'  => '#440088',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#ad8bcf',
    },
  },

  'chara57' => {
    'name' => 'BLACK + PURPLE',
    'name_ja' => 'ブラック＋パープル',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#dd55dd',
    },
    'cell' => {
      'back1' => '#d0aed0',
      'back2' => '#c581c5',
      'link'  => '#770077',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#c581c5',
    },
  },

  'chara58' => {
    'name' => 'BLACK + PINK',
    'name_ja' => 'ブラック＋ピンク',
    'frame' => {
      'back'  => '#333333',
      'link'  => '#dd5599',
    },
    'cell' => {
      'back1' => '#d1afc0',
      'back2' => '#c985a7',
      'link'  => '#800040',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#c985a7',
    },
  },

  'chara59' => {
    'name' => 'WHITE + RED',
    'name_ja' => 'ホワイト＋レッド',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#880000',
    },
    'cell' => {
      'back1' => '#d3b1b1',
      'back2' => '#cd8989',
      'link'  => '#880000',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#cd8989',
    },
  },

  'chara60' => {
    'name' => 'WHITE + ORANGE',
    'name_ja' => 'ホワイト＋オレンジ',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#743a00',
    },
    'cell' => {
      'back1' => '#c9b8a7',
      'back2' => '#b99775',
      'link'  => '#743a00',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#b99775',
    },
  },

  'chara61' => {
    'name' => 'WHITE + YELLOW',
    'name_ja' => 'ホワイト＋イエロー',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#555500',
    },
    'cell' => {
      'back1' => '#bfbf9d',
      'back2' => '#a5a561',
      'link'  => '#555500',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#a5a561',
    },
  },

  'chara62' => {
    'name' => 'WHITE + LEAF',
    'name_ja' => 'ホワイト＋リーフ',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#336600',
    },
    'cell' => {
      'back1' => '#b3c4a2',
      'back2' => '#8daf6b',
      'link'  => '#336600',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#8daf6b',
    },
  },

  'chara63' => {
    'name' => 'WHITE + GREEN',
    'name_ja' => 'ホワイト＋グリーン',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#005500',
    },
    'cell' => {
      'back1' => '#a7c9a7',
      'back2' => '#75b975',
      'link'  => '#005500',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#75b975',
    },
  },

  'chara64' => {
    'name' => 'WHITE + TURQUOISE',
    'name_ja' => 'ホワイト＋ターコイズ',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#006633',
    },
    'cell' => {
      'back1' => '#a5c7b6',
      'back2' => '#71b593',
      'link'  => '#006633',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#71b593',
    },
  },

  'chara65' => {
    'name' => 'WHITE + CYAN',
    'name_ja' => 'ホワイト＋シアン',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#006666',
    },
    'cell' => {
      'back1' => '#a3c5c5',
      'back2' => '#6cb0b0',
      'link'  => '#006666',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#6cb0b0',
    },
  },

  'chara66' => {
    'name' => 'WHITE + BLUE',
    'name_ja' => 'ホワイト＋ブルー',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#004488',
    },
    'cell' => {
      'back1' => '#adbecf',
      'back2' => '#82a4c6',
      'link'  => '#004488',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#82a4c6',
    },
  },

  'chara67' => {
    'name' => 'WHITE + WISTARIA',
    'name_ja' => 'ホワイト＋ウィスタリア',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#0000bb',
    },
    'cell' => {
      'back1' => '#b7b7d9',
      'back2' => '#9696da',
      'link'  => '#0000bb',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#9696da',
    },
  },

  'chara68' => {
    'name' => 'WHITE + VIOLET',
    'name_ja' => 'ホワイト＋バイオレット',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#440088',
    },
    'cell' => {
      'back1' => '#c3b2d4',
      'back2' => '#ad8bcf',
      'link'  => '#440088',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#ad8bcf',
    },
  },

  'chara69' => {
    'name' => 'WHITE + PURPLE',
    'name_ja' => 'ホワイト＋パープル',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#770077',
    },
    'cell' => {
      'back1' => '#d0aed0',
      'back2' => '#c581c5',
      'link'  => '#770077',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#c581c5',
    },
  },

  'chara70' => {
    'name' => 'WHITE + PINK',
    'name_ja' => 'ホワイト＋ピンク',
    'frame' => {
      'back'  => '#bbbbbb',
      'link'  => '#800040',
    },
    'cell' => {
      'back1' => '#d1afc0',
      'back2' => '#c985a7',
      'link'  => '#800040',
    },
    'hr' => {
      'solid'  => '#444444',
    },
    'table' => {
      'th_back' => '#c985a7',
    },
  },

  'chara71' => {
    'name' => 'WINE RED',
    'name_ja' => 'ワインレッド',
    'frame' => {
      'back'  => '#602037',
      'text'  => '#ccb0b5',
      'link'  => '#ff4466',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#333333',
      'link'  => '#ff4466',
    },
    'hr' => {
      'solid'  => '#ccb0b5',
    },
    'table' => {
      'border'  => '#80485b',
      'th_back' => '#39212a',
    },
    'h2' => {
      'border' => '#ccb0b5',
    },
  },

  'chara72' => {
    'name' => 'VALENTINE RED',
    'name_ja' => 'バレンタインレッド',
    'frame' => {
      'back'  => '#772030',
      'text'  => '#ddbbcc',
      'link'  => '#ff7799',
    },
    'cell' => {
      'back1' => '#392722',
      'back2' => '#2d1a17',
      'text'  => '#cfc3c3',
      'link'  => '#ff7799',
    },
    'hr' => {
      'solid'  => '#aa6688',
    },
    'table' => {
      'border'  => '#906070',
      'th_back' => '#291715',
    },
    'h2' => {
      'back'   => '#66212c',
      'border' => '#bb8899',
    },
  },

  'chara73' => {
    'name' => 'VALENTINE PINK',
    'name_ja' => 'バレンタインピンク',
    'frame' => {
      'back'  => '#a04858',
      'text'  => '#dfd3d3',
      'link'  => '#ff99aa',
    },
    'cell' => {
      'back1' => '#392722',
      'back2' => '#2d1a17',
      'link'  => '#ff99aa',
    },
    'hr' => {
      'solid'  => '#aa7788',
    },
    'table' => {
      'border'  => '#906070',
      'th_back' => '#291715',
    },
    'h2' => {
      'back'   => '#843e49',
      'border' => '#cc99aa',
    },
  },

  'chara74' => {
    'name' => 'XMAS RED+GREEN',
    'name_ja' => 'クリスマスレッド＋グリーン',
    'frame' => {
      'back'  => '#702030',
      'link'  => '#ddcc55',
    },
    'cell' => {
      'back1' => '#293325',
      'back2' => '#1b2717',
      'link'  => '#ddcc55',
    },
    'hr' => {
      'solid'  => '#aa7788',
    },
    'table' => {
      'border'  => '#808080',
      'th_back' => '#5c242c',
    },
    'h2' => {
      'border' => '#aa7788',
    },
  },

  'eva00' => {
    'name' => 'E-00 YELLOW',
    'name_ja' => '零号機イエロー',
    'frame' => {
      'back'  => '#906f30',
      'text'  => '#ddddc0',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#55dd66',
      'link_hover'     => '#55dd66',
      'link_hover_back'=> '#008811',
    },
    'cell' => {
      'back1' => '#cccdd0',
      'back2' => '#99a5af',
      'link'  => '#880022',
      'link_hover'     => '#ffbbcc',
      'link_hover_back'=> '#cc0022',
    },
    'hr' => {
      'solid'  => '#772222',
    },
    'table' => {
      'th_back' => '#ac8c50',
    },
  },

  'eva01' => {
    'name' => 'E-01 PURPLE',
    'name_ja' => '初号機パープル',
    'frame' => {
      'back'  => '#564580',
      'text'  => '#88dd88',
      'link'  => '#ccaa22',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#333333',
      'link'  => '#cc8822',
    },
    'hr' => {
      'solid'  => '#888888',
    },
    'table' => {
      'border'  => '#888888',
      'th_back' => '#366336',
    },
    'h2' => {
      'back'   => '#3b703b',
    },
  },

  'eva02' => {
    'name' => 'E-02 RED',
    'name_ja' => '2号機レッド',
    'frame' => {
      'back'  => '#8c3030',
      'text'  => '#e0c0a0',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#00bb44',
    },
    'cell' => {
      'back1' => '#cccccc',
      'back2' => '#cca575',
      'link'  => '#007722',
    },
    'hr' => {
      'solid'  => '#772222',
    },
    'table' => {
      'th_back' => '#cca070',
    },
    'h2' => {
      'back'   => '#c07044',
      'text'   => '#efe7e0',
    },
  },

  'eva03' => {
    'name' => 'E-03 BLACK',
    'name_ja' => '3号機ブラック',
    'frame' => {
      'back'  => '#353f55',
      'link'  => '#66bb66',
      'link_hover'     => '#22c2e2',
      'link_hover_back'=> '#1111a1',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#331315',
      'link'  => '#66bb66',
      'link_hover'     => '#22c2e2',
      'link_hover_back'=> '#1111a1',
    },
    'hr' => {
      'solid'  => '#833333',
    },
    'table' => {
      'border'  => '#666677',
      'th_back' => '#331315',
    },
    'h2' => {
      'back'   => '#a0a0a0',
      'border' => '#dddddd',
    },
  },

  'eva04' => {
    'name' => 'E-04 SILVER',
    'name_ja' => '4号機シルバー',
    'frame' => {
      'back'  => '#878795',
      'text'  => '#600005',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#000000',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#331315',
      'link'  => '#cc8822',
    },
    'hr' => {
      'solid'  => '#644040',
    },
    'table' => {
      'border'  => '#757080',
      'th_back' => '#484058',
    },
    'h2' => {
      'border' => '#dddddd',
      'text'   => '#eeeeee',
    },
  },

  'eva05' => {
    'name' => 'E-05 GREEN',
    'name_ja' => '5号機グリーン',
    'frame' => {
      'back'  => '#506040',
      'text'  => '#ccb050',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#77cc22',
    },
    'cell' => {
      'back1' => '#b0b8bf',
      'back2' => '#9098a0',
      'link'  => '#000000',
      'link_back' => '#90bb80',
      'link_hover'     => '#222222',
      'link_hover_back'=> '#ccaa22',
    },
    'hr' => {
      'solid'  => '#733036',
    },
    'table' => {
      'th_back' => '#66393b',
      'th_text' => '#ccb060',
    },
    'h2' => {
      'back'   => '#b09960',
    },
  },

  'eva06' => {
    'name' => 'E-06 BLUE',
    'name_ja' => 'Mark.06 ブルー',
    'frame' => {
      'back'  => '#283259',
      'text'  => '#bb9955',
      'link'  => '#dd4455',
    },
    'cell' => {
      'back1' => '#202530',
      'back2' => '#151c25',
      'link'  => '#dd4455',
    },
    'hr' => {
      'solid'  => '#997050',
    },
    'table' => {
      'border'  => '#586078',
      'th_back' => '#151c25',
    },
    'h2' => {
      'back'   => '#997050',
      'border' => '#bbaa80',
      'text'   => '#000000',
    },
  },

  'gn00exi' => {
    'name' => 'EXIA BLUE',
    'name_ja' => 'エクシアブルー',
    'frame' => {
      'back'  => '#4060a0',
      'text'  => '#99ddbb',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#ddbb00',
    },
    'cell' => {
      'back1' => '#bbbbbf',
      'back2' => '#bb8899',
      'link'  => '#004422',
      'link_back'      => '#99bbaa',
    },
    'table' => {
      'th_back' => '#9999aa',
    },
    'h2' => {
      'text'   => '#ddbb66',
    },
  },

  'kr10dcd' => {
    'name' => 'DCD MAGENTA',
    'name_ja' => 'ディケイドマゼンタ',
    'frame' => {
      'back'  => '#a05070',
      'text'  => '#000000',
      'in'    => '#505050 #a0a0a0 #a0a0a0 #505050',
      'link'  => '#ffbb33',
    },
    'cell' => {
      'back1' => '#222222',
      'back2' => '#224835',
      'link'  => '#d33333',
    },
    'hr' => {
      'solid'  => '#777777',
    },
    'table' => {
      'border'  => '#777777',
      'th_back' => '#555555',
    },
    'h2' => {
      'back'   => '#aaaaaa',
      'border' => '#777777',
    },
  },

  'kr11cj' => {
    'name' => 'CYCLONE JOKER',
    'name_ja' => 'サイクロンジョーカー',
    'frame' => {
      'back'  => '#333333',
      'text'  => '#b388dd',
      'link'  => '#b22222',
    },
    'cell' => {
      'back1' => '#90c0a0',
      'back2' => '#a0bb90',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#a0bb90',
    },
    'h2' => {
      'back'   => '#404040',
      'text'   => '#b596dd',
    },
    'h3' => {
      'back'   => '#505050',
      'text'   => '#bb99dd',
    },
  },

  'kr11cm' => {
    'name' => 'CYCLONE METAL',
    'name_ja' => 'サイクロンメタル',
    'frame' => {
      'back'  => '#777777',
      'text'  => '#e0e0e0',
      'out'   => '#bbbbbb #333333 #333333 #bbbbbb',
      'in'    => '#333333 #bbbbbb #bbbbbb #333333',
      'link'  => '#800000',
    },
    'cell' => {
      'back1' => '#90c0a0',
      'back2' => '#a0bb90',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#99bb88',
    },
  },

  'kr11ct' => {
    'name' => 'CYCLONE TRIGGER',
    'name_ja' => 'サイクロントリガー',
    'frame' => {
      'back'  => '#3050a0',
      'text'  => '#aaccdd',
      'link'  => '#c44444',
    },
    'cell' => {
      'back1' => '#90c0a0',
      'back2' => '#a0bb90',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#99bb88',
    },
  },

  'kr11hj' => {
    'name' => 'HEAT JOKER',
    'name_ja' => 'ヒートジョーカー',
    'frame' => {
      'back'  => '#702029',
      'text'  => '#d0a080',
      'link'  => '#d55555',
    },
    'cell' => {
      'back1' => '#303030',
      'back2' => '#403050',
      'link'  => '#e44444',
    },
    'hr' => {
      'solid'  => '#707070',
    },
    'table' => {
      'border'  => '#707070',
      'th_back' => '#403050',
    },
    'h2' => {
      'border' => '#c09070',
    },
    'h3' => {
      'border' => '#c09070',
    }
  },

  'kr11hm' => {
    'name' => 'HEAT METAL',
    'name_ja' => 'ヒートメタル',
    'frame' => {
      'back'  => '#702029',
      'text'  => '#d0a080',
      'in'    => '#666666 #eeeeee #eeeeee #666666',
      'link'  => '#d55555',
    },
    'cell' => {
      'back1' => '#aaaaaa',
      'back2' => '#c3c3c3',
      'link'  => '#900000',
    },
    'hr' => {
      'solid'  => '#707070',
    },
    'table' => {
      'th_back' => '#c3c3c3',
    },
    'h2' => {
      'border' => '#c09070',
    },
    'h3' => {
      'border' => '#c09070',
    }
  },

  'kr11ht' => {
    'name' => 'HEAT TRRIGER',
    'name_ja' => 'ヒートトリガー',
    'frame' => {
      'back'  => '#702029',
      'text'  => '#d0a080',
      'in'    => '#000000 #666666 #666666 #000000',
      'link'  => '#d55555',
    },
    'cell' => {
      'back1' => '#7090cc',
      'back2' => '#88aacc',
      'text'  => '#000000',
      'link'  => '#800000',
    },
    'hr' => {
      'solid'  => '#707070',
    },
    'table' => {
      'th_back' => '#88aacc',
    },
    'h2' => {
      'border' => '#c09070',
    },
    'h3' => {
      'border' => '#c09070',
    }
  },

  'kr11lj' => {
    'name' => 'LUNA JOKER',
    'name_ja' => 'ルナジョーカー',
    'frame' => {
      'back'  => '#333333',
      'text'  => '#b388dd',
      'link'  => '#b22222',
    },
    'cell' => {
      'back1' => '#c0bb90',
      'back2' => '#bba880',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#bba888',
    },
    'h2' => {
      'back'   => '#404040',
      'text'   => '#b596dd',
    },
    'h3' => {
      'back'   => '#505050',
      'text'   => '#bb99dd',
    },
  },

  'kr11lm' => {
    'name' => 'LUNA METAL',
    'name_ja' => 'ルナメタル',
    'frame' => {
      'back'  => '#777777',
      'text'  => '#e0e0e0',
      'out'   => '#bbbbbb #333333 #333333 #bbbbbb',
      'in'    => '#333333 #bbbbbb #bbbbbb #333333',
      'link'  => '#800000',
    },
    'cell' => {
      'back1' => '#c0bb90',
      'back2' => '#bba880',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#bba880',
    },
  },

  'kr11lt' => {
    'name' => 'LUNA TRIGGER',
    'name_ja' => 'ルナトリガー',
    'frame' => {
      'back'  => '#3050a0',
      'text'  => '#aaccdd',
      'link'  => '#c44444',
    },
    'cell' => {
      'back1' => '#c0bb90',
      'back2' => '#bba880',
      'link'  => '#800000',
    },
    'table' => {
      'th_back' => '#bba880',
    },
  },

  'kr11fj' => {
    'name' => 'FANG JOKER',
    'name_ja' => 'ファングジョーカー',
    'frame' => {
      'back'  => '#333333',
      'text'  => '#b388dd',
      'link'  => '#b22222',
    },
    'cell' => {
      'back1' => '#c0c0c0',
      'link'  => '#900000',
    },
    'table' => {
      'th_back' => '#505050',
    },
    'h2' => {
      'back'   => '#404040',
    },
    'h3' => {
      'back'   => '#505050',
    },
  },

);

1;
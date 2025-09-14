var d_c = self.document.chr;

function calc(){
	var Syndrome1 = d_c.syndrome1.options[d_c.syndrome1.selectedIndex].value;
	var Syndrome2 = d_c.syndrome2.options[d_c.syndrome2.selectedIndex].value;
	var Syndrome3 = d_c.syndrome3.options[d_c.syndrome3.selectedIndex].value;
	
	if(Syndrome1){
		var SttSyn1Body   = Syn[Syndrome1][0]; document.getElementById("SttSyn1Body").innerHTML   = SttSyn1Body;
		var SttSyn1Sense  = Syn[Syndrome1][1]; document.getElementById("SttSyn1Sense").innerHTML  = SttSyn1Sense;
		var SttSyn1Spirit = Syn[Syndrome1][2]; document.getElementById("SttSyn1Spirit").innerHTML = SttSyn1Spirit;
		var SttSyn1Social = Syn[Syndrome1][3]; document.getElementById("SttSyn1Social").innerHTML = SttSyn1Social;
	}
	if(Syndrome2){
		var SttSyn2Body   = Syn[Syndrome2][0]; document.getElementById("SttSyn2Body").innerHTML   = SttSyn2Body;
		var SttSyn2Sense  = Syn[Syndrome2][1]; document.getElementById("SttSyn2Sense").innerHTML  = SttSyn2Sense;
		var SttSyn2Spirit = Syn[Syndrome2][2]; document.getElementById("SttSyn2Spirit").innerHTML = SttSyn2Spirit;
		var SttSyn2Social = Syn[Syndrome2][3]; document.getElementById("SttSyn2Social").innerHTML = SttSyn2Social;
	} else {
		var SttSyn2Body   = 0; document.getElementById("SttSyn2Body").innerHTML   = '';
		var SttSyn2Sense  = 0; document.getElementById("SttSyn2Sense").innerHTML  = '';
		var SttSyn2Spirit = 0; document.getElementById("SttSyn2Spirit").innerHTML = '';
		var SttSyn2Social = 0; document.getElementById("SttSyn2Social").innerHTML = '';
		if(SttSyn1Body)   { document.getElementById("SttSyn1Body").innerHTML   = SttSyn1Body   + ' × 2'; } SttSyn1Body   = SttSyn1Body   * 2;
		if(SttSyn1Sense)  { document.getElementById("SttSyn1Sense").innerHTML  = SttSyn1Sense  + ' × 2'; } SttSyn1Sense  = SttSyn1Sense  * 2;
		if(SttSyn1Spirit) { document.getElementById("SttSyn1Spirit").innerHTML = SttSyn1Spirit + ' × 2'; } SttSyn1Spirit = SttSyn1Spirit * 2
		if(SttSyn1Social) { document.getElementById("SttSyn1Social").innerHTML = SttSyn1Social + ' × 2'; } SttSyn1Social = SttSyn1Social * 2;
	}
	
	var SttWorksBody   = 0;
	var SttWorksSense  = 0;
	var SttWorksSpirit = 0;
	var SttWorksSocial = 0;
	var worksSttCheck;
	var worksSttList = document.getElementsByName("stt_works");
	var str = "選択されていません";
	for(var i=0; i<worksSttList.length; i++){
		if (worksSttList[i].checked) {
			worksSttCheck = worksSttList[i].value;
			break;
		}
	}
	     if(worksSttCheck == 'body')  { SttWorksBody   = 1 }
	else if(worksSttCheck == 'sense') { SttWorksSense  = 1 }
	else if(worksSttCheck == 'spirit'){ SttWorksSpirit = 1 }
	else if(worksSttCheck == 'social'){ SttWorksSocial = 1 }
	
	var SttGrowBody   = d_c.stt_grow_body.value;
	var SttGrowSense  = d_c.stt_grow_sense.value;
	var SttGrowSpirit = d_c.stt_grow_spirit.value;
	var SttGrowSocial = d_c.stt_grow_social.value;
	var SttAddBody   = d_c.stt_add_body.value;
	var SttAddSense  = d_c.stt_add_sense.value;
	var SttAddSpirit = d_c.stt_add_spirit.value;
	var SttAddSocial = d_c.stt_add_social.value;
	if( isNaN(parseInt(SttGrowBody)) )   { SttGrowBody   = 0; } else { SttGrowBody   = eval(SttGrowBody)  ; }
	if( isNaN(parseInt(SttGrowSense)) )  { SttGrowSense  = 0; } else { SttGrowSense  = eval(SttGrowSense) ; }
	if( isNaN(parseInt(SttGrowSpirit)) ) { SttGrowSpirit = 0; } else { SttGrowSpirit = eval(SttGrowSpirit); }
	if( isNaN(parseInt(SttGrowSocial)) ) { SttGrowSocial = 0; } else { SttGrowSocial = eval(SttGrowSocial); }
	if( isNaN(parseInt(SttAddBody)) )   { SttAddBody   = 0; } else { SttAddBody   = eval(SttAddBody)  ; }
	if( isNaN(parseInt(SttAddSense)) )  { SttAddSense  = 0; } else { SttAddSense  = eval(SttAddSense) ; }
	if( isNaN(parseInt(SttAddSpirit)) ) { SttAddSpirit = 0; } else { SttAddSpirit = eval(SttAddSpirit); }
	if( isNaN(parseInt(SttAddSocial)) ) { SttAddSocial = 0; } else { SttAddSocial = eval(SttAddSocial); }
	
	var SttBody   = SttSyn1Body   + SttSyn2Body   + SttWorksBody   + SttGrowBody   + SttAddBody  ;
	var SttSense  = SttSyn1Sense  + SttSyn2Sense  + SttWorksSense  + SttGrowSense  + SttAddSense ;
	var SttSpirit = SttSyn1Spirit + SttSyn2Spirit + SttWorksSpirit + SttGrowSpirit + SttAddSpirit;
	var SttSocial = SttSyn1Social + SttSyn2Social + SttWorksSocial + SttGrowSocial + SttAddSpirit;
	
	var SttBaseBody   = SttSyn1Body   + SttSyn2Body   + SttWorksBody  ;
	var SttBaseSense  = SttSyn1Sense  + SttSyn2Sense  + SttWorksSense ;
	var SttBaseSpirit = SttSyn1Spirit + SttSyn2Spirit + SttWorksSpirit;
	var SttBaseSocial = SttSyn1Social + SttSyn2Social + SttWorksSocial;
	var SttTotalExp = 0;
	for(var s = SttBaseBody  +1; s <= SttBaseBody   + SttGrowBody  ; s++){ SttTotalExp += (s > 21) ? 30 : (s > 11) ? 20 : 10; }
	for(var s = SttBaseSense +1; s <= SttBaseSense  + SttGrowSense ; s++){ SttTotalExp += (s > 21) ? 30 : (s > 11) ? 20 : 10; }
	for(var s = SttBaseSpirit+1; s <= SttBaseSpirit + SttGrowSpirit; s++){ SttTotalExp += (s > 21) ? 30 : (s > 11) ? 20 : 10; }
	for(var s = SttBaseSocial+1; s <= SttBaseSocial + SttGrowSocial; s++){ SttTotalExp += (s > 21) ? 30 : (s > 11) ? 20 : 10; }
	document.getElementById("SttTotalExp").innerHTML = SttTotalExp;
	
	document.getElementById("SttBody").innerHTML   = SttBody;
	document.getElementById("SttSense").innerHTML  = SttSense;
	document.getElementById("SttSpirit").innerHTML = SttSpirit;
	document.getElementById("SttSocial").innerHTML = SttSocial;
	document.getElementById("SkillBody").innerHTML   = SttBody;
	document.getElementById("SkillSense").innerHTML  = SttSense;
	document.getElementById("SkillSpirit").innerHTML = SttSpirit;
	document.getElementById("SkillSocial").innerHTML = SttSocial;
	
	var SubHpAdd      = d_c.sub_hp_add.value;
	var SubProvideAdd = d_c.sub_provide_add.value;
	var SubSpeedAdd   = d_c.sub_speed_add.value;
	var SubMoveAdd    = d_c.sub_move_add.value;
	if( isNaN(parseInt(SubHpAdd)     ) ){ SubHpAdd     = 0; } else { SubHpAdd     = eval(SubHpAdd)     ; }
	if( isNaN(parseInt(SubProvideAdd)) ){ SubProvideAdd= 0; } else { SubProvideAdd= eval(SubProvideAdd); }
	if( isNaN(parseInt(SubSpeedAdd)  ) ){ SubSpeedAdd  = 0; } else { SubSpeedAdd  = eval(SubSpeedAdd)  ; }
	if( isNaN(parseInt(SubMoveAdd)   ) ){ SubMoveAdd   = 0; } else { SubMoveAdd   = eval(SubMoveAdd)   ; }
	
	var SkillFightLv = d_c.skill_fight_lv.value;
	var SkillShootLv = d_c.skill_shoot_lv.value;
	var SkillRCLv    = d_c.skill_RC_lv.value;
	var SkillNegoLv  = d_c.skill_nego_lv.value;
	var SkillDodgeLv = d_c.skill_dodge_lv.value;
	var SkillPerceLv = d_c.skill_perce_lv.value;
	var SkillWillLv  = d_c.skill_will_lv.value;
	var SkillRaiseLv = d_c.skill_raise_lv.value
	if( isNaN(parseInt(SkillFightLv)) ){ SkillFightLv = 0; } else { SkillFightLv = eval(SkillFightLv); }
	if( isNaN(parseInt(SkillShootLv)) ){ SkillShootLv = 0; } else { SkillShootLv = eval(SkillShootLv); }
	if( isNaN(parseInt(SkillRCLv)   ) ){ SkillRCLv    = 0; } else { SkillRCLv    = eval(SkillRCLv)   ; }
	if( isNaN(parseInt(SkillNegoLv) ) ){ SkillNegoLv  = 0; } else { SkillNegoLv  = eval(SkillNegoLv) ; }
	if( isNaN(parseInt(SkillDodgeLv)) ){ SkillDodgeLv = 0; } else { SkillDodgeLv = eval(SkillDodgeLv); }
	if( isNaN(parseInt(SkillPerceLv)) ){ SkillPerceLv = 0; } else { SkillPerceLv = eval(SkillPerceLv); }
	if( isNaN(parseInt(SkillWillLv) ) ){ SkillWillLv  = 0; } else { SkillWillLv  = eval(SkillWillLv) ; }
	if( isNaN(parseInt(SkillRaiseLv)) ){ SkillRaiseLv = 0; } else { SkillRaiseLv = eval(SkillRaiseLv); }
	
	document.getElementById("SubHpTotal").innerHTML      = SttBody   * 2 + SttSpirit + 20 + SubHpAdd;
	document.getElementById("SubProvideTotal").innerHTML = SttSocial * 2 + SkillRaiseLv * 2 + SubProvideAdd;
	document.getElementById("SubSpeedTotal").innerHTML   = SttSense * 2 + SttSpirit + SubSpeedAdd;
	document.getElementById("SubMoveTotal").innerHTML    = SttSense * 2 + SttSpirit + SubSpeedAdd + 5 + SubMoveAdd;
	document.getElementById("SubFullMoveTotal").innerHTML= ( SttSense * 2 + SttSpirit + SubSpeedAdd + 5 + SubMoveAdd ) * 2;
	
	var LpAwakenInvade = d_c.lifepath_awaken_invade.value;
	var LpUrgeInvade   = d_c.lifepath_urge_invade.value;
	var LpOtherInvade  = d_c.lifepath_other_invade.value;
	if( isNaN(parseInt(LpAwakenInvade)) ){ LpAwakenInvade = 0; } else { LpAwakenInvade = eval(LpAwakenInvade); }
	if( isNaN(parseInt(LpUrgeInvade)) )  { LpUrgeInvade   = 0; } else { LpUrgeInvade   = eval(LpUrgeInvade)  ; }
	if( isNaN(parseInt(LpOtherInvade)) ) { LpOtherInvade  = 0; } else { LpOtherInvade  = eval(LpOtherInvade) ; }
	
	document.getElementById("SttInvade").innerHTML = LpAwakenInvade + LpUrgeInvade + LpOtherInvade;
	
	var ItemTotalPoint = 0;
	var ItemTotalExp = 0;
	for(var i=1; i<=CountWeapon; i++){
		var Point = d_c.elements["weapon"+i+"_point"].value;
		var Exp   = d_c.elements["weapon"+i+"_exp"].value;
		if( isNaN(parseInt(Point)) ){ Point = 0; } else { Point = eval(Point); }
		if( isNaN(parseInt(Exp)) )  { Exp   = 0; } else { Exp   = eval(Exp)  ; }
		ItemTotalPoint += Point;
		ItemTotalExp   += Exp;
	}
	for(var i=1; i<=CountArmour; i++){
		var Point = d_c.elements["armour"+i+"_point"].value;
		var Exp   = d_c.elements["armour"+i+"_exp"].value;
		if( isNaN(parseInt(Point)) ){ Point = 0; } else { Point = eval(Point); }
		if( isNaN(parseInt(Exp)) )  { Exp   = 0; } else { Exp   = eval(Exp)  ; }
		ItemTotalPoint += Point;
		ItemTotalExp   += Exp;
	}
	for(var i=1; i<=CountItem; i++){
		var Point = d_c.elements["item"+i+"_point"].value;
		var Exp   = d_c.elements["item"+i+"_exp"].value;
		if( isNaN(parseInt(Point)) ){ Point = 0; } else { Point = eval(Point); }
		if( isNaN(parseInt(Exp)) )  { Exp   = 0; } else { Exp   = eval(Exp)  ; }
		ItemTotalPoint += Point;
		ItemTotalExp   += Exp;
	}
	document.getElementById("ItemTotalPoint").innerHTML = ItemTotalPoint;
	document.getElementById("ItemTotalExp").innerHTML   = ItemTotalExp;
	
	if( isNaN(parseInt(LpAwakenInvade)) ){ LpAwakenInvade = 0; } else { LpAwakenInvade = eval(LpAwakenInvade); }
	
	var SkillTotalExp = -9;
	for(var l=1; l<=SkillFightLv; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillShootLv; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillRCLv   ; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillNegoLv ; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillDodgeLv; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillPerceLv; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillWillLv ; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var l=1; l<=SkillRaiseLv; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 2; }
	for(var i=1; i<=CountSkill; i++){
		var Lv1 = d_c.elements["skill_drive"+i+"_lv"].value;
		var Lv2 = d_c.elements["skill_art"+i+"_lv"].value;
		var Lv3 = d_c.elements["skill_know"+i+"_lv"].value;
		var Lv4 = d_c.elements["skill_info"+i+"_lv"].value;
		if( isNaN(parseInt(Lv1)) ){ Lv1 = 0; } else { Lv1 = eval(Lv1); }
		if( isNaN(parseInt(Lv2)) ){ Lv2 = 0; } else { Lv2 = eval(Lv2); }
		if( isNaN(parseInt(Lv3)) ){ Lv3 = 0; } else { Lv3 = eval(Lv3); }
		if( isNaN(parseInt(Lv4)) ){ Lv4 = 0; } else { Lv4 = eval(Lv4); }
		for(var l=1; l<=Lv1; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 1; }
		for(var l=1; l<=Lv2; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 1; }
		for(var l=1; l<=Lv3; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 1; }
		for(var l=1; l<=Lv4; l++){ SkillTotalExp += (l > 21) ? 10 : (l > 11) ? 5 : (l > 6) ? 3 : 1; }
	}
	document.getElementById("SkillTotalExp").innerHTML = SkillTotalExp;
	
	var EffectTotalExp = 0;
	for(var i=1; i<=CountEffect; i++){
		var Lv = d_c.elements["effect"+i+"_lv"].value;
		var Limit = d_c.elements["effect"+i+"_limit"].value;
		if( isNaN(parseInt(Lv)) ){ Lv = 0; } else { Lv = eval(Lv); }
		if(Lv > 0) {
			EffectTotalExp += Lv * 5 + 10;
			if(Limit === "Dロイス" || Limit === "Ｄロイス"){ EffectTotalExp -= 15; }
		}
	}
	document.getElementById("EffectTotalExp").innerHTML = EffectTotalExp;
	
	var EffectEzTotalExp = 0;
	for(var i=1; i<=CountEffectEz; i++){
		var Lv = d_c.elements["effect_ez"+i+"_lv"].value;
		if( isNaN(parseInt(Lv)) ){ Lv = 0; } else { Lv = eval(Lv); }
		if(Lv > 0) { EffectEzTotalExp += 2; }
	}
	document.getElementById("EffectEzTotalExp").innerHTML = EffectEzTotalExp;
	
	var ExpUse = SttTotalExp + EffectTotalExp + EffectEzTotalExp + SkillTotalExp + ItemTotalExp;
	document.getElementById("ExpUse").innerHTML = ExpUse;
}

function exp_calc(){
	if(d_c.exp_auto.checked) {
		var hst_cnt = d_c.count_history.value *1;
		var exp_ttl = d_c.make_exp.value *1;
		for (var i = 1; i <= hst_cnt; i++){
			var exp_plus = parseInt(eval(d_c["hist_exp" + i].value));
			if(isNaN(exp_plus)){ exp_plus = 0; }
			exp_ttl += exp_plus;
		}
		d_c.exp.value = exp_ttl;
	}
	calc();
}

function emoP(Num){ document.getElementById("LoisN"+Num).checked = false; }
function emoN(Num){ document.getElementById("LoisP"+Num).checked = false; }

function AddSkill(){
	CountSkill++;
	var table = document.getElementById("SkillTable");
	var row = table.insertRow(-1);
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	var cell3 = row.insertCell(2);
	var cell4 = row.insertCell(3);
	var cell5 = row.insertCell(4);
	var cell6 = row.insertCell(5);
	var cell7 = row.insertCell(6);
	var cell8 = row.insertCell(7);
	var cell9 = row.insertCell(8);
	var cell10= row.insertCell(9);
	var cell11= row.insertCell(10);
	var cell12= row.insertCell(11);
	cell1.setAttribute("class","L bbR");
	cell2.setAttribute("class","inp bbL");
	cell3.setAttribute("class","inp C");
	cell4.setAttribute("class","L bbR");
	cell5.setAttribute("class","inp bbL");
	cell6.setAttribute("class","inp C");
	cell7.setAttribute("class","L bbR");
	cell8.setAttribute("class","inp bbL");
	cell9.setAttribute("class","inp C");
	cell10.setAttribute("class","L bbR");
	cell11.setAttribute("class","inp bbL");
	cell12.setAttribute("class","inp C");

	cell1.innerHTML = '運転：';
	cell2.innerHTML = '<input type="text" name="skill_drive' + CountSkill + '_name">';
	cell3.innerHTML = '<input type="text" name="skill_drive' + CountSkill + '_lv" style="width:30px;" onChange="calc()">Lv';
	cell4.innerHTML = '芸術：';
	cell5.innerHTML = '<input type="text" name="skill_art' + CountSkill + '_name">';
	cell6.innerHTML = '<input type="text" name="skill_art' + CountSkill + '_lv" style="width:30px;" onChange="calc()">Lv';
	cell7.innerHTML = '知識：';
	cell8.innerHTML = '<input type="text" name="skill_know' + CountSkill + '_name">';
	cell9.innerHTML = '<input type="text" name="skill_know' + CountSkill + '_lv" style="width:30px;" onChange="calc()">Lv';
	cell10.innerHTML= '情報：';
	cell11.innerHTML= '<input type="text" name="skill_info' + CountSkill + '_name">';
	cell12.innerHTML= '<input type="text" name="skill_info' + CountSkill + '_lv" style="width:30px;" onChange="calc()">Lv';
	
	document.chr.count_skill.value = CountSkill;
}
function DelSkill(){
	if(CountSkill > 1){
		var table = document.getElementById("SkillTable");
		table.deleteRow(-1);
		CountSkill--;
	document.chr.count_skill.value = CountSkill;
	}
}

function AddEffect(Ez){
	if(Ez){ CountEffectEz++; }
	else  { CountEffect++; }

	var table; var RowCount;
	if(Ez){ table = document.getElementById("EffectEzTable"); RowCount = document.getElementById("EffectEzTable").rows.length; }
	else  { table = document.getElementById("EffectTable");   RowCount = document.getElementById("EffectTable").rows.length; }

	if( (Ez && CountEffectEz % 10 == 0)
	 || (! Ez && CountEffect % 10 == 0) ){
		var rowH = table.insertRow(RowCount-1);
		var thObj1 = document.createElement("th");
		var thObj2 = document.createElement("th");
		var thObj3 = document.createElement("th");
		var thObj4 = document.createElement("th");
		var thObj5 = document.createElement("th");
		var thObj6 = document.createElement("th");
		var thObj7 = document.createElement("th");
		var thObj8 = document.createElement("th");
		var thObj9 = document.createElement("th");
		var thObj10= document.createElement("th");
		thObj1.innerHTML = "No.";
		thObj2.innerHTML = "名称";
		thObj3.innerHTML = "Lv";
		thObj4.innerHTML = "タイミング";
		thObj5.innerHTML = "技能";
		thObj6.innerHTML = "難易度";
		thObj7.innerHTML = "対象";
		thObj8.innerHTML = "射程";
		thObj9.innerHTML = "侵蝕値";
		thObj10.innerHTML= "制限";
		rowH.appendChild(thObj1);
		rowH.appendChild(thObj2);
		rowH.appendChild(thObj3);
		rowH.appendChild(thObj4);
		rowH.appendChild(thObj5);
		rowH.appendChild(thObj6);
		rowH.appendChild(thObj7);
		rowH.appendChild(thObj8);
		rowH.appendChild(thObj9);
		rowH.appendChild(thObj10);
	}
	var row3 = table.insertRow(RowCount-1);
	var row2 = table.insertRow(RowCount-1);
	var row1 = table.insertRow(RowCount-1);
	var cell1 = row1.insertCell(0);
	var cell2 = row1.insertCell(1);
	var cell3 = row1.insertCell(2);
	var cell4 = row1.insertCell(3);
	var cell5 = row1.insertCell(4);
	var cell6 = row1.insertCell(5);
	var cell7 = row1.insertCell(6);
	var cell8 = row1.insertCell(7);
	var cell9 = row1.insertCell(8);
	var cell10= row1.insertCell(9);
	var cell11= row2.insertCell(0);
	var cell12= row3.insertCell(0);

	if( (Ez && CountEffectEz % 2 == 0)
	 || (! Ez && CountEffect % 2 == 0) ){
		row1.setAttribute("class","rv");
		row2.setAttribute("class","rv");
		row3.setAttribute("class","rv");
	}

	cell1.setAttribute("class","C B");
	cell1.setAttribute("rowspan","2");
	cell2.setAttribute("class","inp");
	cell3.setAttribute("class","inp");
	cell4.setAttribute("class","inp");
	cell5.setAttribute("class","inp");
	cell6.setAttribute("class","inp");
	cell7.setAttribute("class","inp");
	cell8.setAttribute("class","inp");
	cell9.setAttribute("class","inp");
	cell10.setAttribute("class","inp");
	cell11.setAttribute("class","inp");
	cell11.setAttribute("colspan","9");
	cell12.setAttribute("class","horizonB");
	cell12.setAttribute("colspan","9");

	if(Ez){ cell1.innerHTML = CountEffectEz; }
	else  { cell1.innerHTML = CountEffect; }
	cell2.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_name">';
	cell3.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_lv">';
	cell4.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_timing">';
	cell5.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_skill">';
	cell6.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_diffi">';
	cell7.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_target">';
	cell8.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_range">';
	cell9.innerHTML = '<input type="text" name="effect'+ Ez + CountEffect + '_point">';
	cell10.innerHTML= '<input type="text" name="effect'+ Ez + CountEffect + '_limit">';
	cell11.innerHTML= '<input type="text" name="effect'+ Ez + CountEffect + '_note">';

	if(Ez){ document.chr.count_effect_ez.value = CountEffectEz; }
	else  { document.chr.count_effect.value = CountEffect; }
}
function DelEffect(){
	if(CountEffect > 1){
		var table = document.getElementById("EffectTable");
		var RowCount = document.getElementById("EffectTable").rows.length;
		table.deleteRow(RowCount-2);
		table.deleteRow(RowCount-3);
		table.deleteRow(RowCount-4);
		if(CountEffect % 10 == 0) { table.deleteRow(RowCount-5); }
		CountEffect--;
		document.chr.count_effect.value = CountEffect;
	}
}
function DelEffectEz(){
	if(CountEffectEz > 1){
		var table = document.getElementById("EffectEzTable");
		var RowCount = document.getElementById("EffectEzTable").rows.length;
		table.deleteRow(RowCount-2);
		table.deleteRow(RowCount-3);
		table.deleteRow(RowCount-4);
		if(CountEffectEz % 10 == 0) { table.deleteRow(RowCount-5); }
		CountEffectEz--;
		document.chr.count_effect_ez.value = CountEffectEz;
	}
}

function AddHistory(){
	CountHistory++;
	var InsHistory = (CountHistory *2) -1 ;
	var table = document.getElementById("table_history");
	var row2 = table.insertRow(InsHistory);
	var row1 = table.insertRow(InsHistory);
	var cell1 = row1.insertCell(0);
	var cell2 = row1.insertCell(1);
	var cell3 = row1.insertCell(2);
	var cell4 = row1.insertCell(3);
	var cell5 = row1.insertCell(4);
	var cell6 = row2.insertCell(0);
	var cell7 = row2.insertCell(1);
	cell1.setAttribute("class","inp");
	cell2.setAttribute("class","inp");
	cell3.setAttribute("class","inp");
	cell4.setAttribute("class","inp");
	cell5.setAttribute("class","inp");
	cell6.setAttribute("colspan","2");
	cell6.setAttribute("class","non R");
	cell7.setAttribute("colspan","5");
	cell7.setAttribute("class","inp");
	cell1.innerHTML = '<input type="text" name="hist_date' + CountHistory + '">';
	cell2.innerHTML = '<input type="text" name="hist_name' + CountHistory + '">';
	cell3.innerHTML = '<input type="text" name="hist_exp' + CountHistory + '" onchange="exp_calc()">';
	cell4.innerHTML = '<input type="text" name="hist_gm' + CountHistory + '">';
	cell5.innerHTML = '<input type="text" name="hist_member' + CountHistory + '">';
	cell6.innerHTML = '備考';
	cell7.innerHTML= '<input type="text" name="hist_note' + CountHistory + '">';
	d_c.count_history.value = CountHistory;
	calc();
}
function DelHistory(){
	if(CountHistory > 1){
		var InsHistory = (CountHistory *2) -1 ;
		var table = document.getElementById("table_history");
		table.deleteRow(InsHistory);
		table.deleteRow(InsHistory);
		CountHistory--;
		d_c.count_history.value = CountHistory;
	}
	calc();
}

function jump(){
	var fb =  '';
	var ft =  '';
	var fl =  '';
	var cb1 = '';
	var cb2 = '';
	var ct =  '';
	var cl =  '';
	var rad = '';
	if(d_c.mycss.checked){
		fb  = d_c.css_frame.value; fb  = encodeURIComponent(fb);
		ft  = d_c.css_font1.value; ft  = encodeURIComponent(ft);
		fl  = d_c.css_pl.value;    fl  = encodeURIComponent(fl);
		cb1 = d_c.css_cell1.value; cb1 = encodeURIComponent(cb1);
		cb2 = d_c.css_cell2.value; cb2 = encodeURIComponent(cb2);
		ct  = d_c.css_font2.value; ct  = encodeURIComponent(ct);
		cl  = d_c.css_link.value;  cl  = encodeURIComponent(cl);
	}
	if(d_c.css_radius.checked){ rad = 1; }
	var css = d_c.CSS.options[d_c.CSS.selectedIndex].value;
	
	var target = "css";
	var url = "color.cgi?mode=preview&id="+css+"&rad="+rad+"&fb="+fb+"&ft="+ft+"&fl="+fl+"&cb1="+cb1+"&cb2="+cb2+"&ct="+ct+"&cl="+cl;
	if(url != "" ){
		if(target == 'top'){
			top.location.href = url;
		}
		else if(target == 'blank'){
			window.open(url, 'window_name');
		}
		else if(target != ""){
			eval('parent.' + target + '.location.href = url');
		}
		else{
			location.href = url;
		}
	}
}

function tbcolorcheck(i,j,k){
	var strs = i.value;
	var red = "" + strs[1] + strs[2];
	var gre = "" + strs[3] + strs[4];
	var blu = "" + strs[5] + strs[6];
	red = parseInt(red,16);
	gre = parseInt(gre,16);
	blu = parseInt(blu,16);
	var array = [red, gre, blu];
	array.sort(function(a,b){return b - a;});
	if(red > 208 || gre > 208 || blu > 208){ i.style.background = "#dd9999"; }
	else if(k == 1 && (red < 32 || gre < 32 || blu < 32)){ i.style.background = "#9999dd"; }
	else if(j == 1 && array[0] - array[2] > 128){ i.style.background = "#dddd99"; }
	else if(j == 2 && array[0] - array[2] > 80){ i.style.background = "#dddd99"; }
	else { i.style.background = ""; }
}

function visible(id){
	var ele = self.document.getElementById(id);
	if (ele.style.display == 'none') { ele.style.display = ''; }
	else { ele.style.display = 'none'; }
}

window.onload = calc();

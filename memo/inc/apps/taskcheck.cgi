sub _NUM {
	my($n1,$n2) = @_;
	if($n1 > $n2){
		##"<td><em class=\"up\"><strong>25</strong><span>&#9654;</span>3.5%</em></td>"
		my $dis = $n1 - $n2;
		if($dis < 0){
			$dis *= -1;
		}
		$dis = sprintf("%.1f",$dis);
		return "<td><em class=\"up\"><strong>${n1}</strong>\[ ${dis} \]</em></td>";
	}
	elsif($n1 < $n2){
		my $dis = $n1 - $n2;
		if($dis < 0){
			$dis *= -1;
		}
		$dis = sprintf("%.1f",$dis);
		return "<td><em class=\"down\"><strong>${n1}</strong>\[ ${dis} \]</em></td>";
	}
	else {
		return "<td><em class=\"up\"><strong>${n1}</strong></em></td>";
	}
}
sub _NUM2 {
	my($n1,$n2) = @_;
	if($n1 > $n2){
		my $dis = $n1 - $n2;
		if($dis < 0){
			$dis *= -1;
		}
		$dis = sprintf("%.1f",$dis);
		return "<td><em class=\"down\"><strong>-${n1}</strong>\[ -${dis} \]</em></td>";
	}
	elsif($n1 < $n2){
		my $dis = $n1 - $n2;
		if($dis < 0){
			$dis *= -1;
		}
		$dis = sprintf("%.1f",$dis);
		return "<td><em class=\"up\"><strong>-${n1}</strong>\[ -${dis} \]</em></td>";
	}
	else {
		return "<td><em class=\"up\"><strong>${n1}</strong></em></td>";
	}
}

sub _AVG {
	my($n1,$n2) = @_;
	if($n1 > 0 && $n2 > 0){
		return sprintf("%.2f",$n1 / $n2);
	}
	else {
		return 0;
	}
}
my $count = 14;
if($_GET{'width'} < 1280){
	$count = 7;
}
if($_GET{'key'} eq $config{'keycode'}){
	## 過去2週間の推移　TODO消化・日課消化
	## 日課の累積値・日課の継続日数
	## 日課の一覧
	if($_GET{'id'}){
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
		my $token = sprintf("%04d%02d%02d",$year+1900,$mon+1,$mday);
		&_COUNTUP("$config{'dir.task'}$_USER{'id'}_count.cgi");
		&_COUNTUP("$config{'dir.task'}$_USER{'id'}_$_GET{'id'}.cgi");
		&_COUNTUP("$config{'dir.task'}$_USER{'id'}_${token}_$_GET{'id'}.cgi");
		
		my $time = time;
		$time -= (60 * 60 * 24); ## 前日のデータをチェック
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
		$token = sprintf("%04d%02d%02d",$year+1900,$mon+1,$mday);
		if(-f "$config{'dir.task'}$_USER{'id'}_${token}_$_GET{'id'}.cgi"){
			## 前日のデータがある場合、カレントをすすめる
			&_COUNTUP("$config{'dir.task'}$_USER{'id'}_current_$_GET{'id'}.cgi");
			my $qty = -s "$config{'dir.task'}$_USER{'id'}_current_$_GET{'id'}.cgi";
			my $max = -s "$config{'dir.task'}$_USER{'id'}_max_$_GET{'id'}.cgi";
			if($qty > $max){
				&_SAVE("$config{'dir.task'}$_USER{'id'}_max_$_GET{'id'}.cgi",&_LOAD("$config{'dir.task'}$_USER{'id'}_current_$_GET{'id'}.cgi"));
			}
		}
		else {
			## 前日のデータが無い場合、カレントをリセット
			&_SAVE("$config{'dir.task'}$_USER{'id'}_current_$_GET{'id'}.cgi",'0');
		}
	}
	
	my @html = ("<table class=\"daily\">");
	my @json = ();
	
	my $time = time;
	my ($t0sec,$t0min,$t0hour,$t0mday,$t0mon,$t0year,$t0wday,$t0yday,$t0isdst) = localtime($time);
	my $t0s = sprintf("%04d%02d%02d",$t0year+1900,$t0mon+1,$t0mday);
	
	## 一週間前を算出
	my $time1 = $time - (60*60*24*($count-1));
	
	## 二週間前を算出
	my $time2 = $time - (60*60*24*($count+7-1));
	
	my @tr = ();
	$tr[0] = "<th>&nbsp;</th>";
	$tr[1] = "<th>$_LANG{'app_analyze_date'}</th>";
	$tr[2] = "<th class=\"text3\">$_LANG{'app_analyze_total'}</th>";
	$tr[3] = "<th class=\"text1\">$_LANG{'app_analyze_task'}</th>";
	$tr[4] = "<th class=\"text2\">$_LANG{'app_analyze_mission'}</th>";
	
	my @mission = &_DB("$config{'dir.task'}$_USER{'id'}.cgi");
	for(my $i=0;$i<@mission;$i++){
		my @m = split(/\t/,$mission[$i]);
		if($m[2]){
			my $k0 = -s "$config{'dir.task'}$_USER{'id'}_${t0s}_${m[0]}.cgi" || 0;
			if($k0 > 0){
				$m[1] = "<strong style=\"color: #F00;\">${m[1]}</strong>";
			}
			$tr[5+$i] = "<th><span style=\"color: #F00;\" class=\"click\" onclick=\"web.App.analyze.action.click('${m[0]}')\">${m[1]}</span></th>";
		}
		else {
			my $k0 = -s "$config{'dir.task'}$_USER{'id'}_${t0s}_${m[0]}.cgi" || 0;
			if($k0 > 0){
				$m[1] = "<strong>${m[1]}</strong>";
			}
			$tr[5+$i] = "<th><span class=\"click\" onclick=\"web.App.analyze.action.click('${m[0]}')\">${m[1]}</span></th>";
		}
	}
	
	my @wt1 = ();
	my @wt2 = ();
	
	my $to1 = 0; ## 今週の合計
	my $to2 = 0; ## 先週の合計
	
	my $wt1 = 0; ## 今週のミッション達成合計
	my $wt2 = 0; ## 先週のミッション達成合計
	
	my $kt1 = 0; ## 今週のタスク処理合計
	my $kt2 = 0; ## 先週のタスク処理合計
	
	my @w = split(/\,/,$_LANG{'calendar_week'});
	for(my $i=0;$i<$count;$i++){
		my $t1 = $time1 + ((60*60*24)*$i);
		my ($t1sec,$t1min,$t1hour,$t1mday,$t1mon,$t1year,$t1wday,$t1yday,$t1isdst) = localtime($t1);
		$t1s = sprintf("%04d%02d%02d",$t1year+1900,$t1mon+1,$t1mday);
		my $t2 = $time2 + ((60*60*24)*$i);
		my ($t2sec,$t2min,$t2hour,$t2mday,$t2mon,$t2year,$t2wday,$t2yday,$t2isdst) = localtime($t2);
		$t2s = sprintf("%04d%02d%02d",$t2year+1900,$t2mon+1,$t2mday);
		
		## 日付表示
		$tr[1] .= "<td class=\"w${t1wday} label\">${t1mday}<span>${w[$t1wday]}</span></td>";
		
		my $k1 = -s "$config{'dir.task'}$_USER{'id'}_${t1s}_task.cgi" || 0;
		my $k2 = -s "$config{'dir.task'}$_USER{'id'}_${t2s}_task.cgi" || 0;
		
		$kt1 += $k1;
		$kt2 += $k2;
		
		## Task
		$tr[3] .= &_NUM($k1,$k2);
		
		my $m1 = 0;
		my $m2 = 0;
		for(my $ii=0;$ii<@mission;$ii++){
			my @m = split(/\t/,$mission[$ii]);
			my $c1 = -s "$config{'dir.task'}$_USER{'id'}_${t1s}_${m[0]}.cgi" || 0;
			my $c2 = -s "$config{'dir.task'}$_USER{'id'}_${t2s}_${m[0]}.cgi" || 0;
			if($m[2]){
				$m1 -= $c1;
				$m2 -= $c2;
				$tr[5+$ii] .= &_NUM2($c1,$c2);
				$wt1[$ii] -= $c1;
				$wt2[$ii] -= $c2;
			}
			else {
				$m1 += $c1;
				$m2 += $c2;
				$tr[5+$ii] .= &_NUM($c1,$c2);
				$wt1[$ii] += $c1;
				$wt2[$ii] += $c2;
			}
		}
		$wt1 += $m1;
		$wt2 += $m2;
		$to1 += $m1+$k1;
		$to2 += $m2+$k2;
		
		## Mission
		$tr[4] .= &_NUM($m1,$m2);
		
		## Total
		$tr[2] .= &_NUM($k1+$m1,$k2+$m2);
		
		## グラフを表示
		my $bar1 = ($k1) * 5;
		my $bar2 = ($m1) * 5;
		my $bar3 = ($k1+$m1) * 5;
		my @j = ("\"${t1mday}\"",($k1+$m1),($k2+$m2));
		push @json,"\[" . join(",",@j) . "\]";
		#$tr[0] .= "<td valign=\"bottom\"><div class=\"barwrap\"><div class=\"bar1\" style=\"height: ${bar1}px\"></div><div class=\"bar2\" style=\"height: ${bar2}px\"></div><div class=\"bar3\" style=\"height: ${bar3}px\"></div></div></td>";
		
	}
	
	$tr[0] .= "<td colspan=\"${count}\"><div id=\"graph\"></div></td><td colspan=\"2\" valign=\"bottom\">$_LANG{'app_analyze_weekly'}<br><br></td><td colspan=\"2\" valign=\"bottom\">$_LANG{'app_analyze_sum'}<br><br></td><td colspan=\"2\" valign=\"bottom\">$_LANG{'continuation'}<br><br></td>";
	$tr[1] .= "<td>$_LANG{'app_analyze_total'}</td><td>$_LANG{'app_analyze_avg'}</td><td>$_LANG{'app_analyze_total'}</td><td>$_LANG{'app_analyze_avg'}</td><td>$_LANG{'currentcontinuation'}</td><td>$_LANG{'maxcontinuation'}</td>";
	
	## タスク
	$tr[3] .= &_NUM($kt1,$kt2);
	$tr[3] .= &_NUM(&_AVG($kt1,7),&_AVG($kt2,7));
	my $ttotal = -s "$config{'dir.task'}$_USER{'id'}_task.cgi" || 0;
	$tr[3] .= "<td>${ttotal}</td><td>-</td><td>-</td><td>-</td>";
	
	## ミッション
	$tr[4] .= &_NUM($wt1,$wt2);
	$tr[4] .= &_NUM(&_AVG($wt1,7),&_AVG($wt2,7));
	my $mtotal = -s "$config{'dir.task'}$_USER{'id'}_count.cgi" || 0;
	$tr[4] .= "<td>${mtotal}</td><td>-</td><td>-</td><td>-</td>";
	
	
	## 合計
	$tr[2] .= &_NUM($to1,$to2);
	$tr[2] .= &_NUM(&_AVG($to1,7),&_AVG($to2,7));
	my $atotal = $ttotal + $mtotal;
	$tr[2] .= "<td>${atotal}</td><td>-</td><td>-</td><td>-</td>";
	
	for(my $ii=0;$ii<@mission;$ii++){
		my @m = split(/\t/,$mission[$ii]);
		$tr[5+$ii] .= &_NUM($wt1[$ii],$wt2[$ii]);
		$tr[5+$ii] .= &_NUM(&_AVG($wt1[$ii],7),&_AVG($wt2[$ii],7));
		my $total = -s "$config{'dir.task'}$_USER{'id'}_${m[0]}.cgi" || 0;
		my $days = int(($time - $m[0]) / (60*60*24));
		$tr[5+$ii] .= "<td>${total}</td>";
		$avg = &_AVG($total,$days);
		$tr[5+$ii] .= "<td>${avg}</td>";
		
		## 継続 現在
		my $current = -s "$config{'dir.task'}$_USER{'id'}_current_${m[0]}.cgi" || 0;
		$tr[5+$ii] .= "<td>${current}</td>";
		
		## 継続 最大
		my $max = -s "$config{'dir.task'}$_USER{'id'}_max_${m[0]}.cgi" || 0;
		$tr[5+$ii] .= "<td>${max}</td>";
		
	}
	
	push @html,"<tr>" . join("</tr><tr>",@tr) . "</tr>";
	
	my $html = join("",@html);
	$html =~ s/\"/\\\"/ig;
	my $json = join("\,",@json);
	$_RESULT{'json'} = "web.App.analyze.action.callback(\"${html}\",\[${json}\]);";
}
else {
	$_RESULT{'json'} = "web.App.analyze.action.error();";
}
1;
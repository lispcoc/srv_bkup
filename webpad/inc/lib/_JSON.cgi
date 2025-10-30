sub _JSON_LOGS {
	## [0] id
	## [1] parent
	## [2] userid
	## [3] create date
	## [4] target date
	## [5] finish date
	## [6] todo
	## [7] worktime
	## [8] location
	## [9] form_text
	my($str,$parentName,$parentId) = @_;
	my @r = split(/\t/,$str);
	$r[7] += 0;
	my $complete = '0';
	if($r[5]){
		$complete = '1';
	}
	my $picture = 'false';
	if(-f "$config{'dir.picture'}${r[2]}.jpg"){
		$picture = "\'$config{'dir.picture'}${r[2]}.jpg\'";
	}
	return "\{id: '${r[0]}',user: '${r[2]}',date: '${r[4]}',text: '${r[9]}',cdate: '${r[3]}',parent: '${r[1]}',todo: '${r[6]}',worktime: ${r[7]},complete: ${complete},parentName: '${parentName}',parentId: '${r[1]}',picture: ${picture}\}";
}
1;
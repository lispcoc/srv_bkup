if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	&_LIB('JSON'); ##
	my $path = "$config{'dir.data'}webpad.cgi";
	my @db = &_DB($path);
	my @parentNode = @db;
	my @current = grep(/\troot\t/,@db);
	my @list = ();
	for(my $i=0;$i<@current;$i++){
		my @r = split(/\t/,$current[$i]);
		my $id = $r[0];
		my $name = (split(/<br>/,$r[6]))[0];
		my $qty = grep(/\t${id}\t/,@db);
		push @list,"\{id: '${id}',name: '${name}',qty: ${qty}\}";
	}
	my $list = join("\,",@list);
	
	my @path = ("\{id: 'root',name: 'root'\}");
	$path = join("\,",@path);
	
	## Logs
	my $lpath = "$config{'dir.data'}logs.cgi";
	my @db = &_DB($lpath);
	@db = sort { (split(/\t/,$a))[4] cmp (split(/\t/,$b))[4]} @db;
	my $index = @db;
	@db = grep(!/\t\[\D\]\t$/,@db);
	my @logs = ();
	for(my $i=@db-1;$i >= 0 && @logs < 20;$i--){
		push @logs,&_JSON_LOGS($db[$i]);
	}
	my $logs = join("\,",@logs);
	
	## Todo
	@db = grep(/\t1\t/,@db);
	my @todo = ();
	for(my $i=0;$i<@db;$i++){
		my @r = split(/\t/,$db[$i]);
		if($r[6] && $r[5] eq $null){
			$r[7] += 0;
			my $timer = 'false';
			my $time = 0;
			my $token = "$config{'dir.data'}timer/${r[0]}.cgi";
			if(-f $token){
				$time = time - (stat $token)[9];
				$timer = 'true';
			}
			my $parentName = '';
			if($r[1] ne 'root'){
				my @p = grep(/^${r[1]}\t/,@parentNode);
				@p = split(/\t/,$p[0]);
				@p = split(/<br>/,$p[6]);
				$parentName = $p[0];
			}
			unshift @todo,"\{id: '${r[0]}',user: '${r[2]}',date: '${r[4]}',text: '${r[9]}',worktime: ${r[7]},timer: ${timer},time: ${time},parentName: '${parentName}',parentId: '${r[1]}'\}";
		}
	}
	my $todo = join("\,",@todo);
	
	my $cycleToken = "$config{'dir.data'}cycle/$_USER{'id'}.cgi";
	my $cycleStat = 'false';
	my $cycleDate = 'null';
	if(-f $cycleToken){
		$cycleStat = 'true';
		$cycleDate = 'new Date(' . (stat $cycleToken)[9] * 1000 . ')';
	}
	
	$_VAL{'script'} = <<"	__HTML__";
		<script>
			var timeagoStrings = '_%%timeago%%_';
			web.App.Id = '$_USER{'id'}';
			web.App.Dir = '$config{'dir.data'}';
			web.App.lifecycle.Status = ${cycleStat};
			web.App.lifecycle.Date = ${cycleDate};
			web.Lang = {
				timeago: '_%%timeago%%_',
				calendarMonth: '_%%calendar_month%%_',
				calendarWeek: '_%%calendar_week%%_',
				calendarFormat: '_%%calendar_format%%_',
				statusSave: '_%%status_save%%_',
				statusMail: '_%%status_mail%%_',
				statusRemove: '_%%status_remove%%_',
				complete: '_%%complete%%_',
				cycleStart: '_%%cycle_start%%_',
				cycleEnd: '_%%cycle_end%%_'
			};
			web.App.logs.Index = ${index};
			web.App.data.action.rebuild(\[${list}\],\[${logs}\],\[${todo}\],\[${path}\],${index})
		</script>
	__HTML__
}
else {
	$_RESULT{'404'} = 1;
}
1;
if($_GET{'key'} eq $config{'keycode'} && $_GET{'q'} ne $null){
	&_LIB('JSON'); ##
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	
	$_GET{'q'} =~ s/　/ /ig;
	my @query = split(/ /ig,$_GET{'q'});
	
	my @db = &_DB($path);
	my @parentNode = @db;
	my $lpath = "$config{'dir.data'}logs.cgi";
	my @logs = &_DB($lpath);
	my $index = @logs;
	for(my $i=0;$i<@query;$i++){
		@db = grep(/${query[$i]}/ig,@db);
		@logs = grep(/${query[$i]}/ig,@logs);
	}
	my @list = ();
	for(my $i=0;$i<@db;$i++){
		my @r = split(/\t/,$db[$i]);
		my $id = $r[0];
		my $name = (split(/<br>/,$r[6]))[0];
		my $qty = grep(/\t${id}\t/,@db);
		push @list,"\{id: '${id}',name: '${name}',qty: ${qty}\}";
	}
	my $list = join("\,",@list);
	
	##
	my @path = ();
	unshift @path,"\{id: 'root',name: 'root'\}";
	$path = join("\,",@path);
	
	## Logs
	@logs = grep(!/\t\[C\]\t/,@logs);
	@logs = grep(!/\t\[S\]\t/,@logs);
	@logs = grep(!/\t\[E\]\t/,@logs);
	@logs = sort { (split(/\t/,$a))[4] cmp (split(/\t/,$b))[4]} @logs;
	my @log = ();
	for(my $i=@logs-1;$i >= 0;$i--){
		push @log,&_JSON_LOGS($logs[$i]);
	}
	my $logs = join("\,",@log);
	
	## Todo
	@logs = grep(/\t1\t/,@logs);
	my @todo = ();
	for(my $i=0;$i<@logs;$i++){
		my @r = split(/\t/,$logs[$i]);
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
			unshift @todo,"\{id: '${r[0]}',user: '${r[2]}',date: '${r[4]}',text: '${r[9]}',worktime: ${r[7]},timer: ${timer},time: ${time},parentName: '${parentName}'\}";
		}
	}
	my $todo = join("\,",@todo);
	
	#$_RESULT{'json'} = "web.App.search.action.callback(\[${list}\],\[${logs}\],\[${todo}\],\[${path}\],${index},'$_GET{'id'}','${parent[1]}');";
	$_RESULT{'json'} = "web.App.search.action.callback(\[${list}\],\[${logs}\],\[${todo}\],\[${path}\],${index},'root','');";
}
else {
	$_RESULT{'404'} = 1;
}
1;
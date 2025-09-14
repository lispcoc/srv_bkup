if($_GET{'key'} eq $config{'keycode'} && $_GET{'id'} ne $null){
	&_LIB('JSON'); ##
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	
	my @db = &_DB($path);
	@db = sort { (split(/\t/,$b))[4] cmp (split(/\t/,$a))[4]} @db;
	my @parentNode = @db;
	my @parent = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	
	## 
	my @current = grep(/\t$_GET{'id'}\t/,@db);
	my @list = ();
	for(my $i=0;$i<@current;$i++){
		my @r = split(/\t/,$current[$i]);
		my $id = $r[0];
		my $name = (split(/<br>/,$r[6]))[0];
		my $qty = grep(/\t${id}\t/,@db);
		push @list,"\{id: '${id}',name: '${name}',qty: ${qty}\}";
	}
	my $list = join("\,",@list);
	
	##
	my @path = ();
	if($_GET{'id'} ne 'root'){
		my @p = @parent;
		my $name = (split(/<br>/,$p[6]))[0];
		@path = ("\{id: '${p[0]}',name: '${name}'\}");
		my $safe = 100;
		while($p[1] ne 'root' && $safe > 0){
			@p = split(/\t/,(grep(/^$p[1]\t/,@db))[0]);
			my $name = (split(/<br>/,$p[6]))[0];
			unshift @path,"\{id: '${p[0]}',name: '${name}'\}";
			$safe--;
		}
	}
	unshift @path,"\{id: 'root',name: 'root'\}";
	$path = join("\,",@path);
	
	## Logs
	my $lpath = "$config{'dir.data'}logs.cgi";
	my @db = &_DB($lpath);
	@db = grep(!/\t\[C\]\t/,@db);
	@db = grep(!/\t\[S\]\t/,@db);
	@db = grep(!/\t\[E\]\t/,@db);
	@db = sort { (split(/\t/,$a))[4] cmp (split(/\t/,$b))[4]} @db;
	if($_GET{'id'} ne 'root'){
		@db = grep(/\t$_GET{'id'}\t/,@db);
	}
	my $index = @db;
	my @logs = ();
	for(my $i=@db-1;$i >= 0 && @logs < 50;$i--){
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
	
	if($_GET{'callback'}){
		my $callback = $_GET{'callback'};
		$_RESULT{'json'} = "${callback}(\[${logs}\],\[${todo}\]);";
	}
	else {
		$_RESULT{'json'} = "web.App.data.action.rebuild(\[${list}\],\[${logs}\],\[${todo}\],\[${path}\],${index},'$_GET{'id'}','${parent[1]}');";
	}
}
else {
	$_RESULT{'404'} = 1;
}
1;
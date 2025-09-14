if($_GET{'key'} eq $config{'keycode'} && $_GET{'id'} ne $null && $_GET{'index'} ne $null){
	&_LIB('JSON'); ##
	$template = '';
	
	my @parentNode = &_DB("$config{'dir.data'}webpad.cgi");
	
	## Logs
	my $lpath = "$config{'dir.data'}logs.cgi";
	my @db = &_DB($lpath);
	my $index = @db;
	my @logs = ();
	for(my $i=$_GET{'index'};$i < @db;$i++){
		my @r = split(/\t/,$db[$i]);
		my $parentName = '';
		if($r[1] ne 'root'){
			my @p = grep(/^${r[1]}\t/,@parentNode);
			@p = split(/\t/,$p[0]);
			@p = split(/<br>/,$p[6]);
			$parentName = $p[0];
		}
		push @logs,&_JSON_LOGS($db[$i],$parentName);
	}
	my $logs = join("\,",@logs);
	
	$_RESULT{'json'} = "web.App.data.action.update(\[${logs}\]);";
}
else {
	$_RESULT{'404'} = 1;
}
1;
if($_GET{'key'} eq $config{'keycode'} && $_GET{'from'} ne $null && $_GET{'to'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}logs.cgi";
	my @db = &_DB($path);
	my ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime,$location,$text) = split(/\t/,(grep(/^$_GET{'from'}\t/,@db))[0]);
	@db = grep(!/^$_GET{'from'}\t/,@db);
	$parent = $_GET{'to'};
	my @log = ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime+$time,$location,$text);
	push @db,join("\t",@log);
	@db = sort { (split(/\t/,$a))[0] cmp (split(/\t/,$b))[0]} @db;
	my $db = join("\n",@db) . "\n";
	&_SAVE($path,$db);
	
	my @parent = &_DB("$config{'dir.data'}webpad.cgi");
	@parent = split(/\t/,(grep(/^$_GET{'to'}\t/,@parent))[0]);
	my $parentName = (split(/<br>/,$parent[6]))[0];
	$_RESULT{'json'} = "web.App.todo.action.dragTodoCallback(\'$_GET{'from'}\',\'${parentName}\',\'$_GET{'to'}\');";
}
else {
	$_RESULT{'json'} = "web.App.todo.action.dragTodoCallback(3);";
}
1;
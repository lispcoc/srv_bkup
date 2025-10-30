if($_GET{'key'} eq $config{'keycode'} && $_GET{'id'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}logs.cgi";
	my @db = &_DB($path);
	my ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime,$location,$text) = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	if($_GET{'id'} eq $id){
		my $token = "$config{'dir.data'}timer/$_GET{'id'}.cgi";
		my $time = 0;
		if(-f $token){
			$time = time - (stat $token)[9];
			unlink $token;
		}
		my $cid = &_ID;
		@db = grep(!/^$_GET{'id'}\t/,@db);
		my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
		my $fdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
		my $dtoken = sprintf("%04d%02d%02d",$year+1900,$mon+1,$day);
		my @log = ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime+$time,$location,$text);
		push @db,join("\t",@log);
		my @todo = ($cid,$parent,$_USER{'id'},$fdate,$id,$time,'c','','',$text,'[C]',"\t");
		push @db,join("\t",@todo);
		@db = sort { (split(/\t/,$a))[0] cmp (split(/\t/,$b))[0]} @db;
		my $db = join("\n",@db) . "\n";
		&_SAVE($path,$db);
		&_COUNTUP("./data/task/${userid}_task.cgi");
		&_COUNTUP("./data/task/${userid}_${dtoken}_task.cgi");
		
		my $index = @db;
		&_SAVE("$config{'dir.data'}index.json","web.App.data.action.index(${index});");
		$_RESULT{'json'} = "web.App.todo.action.callback(1);";
		## ics
		@db = grep(!/\t\[C\]\t/,@db);
		@db = grep(!/\t\[S\]\t/,@db);
		@db = grep(!/\t\[E\]\t/,@db);
		@db = grep(/\t1\t/,@db);
		&_SAVE("$config{'dir.ics'}$config{'keycode'}.ics",&_ICAL(@db));
		## ics
	}
	else {
		$_RESULT{'json'} = "web.App.todo.action.callback(2);";
	}
}
else {
	$_RESULT{'json'} = "web.App.todo.action.callback(3);";
}
1;
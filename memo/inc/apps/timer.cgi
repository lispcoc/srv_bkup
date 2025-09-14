if($_GET{'key'} eq $config{'keycode'} && $_GET{'id'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}logs.cgi";
	my $token = "$config{'dir.data'}timer/$_GET{'id'}.cgi";
	my @db = &_DB($path);
	my ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime,$location,$text) = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	if(-f $token){
		my $time = time - (stat $token)[9];
		@db = grep(!/^$_GET{'id'}\t/,@db);
		$worktime+=$time;
		my @log = ($id,$parent,$userid,$cdate,$tdate,$fdate,$todo,$worktime,$location,$text);
		push @db,join("\t",@log);
		
		## Timer end log
		my $cid = &_ID;
		my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
		my $fdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
		my @timer = ($cid,$worktime,$_USER{'id'},$fdate,$id,'','e','','',"",'[E]',"\t");
		push @db,join("\t",@timer);
		
		@db = sort { (split(/\t/,$a))[0] cmp (split(/\t/,$b))[0]} @db;
		my $db = join("\n",@db) . "\n";
		&_SAVE($path,$db);
		
		## $_RESULT{'json'} = "web.App.todo.action.timerCallback(false,'${id}',${worktime});";
		$_RESULT{'json'} = "web.App.todo.action.callback('timer end');";
		unlink $token;
		
		my $index = @db;
		&_SAVE("$config{'dir.data'}index.json","web.App.data.action.index(${index});");
	}
	else {
		if($_GET{'id'} eq $id){
			$worktime += 0;
			&_SAVE($token,"");
			#$_RESULT{'json'} = "web.App.todo.action.timerCallback(true,'${id}',${worktime});";
			$_RESULT{'json'} = "web.App.todo.action.callback('timer start');";
			
			## Timer start log
			my $cid = &_ID;
			my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
			my $fdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
			my @timer = ($cid,$worktime,$_USER{'id'},$fdate,$id,'','s','','',"",'[S]',"\t");
			&_ADDSAVE($path,join("\t",@timer));
			my $index = @db + 1;
			&_SAVE("$config{'dir.data'}index.json","web.App.data.action.index(${index});");
		}
		else {
			$_RESULT{'json'} = "web.App.todo.action.timerCallback(2);";
		}
	}
}
else {
	$_RESULT{'json'} = "web.App.todo.action.timerCallback(3);";
}
1;
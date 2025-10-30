if($_GET{'key'} eq $config{'keycode'} && $_GET{'from'} ne $null && $_GET{'to'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	my @db = &_DB($path);
	my @pad = split(/\t/,(grep(/^$_GET{'from'}\t/,@db))[0]);
	@db = grep(!/^$_GET{'from'}\t/,@db);
	$pad[1] = $_GET{'to'};
	push @db,join("\t",@pad);
	@db = sort { (split(/\t/,$b))[4] cmp (split(/\t/,$a))[4]} @db;
	&_SAVE($path,join("\n",@db));
	my $qty = grep(/\t$_GET{'to'}\t/,@db);
	$_RESULT{'json'} = "web.App.explorer.action.dragNoteCallback(\'$_GET{'from'}\',\'$_GET{'to'}\',${qty});";
}
else {
	$_RESULT{'404'} = 1;
}
1;
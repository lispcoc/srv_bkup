if($_GET{'key'} eq $config{'keycode'} && $_GET{'type'} eq 'ics'){
	$template = "";
	my @db = &_DB("$config{'dir.data'}logs.cgi");
	@db = grep(!/\t\[C\]\t/,@db);
	@db = grep(!/\t\[S\]\t/,@db);
	@db = grep(!/\t\[E\]\t/,@db);
	@db = grep(/\t1\t/,@db);
	$_RESULT{'ics'} = &_ICAL(@db);
}
else {
	$_RESULT{'404'} = 1;
}
1;
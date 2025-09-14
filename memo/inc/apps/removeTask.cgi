if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	my @db = &_DB("$config{'dir.task'}$_USER{'id'}.cgi");
	@db = grep(!/^$_GET{'id'}\t/,@db);
	$hash = '#updated';
	&_SAVE("$config{'dir.task'}$_USER{'id'}.cgi",join("\n",@db));
	$_RESULT{'redirect'} = "index.cgi?key=$_GET{'key'}&app=task${hash}";
}
else {
	$_RESULT{'404'} = 1;
}
1;
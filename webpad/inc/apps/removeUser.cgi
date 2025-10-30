if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi" && $_GET{'id'} ne $null && !-f "$config{'dir.data'}demo.cgi"){
	$template = "index.tpl";
	my @db = &_DB($config{'file.user'});
	@db = grep(!/^$_GET{'id'}\t/,@db);
	&_SAVE($config{'file.user'},join("\n",@db));
}
else {
	$_RESULT{'404'} = 1;
}
$_RESULT{'redirect'} = "index.cgi?key=$_GET{'key'}&app=setting#removed";
1;
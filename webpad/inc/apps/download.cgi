if($_GET{'key'} eq $config{'keycode'}){
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	my @db = &_DB($path);
	my @p = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	my $name = (split(/<br>/,$p[6]))[0];
	$_RESULT{'filename'} = "${name}.txt";
	#$_RESULT{'download'} = $p[6] . "\x{feff}";
	$_RESULT{'bom'} = "\x{feff}";
	$_RESULT{'download'} = &_UNSANITIZING($p[6]);
	#$_RESULT{'download'} = &_UNSANITIZING($p[6]);
}
else {
	$_RESULT{'404'} = 1;
}
1;
if($_GET{'key'} eq $config{'keycode'}){
	$template = '';
	my $path = "$config{'dir.data'}cycle/$_USER{'id'}.cgi";
	my $result = 0;
	if(-f $path){
		$result = 0;
		unlink $path;
	}
	else {
		$result = time * 1000;
		&_SAVE($path,"");
	}
	$_RESULT{'json'} = "web.App.lifecycle.action.callback(${result});";
}
else {
	$_RESULT{'json'} = "web.App.lifecycle.action.callback(3);";
}
1;
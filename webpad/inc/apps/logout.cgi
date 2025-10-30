if($_GET{'key'} eq $config{'keycode'}){
	if(-f "$config{'dir.session'}/$_COOKIE{'session'}.cgi"){
		unlink "$config{'dir.session'}/$_COOKIE{'session'}.cgi";
	}
	$_COOKIE{'session'} = "";
	$_RESULT{'redirect'} = "index.cgi?key=$_GET{'key'}";
}
else {
	$_RESULT{'404'} = 1;
}
1;
if($config{'keycode'} eq $null){
	$_VAL{'title'} = 'Install';
	if($_POST{'password'} eq $_POST{'repassword'} && $_POST{'password'} ne $null && $_POST{'userid'} ne $null){
		my $passcode = &_HASH($_POST{'password'});
		my $keycode = &_PASSCODE($config{'keycode.digit'});
		&_SAVE($config{'file.key'},"\$config\{\'keycode\'\} = \'${keycode}\';\n1;");
		&_SAVE($config{'file.user'},"$_POST{'userid'}\t${passcode}");
		$_RESULT{'redirect'} = '?key=' . $keycode;
		if(-f "./data/pad.cgi"){
			my @db = &_DB("./data/pad.cgi");
			my @pads = ();
			for(my $i=0;$i<@db;$i++){
				my($id,$text,$createDate,$update,$worktime) = split(/\t/,$db[$i]);
				$text =~ s/\\\\n/<br>/ig;
				my @pad = ($id,'root',$_POST{'userid'},$createDate,$update,$worktime,$text);
				push @pads,join("\t",@pad);
			}
			&_SAVE("./data/webpad.cgi",join("\n",@pads));
		}
	}
	else {
		my $error = "";
		if($_POSTED){
			$error = "<p class=\"error\">_%%error%%_</p>";
		}
		$_VAL{'content'} = <<"		__HTML__";
			<form id="install" method="POST" novalidate>
				<table>
					<tr>
						<th>_%%userid%%_</th>
						<td><input type="email" name="userid" placeholder="_%%userid%%_"></td>
					</tr>
					<tr>
						<th>_%%password%%_</th>
						<td><input type="password" name="password" placeholder="_%%password%%_"></td>
					</tr>
					<tr>
						<th>_%%repassword%%_</th>
						<td><input type="password" name="repassword" placeholder="_%%repassword%%_"></td>
					</tr>
					<tr>
						<td colspan="2">
							${error}
							<button>_%%install%%_</button>
						</td>
					</tr>
				</table>
			</form>
		__HTML__
	}
}
else {
	$_RESULT{'404'} = 1;
}

1;
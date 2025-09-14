if($_GET{'key'} eq $config{'keycode'}){
	$_VAL{'title'} = '_%%login%%_';
	my @user = &_RECORD($config{'file.user'},$_POST{'userid'});
	my $password = &_HASH($_POST{'password'});
	if($user[1] eq $password && $_POST{'password'} ne $null && $user[0] eq $_POST{'userid'}){
		## Successful
		$_COOKIE{'session'} = &_SESSION;
		&_SAVE("$config{'dir.session'}/$_COOKIE{'session'}.cgi","\$_USER\{\'id\'\} = \'${user[0]}\';\n1;");
		$_RESULT{'redirect'} = '?key=' . $_GET{'key'};
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
						<td colspan="2">
							${error}
							<div class="right">
								<button>_%%login%%_</button>
							</div>
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
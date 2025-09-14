if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	$template = "index.tpl";
	$_VAL{'title'} = '_%%index%%_';
	if($_POST{'title'} ne $null){
		my @db = &_DB($config{'file.user'});
		my($id,$pw) = split(/\t/,(grep(/^$_POST{'title'}\t/,@db))[0]);
		if($_POST{'title'} eq $id){
			@db = grep(!/^$_POST{'title'}\t/,@db);
			if($_POST{'email'} ne $pw){
				$pw = &_HASH($_POST{'email'});
			}
			$hash = '#updated';
		}
		else {
			$hash = '#added';
			$id = $_POST{'title'};
			$pw = &_HASH($_POST{'email'});
		}
		my @user = ($id,$pw);
		push @db,join("\t",@user);
		&_SAVE($config{'file.user'},join("\n",@db));
		if($_POST{'picture'} && $_BINTYPE{"picture_0"} eq 'jpg'){
			&_BINSAVE("$config{'dir.picture'}${id}.jpg",$_BIN{'picture_0'});
		}
		$_RESULT{'redirect'} = "index.cgi?key=$_GET{'key'}&app=setting${hash}";
	}
	else {
		my $label = '_%%add%%_';
		my $current = " current";
		$_VAL{'title'} = '_%%add%%_';
		my($id,$pw,$type) = &_RECORD($config{'file.user'},$_GET{'id'});
		my $uri = "";
		my $readonly = "";
		if($id eq $_GET{'id'} && $id ne $null){
			$label = '_%%update%%_';
			$current = "";
			$_VAL{'title'} = '_%%update%%_';
			$readonly = " readonly=\"readonly\"";
		}
		$_VAL{'nav'} = <<"		__HTML__";
			<nav>
				<ul>
					<li><a href="?key=$_GET{'key'}&app=setting" class="icon index current">_%%index%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=task" class="icon add">_%%app_dailytask%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=error" class="icon error">_%%errhistory%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=logout" class="icon logout">_%%logout%%_</a></li>
				</ul>
			</nav>
		__HTML__
		$_VAL{'content'} = <<"		__HTML__";
			<div class="container">
				<form id="add" method="POST" enctype="multipart/form-data" onsubmit="return web.App.overlay.action.posted();">
					<dl>
						<dt>_%%threadtitle%%_</dt>
						<dd><input type="text" name="title" value="${id}" placeholder="_%%threadtitle%%_"${readonly}></dd>
						
						<dt>_%%password%%_</dt>
						<dd><input type="password" name="email" value="${pw}" placeholder="_%%password%%_"></dd>
						
						<dt>_%%picture%%_</dt>
						<dd><input type="file" name="picture" value="" placeholder="_%%noticeemail%%_" accept=".jpg,.jpeg"></dd>
					</dl>
					<div class="right">
						<button>${label}</button>
					</div>
				</form>
			</div>
		__HTML__
	}
}
else {
	$_RESULT{'404'} = 1;
}
1;
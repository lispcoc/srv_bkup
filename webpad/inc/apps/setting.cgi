if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	$template = "index.tpl";
	$_VAL{'title'} = '_%%index%%_';
	my @db = &_DB($config{'file.user'});
	my @tr = ();
	for(my $i=0;$i<@db;$i++){
		my ($id,$pw) = split(/\t/,$db[$i]);
		my $tr = <<"		__HTML__";
			<li>
				<a href="?key=$_GET{'key'}&app=add&id=${id}" class="title">${id}</a>
				<ul>
					<li><a href="?key=$_GET{'key'}&app=add&id=${id}" class="icon edit">_%%edit%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=removeUser&id=${id}" class="icon remove" data-alert="_%%remove_alert%%_">_%%remove%%_</a></li>
				</ul>
			</li>
		__HTML__
		push @tr,$tr;
	}
	if(@tr < 1){
		push @tr,"<li>_%%notfound%%_</li>";
	}
	@tr = sort { $b cmp $a } @tr;
	my $tr = join("\n",@tr);
	$_VAL{'nav'} = <<"	__HTML__";
		<nav>
			<ul>
				<li><a href="?key=$_GET{'key'}&app=setting" class="icon index current">_%%index%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=task" class="icon add">_%%app_dailytask%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=error" class="icon error">_%%errhistory%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=logout" class="icon logout">_%%logout%%_</a></li>
			</ul>
		</nav>
	__HTML__
	$_VAL{'content'} = <<"	__HTML__";
		<div class="container">
			<div class="index">
				<ul>
					${tr}
				</ul>
				<div class="button">
					<button onclick="location.href='?key=$_GET{'key'}&app=add'">_%%add%%_</button>
				</div>
			</div>
		</div>
		<div class="status" id="status_added">_%%added%%_</div>
		<div class="status" id="status_updated">_%%updated%%_</div>
		<div class="status" id="status_removed">_%%removed%%_</div>
		<script>
			var timeagoStrings = '_%%timeago%%_';
			web.App.check.action.init();
		</script>
	__HTML__
}
else {
	$_RESULT{'404'} = 1;
}
1;
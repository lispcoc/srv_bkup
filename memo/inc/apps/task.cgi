if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	$template = "index.tpl";
	$_VAL{'title'} = '_%%app_dailytask%%_';
	my @db = &_DB("$config{'dir.task'}$_USER{'id'}.cgi");
	my @tr = ();
	for(my $i=0;$i<@db;$i++){
		my ($id,$title) = split(/\t/,$db[$i]);
		my $tr = <<"		__HTML__";
			<li>
				<a href="?key=$_GET{'key'}&app=addtask&id=${id}" class="title">${title}</a>
				<ul>
					<li><a href="?key=$_GET{'key'}&app=addtask&id=${id}" class="icon edit">_%%edit%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=removeTask&id=${id}" class="icon remove" data-alert="_%%remove_alert%%_">_%%remove%%_</a></li>
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
				<li><a href="?key=$_GET{'key'}&app=setting" class="icon index">_%%index%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=task" class="icon add current">_%%app_dailytask%%_</a></li>
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
					<button onclick="location.href='?key=$_GET{'key'}&app=addtask'">_%%task_add%%_</button>
				</div>
			</div>
		</div>
		<div class="status" id="status_added">_%%task_added%%_</div>
		<div class="status" id="status_updated">_%%task_updated%%_</div>
		<div class="status" id="status_removed">_%%task_removed%%_</div>
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
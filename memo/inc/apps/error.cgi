if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	$template = "index.tpl";
	$_VAL{'title'} = '_%%errhistory%%_';
	my @db = &_DB($config{'file.error'});
	my @tr = ();
	for(my $i=0;$i<@db;$i++){
		my ($time,$ip,$host,$ua) = split(/\t/,$db[$i]);
		my $tr = <<"		__HTML__";
			<li>
				<ul>
					<li><span>${ip}</span></li>
					<li><span data-time="${time}000" class="timeago"></span></li>
				</ul>
				<span class="title">${host}<br><span>${ua}</span></span>
			</li>
		__HTML__
		unshift @tr,$tr;
	}
	if(@tr < 1){
		push @tr,"<li>_%%errnotfound%%_</li>";
	}
	my $tr = join("\n",@tr);
	$_VAL{'nav'} = <<"	__HTML__";
		<nav>
			<ul>
				<li><a href="?key=$_GET{'key'}&app=setting" class="icon index">_%%index%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=add" class="icon add">_%%add%%_</a></li>
				<li><a href="?key=$_GET{'key'}&app=error" class="icon error current">_%%errhistory%%_</a></li>
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
			</div>
		</div>
		<script>
			var timeagoStrings = '_%%timeago%%_';
		</script>
	__HTML__
}
else {
	$_RESULT{'404'} = 1;
}
1;
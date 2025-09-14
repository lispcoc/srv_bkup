if($_GET{'key'} eq $config{'keycode'} && -f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
	$template = "./index.tpl";
	$_VAL{'title'} = '_%%task_add%%_';
	if($_POST{'title'} ne $null){
		my @db = &_DB("$config{'dir.task'}$_USER{'id'}.cgi");
		if($_POST{'id'}){
			@db = grep(!/^$_POST{'id'}\t/,@db);
			$hash = '#updated';
		}
		else {
			$_POST{'id'} = time;
			$hash = '#added';
		}
		my @data = ($_POST{'id'},$_POST{'title'},$_POST{'week_0'},$_POST{'week_1'},$_POST{'week_2'},$_POST{'week_3'},$_POST{'week_4'},$_POST{'week_5'},$_POST{'week_6'});
		push @db,join("\t",@data);
		&_SAVE("$config{'dir.task'}$_USER{'id'}.cgi",join("\n",@db));
		$_RESULT{'redirect'} = "index.cgi?key=$_GET{'key'}&app=task${hash}";
	}
	else {
		my $label = '_%%task_add%%_';
		my $current = " current";
		$_VAL{'title'} = '_%%task_add%%_';
		my($id,$title,$w0,$w1,$w2,$w3,$w4,$w5,$w6) = &_RECORD("$config{'dir.task'}$_USER{'id'}.cgi",$_GET{'id'});
		my @w = ();
		if($id eq $_GET{'id'} && $id ne $null){
			$label = '_%%task_update%%_';
			$current = "";
			$_VAL{'title'} = '_%%task_update%%_';
			if($w0){
				$w[0] = " checked";
			}
			if($w1){
				$w[1] = " checked";
			}
			if($w2){
				$w[2] = " checked";
			}
			if($w3){
				$w[3] = " checked";
			}
			if($w4){
				$w[4] = " checked";
			}
			if($w5){
				$w[5] = " checked";
			}
			if($w6){
				$w[6] = " checked";
			}
			
		}
		$_VAL{'nav'} = <<"		__HTML__";
			<nav>
				<ul>
					<li><a href="?key=$_GET{'key'}&app=setting" class="icon index">_%%index%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=task" class="icon add current">_%%app_dailytask%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=error" class="icon error">_%%errhistory%%_</a></li>
					<li><a href="?key=$_GET{'key'}&app=logout" class="icon logout">_%%logout%%_</a></li>
				</ul>
			</nav>
		__HTML__
		$_VAL{'content'} = <<"		__HTML__";
			<div class="container">
				<form id="add" method="POST" enctype="multipart/form-data" onsubmit="return web.App.overlay.action.posted();">
					<input type="hidden" name="id" value="${id}">
					<dl>
						<dt>_%%task_threadtitle%%_</dt>
						<dd><input type="text" name="title" value="${title}" placeholder="_%%task_threadtitle%%_"></dd>
						
						<dt>_%%negative%%_</dt>
						<dd>
							<label><input type="checkbox" name="week_0" value="1"${w[0]}>_%%negative%%_</label>
							<div style="display: none;">
								<label><input type="checkbox" name="week_1" value="1"${w[1]}>_%%week_1%%_</label>
								<label><input type="checkbox" name="week_2" value="1"${w[2]}>_%%week_2%%_</label>
								<label><input type="checkbox" name="week_3" value="1"${w[3]}>_%%week_3%%_</label>
								<label><input type="checkbox" name="week_4" value="1"${w[4]}>_%%week_4%%_</label>
								<label><input type="checkbox" name="week_5" value="1"${w[5]}>_%%week_5%%_</label>
								<label><input type="checkbox" name="week_6" value="1"${w[6]}>_%%week_6%%_</label>
							</div>
						</dd>
					</dl>
					<div class="right">
						<button>${label}</button>
					</div>
				</form>
			</div>
		__HTML__
		my @w = split(/\,/,$_LANG{'calendar_week'});
		for(my $i=0;$i<@w;$i++){
			$_VAL{'content'} =~ s/_%%week_${i}%%_/${w[$i]}/ig;
		}
	}
}
else {
	$_RESULT{'404'} = 1;
}
1;
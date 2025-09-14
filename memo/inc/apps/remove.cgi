if($_GET{'key'} eq $config{'keycode'}){
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	
	my @db = &_DB($path);
	my @pad = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	@db = grep(!/^$_GET{'id'}\t/,@db);
	push @db,join("\t",@data);
	@db = sort { (split(/\t/,$b))[4] cmp (split(/\t/,$a))[4]} @db;
	&_SAVE($path,join("\n",@db));
	
	## 
	my @current = grep(/\t${pad[1]}\t/,@db);
	my @list = ();
	for(my $i=0;$i<@current;$i++){
		my @r = split(/\t/,$current[$i]);
		my $id = $r[0];
		my $name = (split(/<br>/,$r[6]))[0];
		my $qty = grep(/\t${id}\t/,@db);
		push @list,"\{id: '${id}',name: '${name}',qty: ${qty}\}";
	}
	my $list = join("\,",@list);
	
	##
	my @path = ();
	if($pad[1] ne 'root'){
		my @p = split(/\t/,(grep(/^${pad[1]}\t/,@db))[0]);
		my $name = (split(/<br>/,$p[6]))[0];
		@path = ("\{id: '${p[0]}',name: '${name}'\}");
		my $safe = 100;
		while($p[1] ne 'root' && $safe > 0){
			@p = split(/\t/,(grep(/^$p[1]\t/,@db))[0]);
			my $name = (split(/<br>/,$p[6]))[0];
			unshift @path,"\{id: '${p[0]}',name: '${name}'\}";
			$safe--;
		}
	}
	unshift @path,"\{id: 'root',name: 'root'\}";
	$path = join("\,",@path);
	$_RESULT{'json'} = "web.App.note.action.removeCallback(\[${list}\],\[${path}\]);";
}
else {
	$_RESULT{'404'} = 1;
}
1;
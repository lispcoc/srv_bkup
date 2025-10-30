#[0] $id
#[1] $parent
#[2] $userid
#[3] $cdate
#[4] $udate
#[5] $_POST{'form_worktime'}
#[6] $_POST{'form_text'}
#[7] $_POST{'form_public'}

if($_GET{'key'} eq $config{'keycode'}){
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	
	my $id = $_POST{'form_id'};
	if(!$id){
		$id = &_ID;
	}
	
	my $parent = $_POST{'form_parent'};
	if(!$parent || $parent eq $id){
		$parent = 'root';
	}
	
	my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
	my $udate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
	my $cdate = $udate;
	
	my @db = &_DB($path);
	my @pad = split(/\t/,(grep(/^${id}\t/,@db))[0]);
	@db = grep(!/^${id}\t/,@db);
	if($pad[3]){
		$cdate = $pad[3];
	}
	if($pad[1]){
		$parent = $pad[1];
	}
	
	my $userid = $_USER{'id'};
	if($pad[2]){
		$userid = $pad[2];
	}
	if(!$_POST{'form_public'}){
		$_POST{'form_public'} = 0;
	}
	else {
		$_POST{'form_public'} = 1;
	}
	my $title = (split(/<br>/,$_POST{'form_text'}))[0];
	my @data = ($id,$parent,$userid,$cdate,$udate,$_POST{'form_worktime'},$_POST{'form_text'},$_POST{'form_public'});
	push @db,join("\t",@data);
	@db = sort { (split(/\t/,$b))[4] cmp (split(/\t/,$a))[4]} @db;
	&_SAVE($path,join("\n",@db));
	
	## 
	my @current = grep(/\t${parent}\t/,@db);
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
	if($parent ne 'root'){
		my @p = split(/\t/,(grep(/^${parent}\t/,@db))[0]);
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
	$_RESULT{'html'} = "<script>window.parent.web.App.note.action.saveCallback('${id}','${parent}',\[${list}\],\[${path}\],'${title}','${udate}')</script>";
}
else {
	$_RESULT{'404'} = 1;
}
1;
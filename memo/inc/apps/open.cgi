if($_GET{'key'} eq $config{'keycode'} && $_GET{'id'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}webpad.cgi";
	
	my @db = &_DB($path);
	my @p = split(/\t/,(grep(/^$_GET{'id'}\t/,@db))[0]);
	my $name = (split(/<br>/,$p[6]))[0];
	## my @data = ($id,$parent,$userid,$cdate,$udate,$_POST{'form_worktime'},$_POST{'form_text'});
	my $publicStatus = 0;
	if($p[7]){
		$publicStatus = 1;
	}
	$p[6] =~ s/&nbsp;/ /ig;
	$p[6] =~ s/\'/&apos;/ig;
	$_RESULT{'json'} = "web.App.note.action.openCallback(\{id: '${p[0]}',name: '${name}',parent: '${p[1]}',createDate: '${p[3]}',updateDate: '${p[4]}',worktime: '${p[5]}',text: '${p[6]}',public: ${publicStatus}\});";
}
else {
	$_RESULT{'404'} = 1;
}
1;
if($_GET{'key'} eq $config{'keycode'} && $_POST{'form_text'} ne $null){
	$template = '';
	my $path = "$config{'dir.data'}logs.cgi";
	
	my $id = $_POST{'form_id'};
	if(!$id){
		$id = &_ID;
	}
	
	my $parent = $_POST{'form_parent'};
	if(!$parent || $parent eq $id){
		$parent = 'root';
	}
	
	my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
	my $cdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
	#my $fdate = $udate; ## Finish Date
	#my $tdate = ""; ## Target Date
	
	my @db = &_DB($path);
	my $index = @db + 1;
	my @pad = split(/\t/,(grep(/^${id}\t/,@db))[0]);
	@db = grep(!/^${id}\t/,@db);
	if($pad[3]){
		$cdate = $pad[3];
	}
	
	my $userid = $_USER{'id'};
	if($pad[2]){
		$userid = $pad[2];
	}
	
	if($_POST{'form_text'} ne $null){
		## tday
		my $tdate = &_DATE($_POST{'form_text'},time);
		my @data = ($id,$parent,$userid,$cdate,$tdate,$fdate,$_POST{'form_todo'},$worktime,$location,$_POST{'form_text'});
		&_ADDSAVE($path,join("\t",@data));
		#push @db,join("\t",@data);
		#@db = sort { (split(/\t/,$a))[4] cmp (split(/\t/,$b))[4]} @db;
		#&_SAVE($path,join("\n",@db));
		&_SAVE("$config{'dir.data'}index.json","web.App.data.action.index(${index});");
		$_RESULT{'html'} = "<script>window.parent.web.App.logs.action.callback()</script>";
		# $_RESULT{'html'} = "<script>alert('Success')</script>";
		
		## ics
		push @db,join("\t",@data);
		@db = grep(!/\t\[C\]\t/,@db);
		@db = grep(!/\t\[S\]\t/,@db);
		@db = grep(!/\t\[E\]\t/,@db);
		@db = grep(/\t1\t/,@db);
		&_SAVE("$config{'dir.ics'}$config{'keycode'}.ics",&_ICAL(@db));
		## ics
	}
}
else {
	#$_RESULT{'404'} = 1;
	$_RESULT{'html'} = "<script>window.parent.web.App.logs.action.callback()</script>";
}

sub _DATE {
	my($str,$Time) = @_;
	my $date;
	my ($sec,$min,$hour,$day,$mon,$year) = localtime($Time);
	$wday{'日'} = 0;
	$wday{'月'} = 1;
	$wday{'火'} = 2;
	$wday{'水'} = 3;
	$wday{'木'} = 4;
	$wday{'金'} = 5;
	$wday{'土'} = 6;
	
	$nday{'今日'} = 0;
	$nday{'明日'} = 1;
	$nday{'明後日'} = 2;
	$nday{'明明後日'} = 3;
	$nday{'昨日'} = -1;
	$nday{'一昨日'} = -2;
	
	$nday{'後'} = 1;
	$nday{'間'} = 1;
	$nday{'前'} = -1;
	$mon++;$year += 1900;
	if($str =~ /^([0-9][0-9]|[0-9])秒(後|間|前)/si){
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($1*$nday{$2}));$mon++;$year += 1900;
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	elsif($str =~ /^([0-9][0-9]|[0-9])分(後|間|前)/si){
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($1*60*$nday{$2}));$mon++;$year += 1900;
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	elsif($str =~ /^([0-9][0-9]|[0-9])時間(後|間|前)/si){
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($1*60*60*$nday{$2}));$mon++;$year += 1900;
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	elsif($str =~ /^([0-9][0-9][0-9]|[0-9][0-9]|[0-9])日(後|間|前)/si){
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($1*60*60*24*$nday{$2}));$mon++;$year += 1900;
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	elsif($str =~ /^([0-9][0-9][0-9]|[0-9][0-9]|[0-9])年(後|間|前)/si){
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time);$mon++;$year += 1900 + ($1*$nday{$2});
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	elsif($str =~ /^([0-1][0-9]|[0-9])月([0-3][0-9]|[0-9])日(.*?)$/si){
		## MM月DD日
		$M = $1;$D = $2;
		if($3 =~ /^([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,$2,0);
		}
		elsif($3 =~ /^([0-5][0-9]|[0-9])時/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,0,0);
		}
		elsif($3 =~ /^([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,$2,0);
		}
		else {
			$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$M,$D);
		}
	}
	elsif($str =~ /^([0-3][0-9]|[0-9])日(.*?)$/si){
		## DD日
		$M = $mon;$D = $1;
		if($2 =~ /^([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,$2,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])時/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,0,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$M,$D,$1,$2,0);
		}
		else {
			$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$M,$D);
		}
	}
	elsif($str =~ /^([0-1][0-9]|[0-9])月([0-3][0-9]|[0-9])日([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$1,$2,$3,$4,0);
	}
	elsif($str =~ /^([0-1][0-9]|[0-9])\/([0-3][0-9]|[0-9]) ([0-2][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$1,$2,$3,$4,0);
	}
	elsif($str =~ /^([0-3][0-9]|[0-9])日([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$1,$2,$3,0);
	}
	elsif($str =~ /^([0-3][0-9]|[0-9])日([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$1,$2,$3,0);
	}
	elsif($str =~ /^([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
	}
	elsif($str =~ /^([0-5][0-9]|[0-9])時/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,0,0);
	}
	elsif($str =~ /^([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
	}
	elsif($str =~ /^([0-9][0-9][0-9][0-9])\/([0-1][0-9]|[0-9])\/([0-3][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$1,$2,$3);
	}
	elsif($str =~ /^([0-1][0-9]|[0-9])\/([0-3][0-9]|[0-9])/si){
		$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$1,$2);
	}
	elsif($str =~ /^([0-9][0-9][0-9][0-9]|[0-9][0-9])年([0-1][0-9]|[0-9])月([0-3][0-9]|[0-9])日/si){
		$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$1,$2,$3);
	}
	elsif($str =~ /^([0-1][0-9]|[0-9])月([0-3][0-9]|[0-9])日/si){
		$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$1,$2);
	}
	elsif($str =~ /^(今日|明日|明後日|明明後日)中/si){
		$date =  &_FDATE($year,$mon,$day,$nday{$1},$config{'day.end'});
	}
	elsif($str =~ /^(今日|明日|明後日|明明後日|昨日|一昨日)([0-2][0-9]|[0-9])時/si){
		$h = sprintf("%02d",$2);
		$date =  &_FDATE($year,$mon,$day,$nday{$1},"${h}:00:00");
	}
	elsif($str =~ /^(今日|明日|明後日|明明後日|昨日|一昨日)/si){
		$date =  &_FDATE($year,$mon,$day,$nday{$1},$config{'day.start'});
	}
	elsif($str =~ /^(日|月|火|水|木|金|土)曜日(.*?)$/si){
		($sec,$min,$hour,$day,$mon,$year,$wday) = localtime($Time);$mon++;$year += 1900;
		$wday = 7 - ($wday - $wday{$1});
		if($wday < 0){$wday = $wday * -1;}
		$wday = $wday % 7;
		if($wday == 0){$wday=7;}
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($wday*60*60*24));$mon++;$year += 1900;
		if($2 =~ /^([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])時/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,0,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
		}
		else {
			$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$mon,$day);
		}
	}
	elsif($str =~ /^(日|月|火|水|木|金|土)曜(.*?)$/si){
		($sec,$min,$hour,$day,$mon,$year,$wday) = localtime($Time);$mon++;$year += 1900;
		$wday = 7 - ($wday - $wday{$1});
		if($wday < 0){$wday = $wday * -1;}
		$wday = $wday % 7;
		if($wday == 0){$wday=7;}
		($sec,$min,$hour,$day,$mon,$year) = localtime($Time+($wday*60*60*24));$mon++;$year += 1900;
		if($2 =~ /^([0-5][0-9]|[0-9])時([0-5][0-9]|[0-9])分/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])時/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,0,0);
		}
		elsif($2 =~ /^([0-5][0-9]|[0-9])\:([0-5][0-9]|[0-9])/si){
			$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$1,$2,0);
		}
		else {
			$date = sprintf("%04d-%02d-%02d $config{'day.start'}",$year,$mon,$day);
		}
	}
	else {
		$date = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$mon,$day,$hour,$min,$sec);
	}
	return $date;
}
sub _FDATE {
	my($y,$m,$d,$ajust,$datetime) = @_;
	my @month = (0,31,28,31,30,31,30,31,31,30,31,30,31);
	$month[2] += &_LEAP($y);
	if(($d + $ajust) < 1){
		$m--;
		if($m > 0){
			$d = $d+$ajust+$month[$mon];
		}
		else {
			$y--;
			$mon = 12;
			$d = $d+$ajust+$month[$mon];
		}
	}
	elsif(($d + $ajust) > $month[$m]){
		$m++;
		if($m > 12){
			$y++;
			$d = ($d + $ajust) - $month[$m-1];
			$m = 1;
		}
		else {
			$d = ($d + $ajust) - $month[$m-1];
		}
	}
	else {
		$d = $d + $ajust;
	}
	return sprintf("%04d-%02d-%02d ${datetime}",$y,$m,$d);
}
sub _LEAP {
	my($y) = @_;
	my $d = 0;
	if($y % 100 == 0 || $y % 4 != 0){
		if($y % 400 != 0){
			$d = 0;
		}
		else{
			$d = 1;
		}
	}
	elsif($y % 4 == 0){
		$d = 1;
	}
	else{
		$d = 1;
	}
	return $d;
}

1;
my $ver = '3.2.0 beta / 2020-01-21';
sub main {
	$template = "index.tpl";
	&_COOKIE;
	&_GET;
	if($_GET{'bin'}){
		&_POSTBIN;
	}
	else {
		&_POST;
	}
	&_LANG;
	if(&_ERROR < $config{'error.limit'}){
		if(-f $config{'file.key'}){
			&_REQUIRE($config{'file.key'});
			if($_GET{'key'} eq $config{'keycode'}){
				if(-f "$config{'dir.data'}demo.cgi"){
					$_VAL{'demo'} = "<div id=\"demo\">$_LANG{'demoText'}</div>";
				}
				if($_GET{'type'} eq 'ics'){
					$_GET{'app'} = 'ics';
				}
				elsif(-f "$config{'dir.session'}$_COOKIE{'session'}.cgi"){
					&_REQUIRE("$config{'dir.session'}$_COOKIE{'session'}.cgi");
					$template = "app.tpl";
					## Login
					if(!$_GET{'app'}){
						$_GET{'app'} = 'main';
					}
				}
				else {
					$_GET{'app'} = 'login';
				}
			}
			else {
				$_RESULT{'404'} = 1;
			}
		}
		else {
			$_GET{'app'} = 'install';
		}
	}
	else {
		$_RESULT{'403'} = 1;
	}
	&_REQUIRE("./inc/apps/$_GET{'app'}.cgi");
	if($template){
		$_RESULT{'html'} = &_LOAD($template);
	}
}
sub _LANG {
	if(-f "./inc/lang/$_GETS{'lang'}.cgi"){
		$_COOKIE{'lang'} = $_GETS{'lang'};
		&_REQUIRE("./inc/lang/$_GETS{'lang'}.cgi");
	}
	elsif(-f "./inc/lang/$_COOKIE{'lang'}.cgi"){
		&_REQUIRE("./inc/lang/$_COOKIE{'lang'}.cgi");
	}
	else {
		$_COOKIE{'lang'} = '';
		&_REQUIRE("./inc/lang/$config{'lang'}.cgi");
	}
	$_LANG{'ver'} = $ver;
}
sub _REQUIRE {
	my($path) = @_;
	if(-f $path){
		require $path;
	}
}
sub _LIB {
	my($path) = @_;
	if(-f "./inc/lib/_${path}.cgi"){
		require "./inc/lib/_${path}.cgi";
	}
}
sub _POST {
	use CGI;
	my $q = new CGI;
	my @names = $q->param;
	if($ENV{'CONTENT_LENGTH'}){
		$_POSTED = 1;
		for(my $cnt=0;$cnt<@names;$cnt++){
			my $name = $names[$cnt];
			my $value = "";
			if($name ne $null){
				my @list = $q->param($name);
				if(@list > 0){
					@list = sort { $a <=> $b } @list;
					$value = join("\n",@list);
				}
				else {
					$value = $q->param($name);
				}
				$_POST{$name} = &_SANITIZING($value);
				if($q->upload($name)){
					my @fH = $q->upload($name);
					@fH = sort { $a <=> $b } @fH;
					for(my $i=0;$i<@fH;$i++){
						my @filenames = split(/\\/,$fH[$i]);
						my $filename = $filenames[-1];
						my @filetypes = split /\./,$filename;
						$_BINTYPE{"${name}_${i}"} = lc $filetypes[-1];
						if($_BINTYPE{"${name}_${i}"} =~ /^jpeg$/ig){
							$_BINTYPE{"${name}_${i}"} = 'jpg';
						}
						$_BINNAME{"${name}_${i}"} = $filename;
						$_BINQTY{$name}++;
						while(read($fH[$i], $buffer, 1024)){
							$_BIN{"${name}_${i}"} .= $buffer;
						}
						$_BINSIZE{"${name}_${i}"} = (length $_BIN{"${name}_${i}"});
						$_BINSIZE{$name} += (length $_BIN{"${name}_${i}"});
					}
				}
			}
		}
	}
}
sub _POSTBIN {
	binmode STDIN;
	read(STDIN, $_BIN, $ENV{'CONTENT_LENGTH'});
}
sub _BINSAVE {
	my($path,$str) = @_;
	chmod 0777, $path;
	flock(FH, LOCK_EX);
		open(FH,">${path}");
			binmode (FH);
			print FH $str;
		close(FH);
	flock(FH, LOCK_NB);
	chmod 0644, $path;
}
sub _IMAGE_SIZE {
	my($path) = @_;
	my ($t, $m, $c, $l, $W, $H);
	if($path =~ /\.jpg/si){
		open(IMG, $path) || return (0,0);
			binmode IMG;
			read(IMG, $t, 2);
			while(1){
				read(IMG, $t, 4);
				($m, $c, $l) = unpack("a a n", $t);
				if($m ne "\xFF") {
					$W = $H = 0;
					last;
				}
				elsif((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
					read(IMG, $t, 5);
					($H, $W) = unpack("xnn", $t);
					last;
				}
				else {
					read(IMG, $t, ($l - 2));
				}
			}
		close(IMG);
	}
	elsif($path =~ /\.gif/si){
		my $data;
		open(IMG,$path) || return (0,0);
			binmode(IMG);
			sysread(IMG,$data,10);
		close(IMG);
		if($data =~ /^GIF/){
			$data = substr($data,-4);
		}
		$W = unpack("v",substr($data,0,2));
		$H = unpack("v",substr($data,2,2));
	}
	elsif($path =~ /\.png/si){
		my $data;
		open(IMG, $path) || return (0,0);
			binmode(IMG);
			read(IMG, $data, 24);
		close(IMG);
		$W = unpack("N", substr($data, 16, 20));
		$H = unpack("N", substr($data, 20, 24));
	}
	return ($W, $H);
}
sub _HOST {
	my @addr = split(/\./,$ENV{'REMOTE_ADDR'});
	my $addr = pack("C4", $addr[0], $addr[1], $addr[2], $addr[3]);
	my($name, $aliases, $addrtype, $length, @addrs) = gethostbyaddr($addr, 2);
	return $name;
}
sub _GET {
	if($ENV{'QUERY_STRING'}){
		$buffer = $ENV{'QUERY_STRING'};
		@pairs = split(/&/, $buffer);
		foreach $pair (@pairs) {
			($name, $value) = split(/=/, $pair);
			$name =~ tr/+/ /;
			$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			$value =~ tr/+/ /;
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			$value =~ s/_%%//ig;
			$value =~ s/%%_//ig;
			if($_GET{$name} eq $null){
				$_GET{$name} = $value;
			}
			else {
				$_GET{$name} .= "\n${value}";
			}
			$_GETS{$name} = &_SECURE_STRING($_GET{$name});
		}
		$_GET{'app'} = &_SECURE_STRING($_GET{'app'});
	}
}
sub _PASSCODE {
	my($digit) = @_;
	my $passcode;
	my @str = split(//,"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-");
	my $num = @str;
	for(my $i=0;$i<$digit;$i++){
		$passcode .= $str[int(rand() * $num)];
	}
	return $passcode;
}
sub _SECURE_STRING {
	my($str) = @_;
	my @str = ("\r","\n","\t","\"","\'",'/','|');
	for(my $i=0;$i<@str;$i++){
		$str =~ s/${str[$i]}//ig;
	}
	$str =~ s/\.//ig;
	return $str;
}
sub _SAVE {
	my($path,$str) = @_;
	chmod 0777, $path;
	if(-f $path){
		open(FH,"+< ${path}");
			flock(FH,2);
			seek(FH,0,0);
			print FH $str;
			truncate(FH,tell(FH));
		close(FH);
	}
	else {
		open(FH,">${path}");
			print FH $str;
		close(FH);
	}
	chmod 0644, $path;
}
sub _COUNTUP {
	my($path) = @_;
	chmod 0777, $path;
	open(FH,">>${path}");
		print FH '0';
	close(FH);
	chmod 0644, $path;
}
sub _ADDSAVE {
	my($path,$str) = @_;
	chmod 0777, $path;
	open(FH,">>${path}");
		print FH "${str}\n";
	close(FH);
	chmod 0644, $path;
}
sub _LOAD {
	my($path) = @_;
	my @loader = ();
	flock(FH, LOCK_EX);
		open(FH,$path);
			@loader = <FH>;
		close(FH);
	flock(FH, LOCK_NB);
	return join('',@loader);
}
sub _DB {
	my($path) = @_;
	my $loader = &_LOAD($path);
	$loader =~ s/\r//ig;
	return split(/\n/,$loader);
}
sub _RECORD {
	my($path,$id) = @_;
	my @loader = &_DB($path);
	return split(/\t/,(grep(/^${id}\t/,@loader))[0]);
}
sub _SNIPPET {
	my($str,$qty) = @_;
	$str =~ s/<.*?>//ig;
	if((length $str) > $qty){
		$str = substr($str, 0,$qty);
		$str =~ s/[\xC0-\xFD]$//;
		$str =~ s/[\xE0-\xFD][\x80-\xBF]$//;
		$str .= "...";
	}
	return $str;
}
sub _CM {
	my($num) = @_;
	1 while $num =~ s/(.*\d)(\d\d\d)/$1,$2/;
	return $num;
}
sub _LIST {
	my($str) = @_;
	return split(/<br>/,$str);
}
sub _ERRCLA {
	my $path = "$config{'dir.errors'}$ENV{'REMOTE_ADDR'}.cgi";
	if(-f $path){
		unlink $path;
	}
}
sub _ERROR {
	my $path = "$config{'dir.errors'}$ENV{'REMOTE_ADDR'}.cgi";
	if(-f $path){
		if(time < ((stat $path)[9]+$config{'error.time'})){
			my $size = -s $path;
			return $size / 2;
		}
		else {
			unlink $path;
			return 0;
		}
	}
	else {
		return 0;
	}
}
sub _RESULT {
	if($_RESULT{'404'}){
		$_VAL{'title'} = "_%%404%%_";
		$_VAL{'content'} = '_%%404text%%_';
		my @error = (time,$ENV{'REMOTE_ADDR'},&_HOST,&_SANITIZING($ENV{'HTTP_USER_AGENT'}));
		&_ADDSAVE($config{'file.error'},join("\t",@error));
		&_COUNTUP("$config{'dir.errors'}$ENV{'REMOTE_ADDR'}.cgi");
		print "Status: 404 Not Found\n";
		print "Content-type: text/html;charset=UTF-8\n\n";
		print &_VAL($_RESULT{'html'});
	}
	elsif($_RESULT{'403'}){
		$_VAL{'title'} = "_%%403%%_";
		$_VAL{'content'} = '_%%403text%%_';
		my @error = (time,$ENV{'REMOTE_ADDR'},&_HOST,&_SANITIZING($ENV{'HTTP_USER_AGENT'}));
		&_ADDSAVE($config{'file.error'},join("\t",@error));
		&_COUNTUP("$config{'dir.errors'}$ENV{'REMOTE_ADDR'}.cgi");
		print "Status: 403 Not Found\n";
		print "Content-type: text/html;charset=UTF-8\n\n";
		print &_VAL($_RESULT{'html'});
	}
	elsif($_RESULT{'ics'}){
		print "Content-type: text/calendar;charset=UTF-8\n\n";
		print $_RESULT{'ics'};
	}
	elsif($_RESULT{'text'}){
		&_ERRCLA();
		print "Content-type: plain/text;charset=UTF-8\n\n";
		print $_RESULT{'text'};
	}
	elsif($_RESULT{'json'}){
		&_ERRCLA();
		print "Content-type: text/json;charset=UTF-8\n";
		&_SET_COOKIE;
		print $_RESULT{'json'};
	}
	elsif($_RESULT{'downloadpath'} || $_RESULT{'download'}){
		&_ERRCLA();
		my $filename = &encodeURI($_RESULT{'filename'});
		print "Pragma: no-cache\n";
		print "Cache-Control: no-cache\n";
		print "Content-type: application/octet-stream;\n";
		print "Content-Disposition: attachment; filename=\"$_RESULT{'filename'}\"; filename*=UTF-8''${filename}\n";
		&_SET_COOKIE;
		if($_RESULT{'downloadpath'}){
			open(IN,$_RESULT{'downloadpath'});
				binmode(IN);
				print <IN>;
			close(IN);
		}
		else {
			print $_RESULT{'bom'};
			print $_RESULT{'download'};
		}
	}
	elsif($_RESULT{'redirect'}){
		&_ERRCLA();
		print "Location: $_RESULT{'redirect'}\n";
		&_SET_COOKIE;
	}
	else {
		&_ERRCLA();
		print "Content-type: text/html;charset=UTF-8\n";
		&_SET_COOKIE;
		print &_VAL($_RESULT{'html'});
	}
}
sub _VAL {
	my($str) = @_;
	foreach $key (keys(%_VAL)){
		$str =~ s/_%%$key%%_/$_VAL{$key}/ig;
	}
	foreach $key (keys(%_LANG)){
		$str =~ s/_%%$key%%_/$_LANG{$key}/ig;
	}
	$str =~ s/_%%.*?%%_//ig;
	return $str;
}
sub _TIMESTR {
	my($str) = @_;
	if($str < 60){
		return sprintf("00:00:%02d",$str);
	}
	elsif($str < 3600){
		return sprintf("00:%02d:%02d",($str/60),($str%60));
	}
	elsif($str < 86400){
		return sprintf("%02d:%02d:%02d",($str/3600),(($str%3600)/60),($str%60));
	}
	else {
		return sprintf("%03d day %02d:%02d:%02d",$str/86400,(($str%86400)/3600),(($str%3600)/60),($str%60));
	}
}
sub _HASH {
	my($str) = @_;
	use Digest::MD5;
	$md5 = Digest::MD5->new;
	$str = $md5->add($str)->b64digest;
	$str =~ s/\//\-/ig;
	$str =~ s/\+/\_/ig;
	return $str;
}
sub _FILENAME {
	my($str) = @_;
	$str =~ s/</&lt;/ig;
	$str =~ s/>/&gt;/ig;
	$str =~ s/\'/&rsquo;/ig;
	$str =~ s/\"/&quot;/ig;
	$str =~ s/\t/&nbsp;&nbsp;/ig;
	$str =~ s/\r\n/\n/ig;
	$str =~ s/\r/\n/ig;
	$str =~ s/\n//ig;
	return $str;
}
sub _SANITIZING {
	my($str) = @_;
	$str =~ s/\&/&amp;/ig;
	$str =~ s/\\/&yen;/ig;
	$str =~ s/</&lt;/ig;
	$str =~ s/>/&gt;/ig;
	$str =~ s/\'/&rsquo;/ig;
	$str =~ s/\"/&quot;/ig;
	$str =~ s/\t/&nbsp;&nbsp;/ig;
	$str =~ s/\r\n/\n/ig;
	$str =~ s/\r/\n/ig;
	$str =~ s/\n/<br>/ig;
	return $str;
}
sub _UNSANITIZING {
	my($str) = @_;
	$str =~ s/&amp;/\&/ig;
	$str =~ s/&lt;/</ig;
	$str =~ s/&gt;/>/ig;
	$str =~ s/&rsquo;/\'/ig;
	$str =~ s/&quot;/\"/ig;
	$str =~ s/&nbsp;/ /ig;
	$str =~ s/<br>/\n/ig;
	return $str;
}
sub decodeURI {
	my($str) = @_;
	$str =~ tr/+/ /;
	$str =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	return $str;
}
sub encodeURI {
	my($str) = @_;
	$str =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$str =~ tr/ /+/;
	return $str;
}
sub _SESSION {
	my @ip = split(/\./,$ENV{'REMOTE_ADDR'});
	my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
	my $path = 'index.cgi';
	my $session = "";
	while(-f $path){
		$ses1 = &_CRYPT((sprintf("%04d%02d%02d",$year+1900,$mon+1,$day)));
		$ses2 = &_CRYPT((sprintf("%02d%02d%02d",$hour,$min,$sec)));
		$ses3 = &_CRYPT("${ip[0]}.${ip[1]}");
		$ses4 = &_CRYPT("${ip[2]}.${ip[3]}");
		$session = "${ses1}${ses2}${ses3}${ses4}";
		my $dir = lc (substr($session,0,1));
		$path = "$config{'dir.session'}/${session}.cgi";
	}
	return $session;
}
sub _ID {
	my $id = time;
	my @salt = ('a'..'z','A'..'Z','0'..'9','-','_');
	my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
	return "${id}${salt}";
}
sub _CRYPT {
	my($str) = @_;
	my @salt = ('a'..'z','A'..'Z','0'..'9','-','_');
	my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
	$str = crypt($str,$salt);
	$str =~ s/\./_/ig;
	$str =~ s/\//-/ig;
	$str =~ s/\%/-/ig;
	return $str;
}
sub _COOKIE_PATH {
	my @path = split(/\//,$ENV{'SCRIPT_NAME'});
	$path[-1] = "";
	return join('/',@path);
}
sub _COOKIE {
	if($ENV{'HTTP_COOKIE'} =~ /$config{'prefix'}=\|(.*?)\|/si){
		my $cookie = $1;
		my @cookies = split(/\&/,$cookie);
		for(my $cnt=0;$cnt<@cookies;$cnt++){
			my($name, $value) = split(/=/,$cookies[$cnt]);
			$_COOKIE{$name} = &decodeURI($value);
			$_COOKIE{$name} = &_SECURE_STRING($_COOKIE{$name});
		}
	}
}
sub _SET_COOKIE {
	my @cookie = ();
	foreach $key(keys(%_COOKIE)){
		if($_COOKIE{$key} ne $null){
			$_COOKIE{$key} =~ s/\|//ig;
			push @cookie,"${key}=" . &encodeURI($_COOKIE{$key});
		}
	}
	my $exp = &_EXPIRES(30);
	print "Set-Cookie: $config{'prefix'}=\|" . join("&",@cookie) . "\|; path=" . &_COOKIE_PATH . "; expires=${exp}\n\n";
}
sub _EXPIRES {
	my($exp) = @_;
	my($gmt, @t, @m, @w);
	@t = gmtime(time + $exp*60*60*24);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	return sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);
}
sub _ICAL {
	my(@db) = @_;
	my $ics = <<"	__HTML__";
		BEGIN:VCALENDAR
		METHOD:PUBLISH
		VERSION:2.0
		X-WR-CALNAME:WEBPAD3
		PRODID:-//SYNCKGRAPHICA.//WEBPAD3//EN
		X-APPLE-CALENDAR-COLOR:#999999
		X-WR-TIMEZONE:Asia/Tokyo
		CALSCALE:GREGORIAN
		<!--main-->
		BEGIN:VTIMEZONE
		TZID:Asia/Tokyo
		BEGIN:STANDARD
		DTSTART:19700101T000000
		TZOFFSETFROM:+0900
		TZOFFSETTO:+0900
		END:STANDARD
		END:VTIMEZONE
		END:VCALENDAR
	__HTML__
	my @todo = ();
	for(my $i=0;$i<@db;$i++){
		my @r = split(/\t/,$db[$i]);
		if($r[6] && $r[5] eq $null){
			my $summary = $r[9];
			my $uid = $r[0];
			my $description = $r[9];
			my $enter = $r[4] || $r[3];
			$enter =~ s/\-//ig;
			$enter =~ s/\://ig;
			my($date,$time) = split(/ /,$enter);
			my $endtime = sprintf("%06d",($time + 3000));
			
			## LOCATION
			## http://www.asahi-net.or.jp/~CI5M-NMR/iCal/ref.html
			
			my $parts = <<"			__HTML__";
				BEGIN:VEVENT
				ORGANIZER:${r[2]}
				LOCATION:${r[8]}
				UID:${uid}
				DTSTART;TZID=Asia/Tokyo:${date}T${time}
				SUMMARY:${summary}
				BEGIN:VALARM
				TRIGGER:-PT15M
				ATTACH;VALUE=URI:Basso
				ACTION:AUDIO
				END:VALARM
				END:VEVENT
			__HTML__
			push @todo,$parts;
		}
	}
	my $todo = join("",@todo);
	$ics =~ s/<!--main-->/${todo}/ig;
	$ics =~ s/\t//ig;
	$ics =~ s/\n\n/\n/ig;
	return $ics;
}
1;
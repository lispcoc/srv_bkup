sub _MAIL {
	my($to,$from,$name,$bcc,$subject,$body) = @_;
	if($config{'smtp.server'}){
		&_SMTP($to,$from,$name,$bcc,$subject,$body);
	}
	else {
		&_SENDMAIL($to,$from,$name,$bcc,$subject,$body);
	}
}
sub _MIME {
	my($str,$charset) = @_;
	$str = "=?${charset}?B?" . encode_base64($str) . '?=';
	$str =~ s/\r//ig;
	$str =~ s/\n//ig;
	return "${str}\n";
}
sub _SENDMAIL {
	my($to,$from,$name,$bcc,$subject,$body) = @_;
	open(MAIL,"| $config{'sendmail'} -f ${from} -t");
		print MAIL &_MAILHEADER($to,$from,$name,$bcc,$subject,$body);
	close(MAIL);
}
sub _SMTP {
	my($to,$from,$name,$bcc,$subject,$body) = @_;
	use Net::SMTP;
	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my @month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	my $date = sprintf("%s, %d %s %04d %02d:%02d:%02d +0900 (JST)",$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
	my $SMTP;
	if($config{'smtp.tls'}){
		use lib "inc/lib";
		use Net::SMTP::TLS;
		$SMTP = Net::SMTP::TLS->new($config{'smtp.server'},Port=>$config{'smtp.port'},User=>$config{'smtp.user'},Password=>$config{'smtp.passwd'});
	}
	elsif($config{'smtp.port'}){
		$SMTP = Net::SMTP->new($config{'smtp.server'}, Timeout=>20, Hello=>$config{'smtp.server'},Port=>$config{'smtp.port'});
	}
	else {
		$SMTP = Net::SMTP->new($config{'smtp.server'}, Timeout=>20, Hello=>$config{'smtp.server'});
	}
	
	if($SMTP){
		if($config{'smtp.user'} ne $null && $config{'smtp.passwd'} ne $null && !$config{'smtp.tls'}){
			$SMTP->auth($config{'smtp.user'},$config{'smtp.passwd'});
		}
		$SMTP->mail($from);
		$SMTP->to($to);
		$SMTP->data();
		$SMTP->datasend("Date: ${date}\n");
		$SMTP->datasend(&_MAILHEADER($to,$from,$name,$bcc,$subject,$body));
		$SMTP->dataend();
		$SMTP->quit;
	}
}
sub _MAILBODY {
	my($body) = @_;
	return encode_base64($body);
}
sub _MAILHEADER {
	my($to,$from,$name,$bcc,$subject,$body) = @_;
	my $str;
	use MIME::Base64;
	## boundary
	$boundary = "------------boundary_" . time . "_" . $$;
	$subject = &_MIME($subject,'UTF-8');
	my $return = $from;
	$from = &_MIME("${name}",'UTF-8') . "<${from}>";
	$body = encode_base64($body);
	$subject =~ s/\r//ig;
	$subject =~ s/\n//ig;
	$from =~ s/\r//ig;
	$from =~ s/\n//ig;
	$str = "Return-Path: <${return}>\n";
	$str .= "Subject: ${subject}\n";
	$str .= "From: ${from}\n";
	$str .= "Content-Type: multipart/alternative; boundary=\"${boundary}\"\n";
	$str .= "To: ${to}\n";
	if($bcc){
		$str .= "Bcc: ${bcc}\n";
	}
	$str .= "MIME-Version: 1.0\n\n";
	$str .= "--${boundary}\n";
	$str .= "Content-Type: text/plain; charset=\"UTF-8\"\n";
	$str .= "Content-Transfer-Encoding: Base64\n";
	$str .= "Content-Disposition: inline\n\n";
	$str .= "${body}\n";
	$str .= "--${boundary}--\n";
	return $str;
}
1;
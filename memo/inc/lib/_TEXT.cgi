sub _TEXT {
	my($str) = @_;
	
	## initialize
	$str = "<br>${str}<br>";
	while($str =~ /<br><br><br>/si){
		$str =~ s/<br><br><br>/<br><br>/ig;
	}
	$str =~ s/　/ /ig;
	while($str =~ /  /si){
		$str =~ s/  / /ig;
	}
	$str =~ s/<br><br>$/<br>/ig;
	$str =~ s/^<br><br>/<br>/ig;
	$str =~ s/<br><br>/<\/p><p>/ig;
	$str = "<p>${str}</p>";
	
	## list
	$str =~ s/>・(.*?)</><li>$1<\/li></g;
	$str =~ s/>\*(.*?)</><li>$1<\/li></g;
	$str =~ s/<p><li>/<ul><li>/g;
	$str =~ s/<br><li>/<\/p><ul><li>/g;
	$str =~ s/<\/li><br \/>/<\/li>/g;
	$str =~ s/<\/li><\/p>/<\/li><\/ul>/g;
	$str =~ s/<\/li><br>/<\/li>/g;
	$str =~ s/<\/li>/<\/li><\/ul>/g;
	$str =~ s/<\/ul><\/ul>/<\/ul>/g;
	$str =~ s/<\/ul><ul>//g;
	$str =~ s/<\/ul><li>/<li>/g;
	$str =~ s/<\/ul><ul>//g;
	$str =~ s/<\/ul><\/p>/<\/ul>/g;
	
	## https://youtu.be/YOceYWm0UKE
	## <iframe width="560" height="315" src="https://www.youtube.com/embed/YOceYWm0UKE?rel=0" frameborder="0" allowfullscreen></iframe>
	$str =~ s/>http\:\/\/www\.youtube\.com\/watch\?v\=(.*?)</><\/p><div class=\"youtube\"><iframe src=\"https\:\/\/www\.youtube\.com\/embed\/${1}\?rel=0\" frameborder=\"0\" allowfullscreen><\/iframe><\/div><p></ig;
	$str =~ s/>https\:\/\/www\.youtube\.com\/watch\?v\=(.*?)</><\/p><div class=\"youtube\"><iframe src=\"https\:\/\/www\.youtube\.com\/embed\/${1}\?rel=0\" frameborder=\"0\" allowfullscreen><\/iframe><\/div><p></ig;
	$str =~ s/>https\:\/\/youtu\.be\/(.*?)</><\/p><div class=\"youtube\"><iframe src=\"https\:\/\/www\.youtube\.com\/embed\/${1}\?rel=0\" frameborder=\"0\" allowfullscreen><\/iframe><\/div><p></ig;
	
	## URL
	$str =~ s/>(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)</><a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a></ig;
	
	$str =~ s/>--</><\/p><hr><p></g;
	$str =~ s/>-</><\/p><hr><p></g;
	$str =~ s/>----(.*?)</><\/p><h6>$1<\/h6><p></g;
	$str =~ s/>---(.*?)</><\/p><h5>$1<\/h5><p></g;
	$str =~ s/>--(.*?)</><\/p><h4>$1<\/h4><p></g;
	$str =~ s/>-(.*?)</><\/p><h3>$1<\/h3><p></g;
	
	$str =~ s/<h3>/<section><h3>/ig;
	my @text = split(/<section>/,$str);
	if(@text > 0){
		for(my $i=0;$i<@text;$i++){
			$text[$i] = "<section>${text[$i]}</section>";
		}
		$str = join("<section>",@text);
		$str =~ s/^<\/section>//ig;
		$str =~ s/<section>$//ig;
		$str =~ s/<section><section>/<section>/ig;
		$str =~ s/<section><\/section>//ig;
	}
	else {
		$str = "<section>${str}</section>";
	}
	
	$str =~ s/>&gt;(.*?)</><\/p><blockquote>$1<\/blockquote><p></ig;
	
	$str =~ s/<div/<\/p><div/ig;
	$str =~ s/<\/div>/<\/div><p>/ig;
	$str =~ s/<p><br>/<p>/ig;
	$str =~ s/<br><\/p>/<\/p>/ig;
	$str =~ s/<\/p><\/p>/<\/p>/ig;
	$str =~ s/<p><\/p>//ig;
	$str =~ s/<p><\/section>/<\/section>/ig;
	$str =~ s/<section><\/section>//ig;
	
	
	return $str;
}
sub _OPTIMIZATION {
	my($str) = @_;
	my @a = ('ｶﾞ','ｷﾞ','ｸﾞ','ｹﾞ','ｺﾞ','ｻﾞ','ｼﾞ','ｽﾞ','ｾﾞ','ｿﾞ','ﾀﾞ','ﾁﾞ','ﾂﾞ','ﾃﾞ','ﾄﾞ','ﾊﾞ','ﾋﾞ','ﾌﾞ','ﾍﾞ','ﾎﾞ','ﾊﾟ','ﾋﾟ','ﾌﾟ','ﾍﾟ','ﾎﾟ','ｦ','ｧ','ｨ','ｩ','ｪ','ｫ','ｬ','ｭ','ｮ','ｯ','ｰ','ｱ','ｲ','ｳ','ｴ','ｵ','ｶ','ｷ','ｸ','ｹ','ｺ','ｻ','ｼ','ｽ','ｾ','ｿ','ﾀ','ﾁ','ﾂ','ﾃ','ﾄ','ﾅ','ﾆ','ﾇ','ﾈ','ﾉ','ﾊ','ﾋ','ﾌ','ﾍ','ﾎ','ﾏ','ﾐ','ﾑ','ﾒ','ﾓ','ﾔ','ﾕ','ﾖ','ﾗ','ﾘ','ﾙ','ﾚ','ﾛ','ﾜ','ﾝ','Ａ','Ｂ','Ｃ','Ｄ','Ｅ','Ｆ','Ｇ','Ｈ','Ｉ','Ｊ','Ｋ','Ｌ','Ｍ','Ｎ','Ｏ','Ｐ','Ｑ','Ｒ','Ｓ','Ｔ','Ｕ','Ｖ','Ｗ','Ｘ','Ｙ','Ｚ','ａ','ｂ','ｃ','ｄ','ｅ','ｆ','ｇ','ｈ','ｉ','ｊ','ｋ','ｌ','ｍ','ｎ','ｏ','ｐ','ｑ','ｒ','ｓ','ｔ','ｕ','ｖ','ｗ','ｘ','ｙ','ｚ','＠','０','１','２','３','４','５','６','７','８','９','．','－','〜','｢','｣');
	my @b = ('ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ','ヲ','ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ','ッ','ー','ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ン','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','@','0','1','2','3','4','5','6','7','8','9','.','-','～','「','」');
	for(my $i=0;$i<@a;$i++){
		$str =~ s/$a[$i]/$b[$i]/ig;
	}
	return $str;
}
1;
################ 画像アップロード ################
use strict;
use warnings;
use utf8;

my $max_size = ( $set::image_maxsize ? $set::image_maxsize : 1024 * 512 );
my $max_width  = 300;
my $max_height = 500;

my $imgdir = $set::imgdir;
use Image::Magick;

my $upload_file = param('upload_file');
my $upload_thum = param('upload_thum');
my $upload_back = param('upload_back');

our %pc = %main::pc;

# ファイルの削除
if (($upload_file || $pc{'del_file'}) && !$pc{'ext_s'}) {
	unlink "$imgdir$pc{'file'}_.$pc{'ext_l'}";
}
if ($upload_file || $pc{'del_file'}) {
	unlink "$imgdir$pc{'file'}.$pc{'ext_l'}" ,"$imgdir$pc{'file'}__.$pc{'ext_l'}";
	$pc{'ext_l'} = "";
}
if (($upload_thum || $pc{'del_thum'}) && $pc{'ext_s'}) {
	unlink "$imgdir$pc{'file'}_.$pc{'ext_s'}","$imgdir$pc{'file'}___.$pc{'ext_s'}"; $pc{'ext_s'} = "";
	my $img = Image::Magick->new;
	$img->Read("$imgdir$pc{'file'}.$pc{'ext_l'}");
	my($width,$filesize) = $img->Get('width','filesize');
	if ($width > $max_width) {
		$img->Resize(geometry=>$max_width);
		$img->Set(quality=>95);
		$img->Write(filename=>"$imgdir$pc{'file'}_.$pc{'ext_l'}");
	}
}
if ($upload_back || $pc{'del_back'}) {
	unlink "$imgdir$pc{'file'}_back.$pc{'ext_b'}" ,"$imgdir$pc{'file'}_back_.$pc{'ext_b'}";
	$pc{'ext_b'} = "";
}

foreach ('upload_file','upload_thum','upload_back'){
	# ファイル名の取得
	my $filename;
	if   ($_ eq 'upload_file'){ $filename = $upload_file; }
	elsif($_ eq 'upload_thum'){ $filename = $upload_thum; }
	elsif($_ eq 'upload_back'){ $filename = $upload_back; }
	if($filename) {
		# MIMEタイプの取得
		my $type = uploadInfo($filename)->{'Content-Type'};
		
		# ファイルの受け取り
		my $file; my $buffer;
		while(my $bytesread = read($filename, $buffer, 2048)) {
			$file .= $buffer;
		}

		my $flg_l;
		if (length($file) <= $max_size){ $flg_l=1; }

		# ファイル判別
		my $ext; my $flg_t;
		if    ($type eq "image/gif")   { $ext ="gif"; $flg_t=1; } #GIF
		elsif ($type eq "image/jpeg")  { $ext ="jpg"; $flg_t=1; } #JPG
		elsif ($type eq "image/pjpeg") { $ext ="jpg"; $flg_t=1; } #JPG
		elsif ($type eq "image/png")   { $ext ="png"; $flg_t=1; } #PNG
		elsif ($type eq "image/x-png") { $ext ="png"; $flg_t=1; } #PNG

		# ファイルの保存
		if($flg_t && $flg_l) {
			if   ($_ eq 'upload_file'){
				open(IMG, "> $imgdir$pc{'file'}.${ext}");
				$pc{'ext_l'} = $ext;
			}
			elsif($_ eq 'upload_thum'){
				open(IMG, "> $imgdir$pc{'file'}_.${ext}");
				$pc{'ext_s'} = $ext;
			}
			elsif($_ eq 'upload_back'){
				open(IMG, "> $imgdir$pc{'file'}_back.${ext}");
				$pc{'ext_b'} = $ext;
			}
			binmode(IMG);
			print(IMG $file);
			close(IMG);
		}

		# サムネイルの生成
		if($_ eq 'upload_file'){
			my $img = Image::Magick->new;
			$img->Read("$imgdir$pc{'file'}.${ext}");
			my($width,$filesize) = $img->Get('width','filesize');
			if (!$upload_thum && !$pc{'ext_s'}) {
				if ($width > $max_width) {
					$img->Resize(geometry=>$max_width);
					$img->Set(quality=>98, 'sampling-factor'=>'1x1');
				}
				$img->Write(filename=>"$imgdir$pc{'file'}_.${ext}");
			}
			# ミニサムネ
			$img->Resize(geometry=>"50x50");
			$img->Set(quality=>95, 'sampling-factor'=>'1x1');
			$img->Write(filename=>"$imgdir$pc{'file'}__.${ext}");
		}
		if($_ eq 'upload_thum'){
			my $thu = Image::Magick->new;
			$thu->Read("$imgdir$pc{'file'}_.${ext}");
			my($width,$filesize) = $thu->Get('width','filesize');
			if ($width > $max_width) {
				$thu->Resize(geometry=>$max_width);
				$thu->Set(quality=>98, 'sampling-factor'=>'1x1');
				$thu->Write(filename=>"$imgdir$pc{'file'}_.${ext}");
			}
			# ミニサムネ
			$thu->Resize(geometry=>"50x50");
			$thu->Set(quality=>95, 'sampling-factor'=>'1x1');
			$thu->Write(filename=>"$imgdir$pc{'file'}___.${ext}");
		}
		if($_ eq 'upload_back'){
			my $img = Image::Magick->new;
			$img->Read("$imgdir$pc{'file'}_back.${ext}");
			my($width,$filesize) = $img->Get('width','filesize');
			# ミニサムネ
			$img->Resize(geometry=>"50x50");
			$img->Set(quality=>95, 'sampling-factor'=>'1x1');
			$img->Write(filename=>"$imgdir$pc{'file'}_back_.${ext}");
		}
	}
}

1;
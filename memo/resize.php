<?php
	ini_set('memory_limit', '256M');
	$key = str_replace('.', '', $_GET['key']);
	$key = str_replace('/', '', $key);
	$key = './data/tmp/' . $key . '.php';
	if(file_exists($key)){
		include $key;
		// $image,$type,$width,$thumbnail
		list($w, $h) = getimagesize($image);
		$nw = $width;
		$nh = $h * ($nw / $w);
		$out = imagecreatetruecolor($nw, $nh);
		if($type == 'jpg'){
			$in = imagecreatefromjpeg($image);
			ImageCopyResampled($out, $in, 0, 0, 0, 0, $nw, $nh, $w, $h);
			imagejpeg($out,$thumbnail, 100);
			echo("web.App.resize.callback(true);");
		}
		else if($type == 'gif'){
			$in = imagecreatefromgif($image);
			ImageCopyResampled($out, $in, 0, 0, 0, 0, $nw, $nh, $w, $h);
			imagegif($out,$thumbnail);
			echo("web.App.resize.callback(true);");
		}
		else if($type == 'png'){
			$in = imagecreatefrompng($image);
			ImageCopyResampled($out, $in, 0, 0, 0, 0, $nw, $nh, $w, $h);
			imagepng($out,$thumbnail);
			echo("web.App.resize.callback(true);");
		}
		else {
			echo("web.App.resize.callback(false);");
		}
		unlink($key);
	}
	else {
		header('Location: index.cgi');
	}
?>
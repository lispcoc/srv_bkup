<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<meta name="apple-touch-fullscreen" content="YES">
		<meta name="apple-mobile-web-app-capable" content="YES">
		<meta name="apple-mobile-web-app-status-bar-style" content="black">
		<meta name="robots" content="noindex,noarchive">
		<title>_%%title%%_ | _%%name%%_</title>
		<link rel="apple-touch-icon" href="inc/_images/logo-touch-icon.png">
		<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
		<link rel="stylesheet" href="inc/default.css" type="text/css">
		<script type="text/javascript" src="inc/default.js"></script>
	</head>
	<body>
		<header>
			<h1>_%%name%%_</h1>
			_%%nav%%_
		</header>
		<main>
			_%%content%%_
		</main>
		<footer>
			<p>
				_%%name%%_ _%%ver%%_
				<select onchange="langsw(this)">
					<option value="">_%%lang%%_</option>
					<option value="jp">_%%jp%%_</option>
					<option value="en">_%%en%%_</option>
				</select>
			</p>
		</footer>
		_%%form%%_
		_%%demo%%_
	</body>
</html>
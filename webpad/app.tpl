<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<meta name="apple-touch-fullscreen" content="YES">
		<meta name="apple-mobile-web-app-capable" content="YES">
		<meta name="apple-mobile-web-app-status-bar-style" content="black">
		<meta name="robots" content="noindex,noarchive">
		<title>_%%name%%_</title>
		<link rel="apple-touch-icon" href="inc/_images/logo-touch-icon.png?v2">
		<link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v2">
		<link rel="stylesheet" href="inc/app.css" type="text/css">
		<script type="text/javascript" src="inc/app.js"></script>
	</head>
	<body>
		<header>
			<h1>_%%name%%_<span>_%%ver%%_</span></h1>
			<form id="search">
				<div>
					<strong id="search_toggle"></strong>
					<input type="text" id="q" placeholder="_%%search%%_">
					<button type="button" id="search_clear"></button>
				</div>
			</form>
			<nav id="nav_main">
				<ul>
					<li><span id="nav_app_note">_%%app_note%%_</span></li>
					<li><span id="nav_app_logs">_%%app_log%%_</span></li>
					<li><span id="nav_app_file">_%%app_file%%_</span></li>
					<li><span id="nav_app_analyze">_%%app_dailytask%%_</span></li>
					<li><span id="nav_app_setting">_%%app_setting%%_</span></li>
					<li><span id="nav_app_logout">_%%logout%%_</span></li>
				</ul>
			</nav>
		</header>
		<main id="app">
			<nav id="nav_path"></nav>
			<div id="app_main">
				<div class="app_main" id="app_main_note">
					<nav id="nav_app_note" class="nav_apps">
						<ul>
							<li><span id="app_command_new" title="_%%command_n%%_">_%%nav_app_note_new%%_</span></li>
							<li><span id="app_command_save" title="_%%command_s%%_">_%%nav_app_note_save%%_</span></li>
							<li><span id="app_command_remove">_%%nav_app_note_remove%%_</span></li>
							<li><span id="app_command_todo">_%%nav_app_note_todo%%_</span></li>
							<li><span id="app_command_dl">_%%nav_app_note_download%%_</span></li>
							<li><span id="app_command_mail">_%%nav_app_note_mail%%_</span></li>
						</ul>
					</nav>
					<textarea id="app_note" spellcheck="false"></textarea>
					<nav id="nav_app_note_status" class="nav_apps">
						<ul>
							<li><span><label><input type="checkbox" id="app_note_public">_%%app_note_public%%_</label></span></li>
							<li><span>_%%app_note_cdate%%_<em id="app_note_cdate">-</em></span></li>
							<li><span>_%%app_note_udate%%_<em id="app_note_udate">-</em></span></li>
							<li><span>_%%app_note_worktime%%_<em id="app_note_worktime">-</em></span></li>
						</ul>
						<ol>
							<li><img src="inc/_images/pw.png" id="app_note_tool_pw"></li>
							<li><img src="inc/_images/sb.png" id="app_note_tool_sb"></li>
							<li><img src="inc/_images/li.png" id="app_note_tool_li"></li>
							<li><img src="inc/_images/lv.png" id="app_note_tool_lv"></li>
							<li><img src="inc/_images/sl.png" id="app_note_tool_sl"></li>
						</ol>
					</nav>
				</div>
				<div class="app_main" id="app_main_logs">
					<div id="app_main_logs_main">
						<div id="app_main_logs_calendar">
							<h3 id="app_main_logs_calendar_h"></h3>
							<table id="app_main_logs_calendar_wrap">
								<tr>
									<td valign="top"><span id="app_main_logs_calendar_prev">&lt;</span></td>
									<td><div id="app_main_logs_calendar_main"></div></td>
									<td valign="top"><span id="app_main_logs_calendar_next">&gt;</span></td>
								</tr>
							</table>
						</div>
						<div id="app_main_logs_todo"></div>
						<div id="app_main_logs_timeline"></div>
						<form id="app_main_logs_form">
							<input type="text" id="app_main_logs_input" placeholder="_%%app_logs_placeholder%%_">
						</form>
					</div>
				</div>
				<div class="app_main" id="app_main_analyze">
					<div id="app_main_analyze_main">
						<div class="app_main_analyze_section" id="app_main_analyze_table">
							<table class="daily">
								<tr>
									<th>&nbsp;</th>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td valign="bottom">
										<div class="barwrap">
											<div class="bar1"></div>
											<div class="bar2"></div>
											<div class="bar3"></div>
										</div>
									</td>
									<td colspan="2">Weekly</td>
									<td colspan="2">Sum</td>
								</tr>
								<tr>
									<th>Date</th>
									<td>25 Wed</td>
									<td>26 Thu</td>
									<td>27 Fri</td>
									<td class="w6">28 Sat</td>
									<td class="w0">29 Sun</td>
									<td>30 Mon</td>
									<td>31 Tue</td>
									<td>Total</td>
									<td>Avg</td>
									<td>Total</td>
									<td>Avg</td>
								</tr>
								<tr>
									<th class="text3">Total</th>
									<td><em class="up"><strong>25</strong><span>&#9654;</span>3.5%</em></td>
									<td><em class="down"><strong>21</strong><span>&#9654;</span>3.5%</em></td>
									<td>27</td>
									<td>28</td>
									<td>29</td>
									<td>30</td>
									<td>31</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
								</tr>
								<tr>
									<th class="text1">Task</th>
									<td>25</td>
									<td>26</td>
									<td>27</td>
									<td>28</td>
									<td>29</td>
									<td>30</td>
									<td>31</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
								</tr>
								<tr>
									<th class="text2">Mission</th>
									<td>25</td>
									<td>26</td>
									<td>27</td>
									<td>28</td>
									<td>29</td>
									<td>30</td>
									<td>31</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
									<td>1</td>
								</tr>
								
							</table>
						</div>
					</div>
				</div>
			</div>
		</main>
		<aside id="finder">
			<ul id="directories"></ul>
		</aside>
		<footer>
			<button id="audio_button" class="mute"></button>
			<select onchange="langsw(this)">
				<option value="">_%%lang%%_</option>
				<option value="jp">_%%jp%%_</option>
				<option value="en">_%%en%%_</option>
			</select>
		</footer>
		<form id="postform" method="post" target="shadowpost">
			<input type="hidden" name="form_id" id="form_id">
			<input type="hidden" name="form_parent" id="form_parent">
			<input type="hidden" name="form_worktime" id="form_worktime">
			<input type="hidden" name="form_text" id="form_text">
			<input type="hidden" name="form_public" id="form_public">
			<input type="hidden" name="form_todo" id="form_todo">
			<input type="file" name="form_file" id="form_file">
		</form>
		<iframe id="shadowpost" name="shadowpost"></iframe>
		_%%demo%%_
		_%%script%%_
		<iframe src="inc/_audio/500-milliseconds-of-silence.mp3" allow="autoplay" id="audio" style="display:none"></iframe>
	</body>
</html>
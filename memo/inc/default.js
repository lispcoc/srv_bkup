var web = {
	App: [],
	Env: [],
	GET: [],
	Extend: [],
	json: function(src){
		var script = document.createElement('script');
		script.async = false;
		script.type = 'text/javascript';
		script.src = src;
		script.charset = 'UTF-8';
		script.onerror = function(){
			web.json(src);
		};
		document.body.appendChild(script);
	},
	add: function(event,fn){
		var _ = web;
		if(!_.Extend[event]){
			_.Extend[event] = [];
		};
		_.Extend[event].push(fn);
	},
	get: function(){
		if(location.search){
			var g = (location.search.substring(1,location.search.length)).split('&');
			for(var i=0;i<g.length;i++){
				var get = [];
				get = g[i].split('=');
				web.GET[decodeURI(get[0])] = decodeURI(get[1]);
			};
		};
	},
	run: function(event){
		var _ = web;
		if(_.Extend[event]){
			for(var i=0;i<_.Extend[event].length;i++){
				_.Extend[event][i]();
			};
		};
	},
	initialize: function(){
		var _ = web;
		_.get();
		_.addEvent(window,'load',function(){
			_.environment(1);
			_.addEvent(window,'scroll',function(){
				_.environment();
				web.run('scroll');
			});
			_.addEvent(window,'resize',function(){
				_.environment(1);
				web.run('resize');
			});
			_.addEvent(window,'gestureend',function(){
				_.environment(1);
				web.run('resize');
			});
			web.run('ready');
			web.run('resize');
		});
	},
	environment: function(resize){
		var _ = web;
		var bd = document.body,el = document.documentElement;
		if(resize){
			_.Env['canvas'] = {
				width: window.innerWidth || document.documentElement.clientWidth,
				height: window.innerHeight || document.documentElement.clientHeight
			};
			_.Env['contents'] = {
				width: el.scrollWidth || bd.scrollWidth,
				height: el.scrollHeight || bd.scrollHeight
			};
		};
		_.Env['scroll'] = {
			top: el.scrollTop || bd.scrollTop,
			left: el.scrollLeft || bd.scrollLeft
		};
		_.Env['scroll']['horizon'] = _.Env['scroll']['left'] / (_.Env['contents']['width']-_.Env['canvas']['width']);
		_.Env['scroll']['vertical'] = _.Env['scroll']['top'] / (_.Env['contents']['height']-_.Env['canvas']['height']);
	},
	$: function(obj){
		if(typeof obj == 'string'){
			if(document.getElementById(obj)){
				return document.getElementById(obj);
			}
			else {
				return null;
			};
		}
		else {
			return obj;
		};
	},
	byClassName: function(parentNode,className){
		var _ = web;
		try {
			return parentNode.getElementsByClassName(className);
		}
		catch(e){
			var classNames = [];
			var elements = parentNode.getElementsByTagName('*');
			for(var i=0;i<elements.length;i++){
				if(_.className(elements[i],className)){
					classNames.push(elements[i]);
				};
			};
			return classNames;
		};
	},
	className: function(obj,name,reg){
		var _ = web;
		var classNames = new Array();
		classNames = obj.className.split(' ');
		if(!reg){
			var className = new Object();
			for(var i=0;i<classNames.length;i++){
				className[classNames[i]] = true;
			};
			if(name){
				return className[name];
			}
			else {
				return className;
			};
		}
		else {
			var className = null;
			for(var i=0;i<classNames.length;i++){
				if(classNames[i].match(reg)){
					return classNames[i];
				};
			};
			return className;
		};
	},
	addClassName: function(obj,name){
		var _ = web;
		if(!_.className(obj,name)){
			obj.className += ' '+name;
		};
	},
	removeClassName: function(obj,name){
		var _ = web;
		var classNames = [];
		classNames = obj.className.split(' ');
		var setClassName = [];
		for(var i=0;i<classNames.length;i++){
			if(classNames[i] != name)
				setClassName.push(classNames[i]);
		};
		obj.className = setClassName.join(' ');
	},
	addEvent: function(elm,listener,fn){
		try {
			elm.addEventListener(listener,fn,false);
		}
		catch(e){
			elm.attachEvent('on'+listener,fn);
		};
	},
	ready: function(fn){
		if(document.addEventListener){
			document.addEventListener("DOMContentLoaded",fn,false);
		}
		else {
			var IEReady = function(){
				try {
					document.documentElement.doScroll("left");
				}
				catch(e) {
					setTimeout(IEReady,1);
					return;
				};
				fn();
			};
			IEReady();
		};
	}
};
var Mac = navigator.appVersion.indexOf('Mac',0) != -1;
var Win = navigator.appVersion.indexOf('Win',0) != -1;
var IE = navigator.appName.indexOf("Microsoft Internet Explorer",0) != -1;
var NN = navigator.appName.indexOf("Netscape",0) != -1;
var Moz = navigator.userAgent.indexOf("Gecko") != -1;
var Vmajor = parseInt(navigator.appVersion);
var Vminor = parseFloat(navigator.appVersion);
var MacIE4 = ((Mac && navigator.appVersion.indexOf('MSIE 4.',0) != -1));
var MacIE3 = ((Mac && navigator.appVersion.indexOf('MSIE 3.',0) != -1));
function getScrollLeft() {
	if((navigator.appName.indexOf("Microsoft Internet Explorer",0) != -1)) {
		return document.body.scrollLeft;
	}
	else if(window.pageXOffset) {
		return window.pageXOffset;
	}
	else {
		return 0;
	};
};
function getScrollTop() {
	if((navigator.appName.indexOf("Microsoft Internet Explorer",0) != -1)) {
		return document.body.scrollTop;
	}
	else if(window.pageYOffset) {
		return window.pageYOffset;
	}
	else {
		return 0;
	};
};
var pageScrollTimer;
function pageScroll(toX,toY,frms,cuX,cuY) {
	if(pageScrollTimer) clearTimeout(pageScrollTimer);
	if(!toX || toX < 0) toX = 0;
	if(!toY || toY < 0) toY = 0;
	if(!cuX) cuX = 0 + getScrollLeft();
	if(!cuY) cuY = 0 + getScrollTop();
	if(!frms) frms = 6;
	if(toY > cuY && toY > (getAnchorPosObj('end','enddiv').y) - getInnerSize().height) toY = (getAnchorPosObj('end','enddiv').y - getInnerSize().height) + 1;
	cuX += (toX - getScrollLeft()) / frms; if(cuX < 0) cuX = 0;
	cuY += (toY - getScrollTop()) / frms; if(cuY < 0) cuY = 0;
	var posX = Math.floor(cuX);
	var posY = Math.floor(cuY);
	window.scrollTo(posX, posY);
	if(posX != toX || posY != toY) {
		pageScrollTimer = setTimeout("pageScroll("+toX+","+toY+","+frms+","+cuX+","+cuY+")",16);
	};
};
function jumpToPageTop() {
	pageScroll(0,0,5);
};
web.add('ready',function(){
	var div = document.createElement('div');
	div.id = 'pagetop';
	div.onclick = jumpToPageTop;
	document.body.appendChild(div);
	setTimeout(function(){
		document.getElementById('pagetop').style.opacity = 0.5;
	},1000);
});
web.add('ready',function(){
	web.App['overlay'] = {
		Status: false,
		action: {
			init: function(){
				var obj = document.createElement('div');
				obj.id = 'overlay';
				obj.style.height = web.Env['canvas'].height+'px';
				obj.onclick = function(){
					web.App.overlay.action.hide();
				};
				obj.style.display = 'none';
				var inner = document.createElement('div');
				inner.id = 'overlay_inner';
				inner.style.height = web.Env['canvas'].height+'px';
				obj.appendChild(inner);
				var wrap1 = document.createElement('div');
				wrap1.id = 'progress_wrapper';
				var wrap2 = document.createElement('div');
				wrap2.id = 'progress';
				var bar = document.createElement('div');
				bar.id = 'progress_bar';
				wrap2.appendChild(bar);
				var status = document.createElement('div');
				status.id = 'progress_status';
				wrap1.appendChild(status);
				wrap1.appendChild(wrap2);
				obj.appendChild(wrap1);
				document.body.appendChild(obj);
				var iframe = document.createElement('iframe');
				iframe.id = 'overlay_iframe';
				iframe.style.height = web.Env['canvas'].height+'px';
				document.body.appendChild(iframe);
				var img = document.createElement('img');
				img.src = 'inc/_images/close.gif';
				img.id = 'overlay_close';
				img.onclick = function(){
					web.App.overlay.action.hide();
				};
				document.body.appendChild(img);
				var obj = document.createElement('div');
				obj.id = 'uploader_overlay';
				obj.style.height = web.Env['canvas'].height+'px';
				obj.style.display = 'none';
				document.body.appendChild(obj);
				web.App.overlay.action.set(document.body);
			},
			set: function(obj){
				var elements = obj.getElementsByTagName('a');
				for(var i=0;i<elements.length;i++){
					if(elements[i].href.match(/\.(jpg|gif|png)$/) && !elements[i].getAttribute('download')){
						elements[i].onclick = function(){
							web.App.overlay.action.image(this);
							return false;
						};
					}
					else if(elements[i].href.match(/youtube/)){
						elements[i].onclick = function(){
							web.App.overlay.action.iframe(this.href);
							return false;
						};
					}
					else if(elements[i].getAttribute('data-alert')){
						elements[i].onclick = function(){
							if(confirm(this.getAttribute('data-alert'))){
								location.href = this.href;
							};
							return false;
						};
					};
				};
			},
			uploader: {
				show: function(){
					document.getElementById('uploader_overlay').style.display = 'block';
					setTimeout(function(){
						document.getElementById('uploader_overlay').style.opacity = 1;
					},100);
				},
				hide: function(){
					document.getElementById('uploader_overlay').style.opacity = 0;
					document.getElementById('uploader_overlay').style.display = 'none';
				}
			},
			progress: function(par,text){
				document.getElementById('progress_wrapper').style.display = 'block';
				document.getElementById('progress_bar').style.width = par+'%';
				if(text){
					document.getElementById('progress_status').innerHTML = text + ' ' + parseInt(par)+'%';
				}
				else {
					document.getElementById('progress_status').innerHTML = parseInt(par)+'%';
				};
			},
			posted: function(){
				document.getElementById('overlay').style.display = 'block';
				document.getElementById('overlay').onclick = function(){};
				document.getElementById('overlay_close').style.display = 'none';
				document.getElementById('overlay_inner').className = 'overlay_loading';
				return true;
			},
			loading: function(){
				document.getElementById('overlay_inner').className = 'overlay_loading';
			},
			finish: function(){
				document.getElementById('overlay_inner').className = '';
			},
			iframe: function(src){
				web.App.overlay.action.loading();
				document.getElementById('overlay_iframe').src = src;
				document.getElementById('overlay_iframe').style.display = 'block';
				web.App.overlay.action.show();
			},
			image: function(obj){
				web.App.overlay.action.loading();
				var img = new Image();
				img.onload = function(){
					document.getElementById('overlay_inner').className = 'overlay_image';
					document.getElementById('overlay_inner').style.backgroundImage = 'url('+this.src+')';
				};
				img.src = obj.href;
				document.getElementById('overlay_close').style.display = 'block';
				web.App.overlay.action.show();
			},
			toggle: function(){
				if(web.App.overlay.status){
					web.App.overlay.action.hide();
				}
				else {
					web.App.overlay.action.show();
				};
			},
			show: function(loading){
				web.App.overlay.status = true;
				document.getElementById('overlay').style.display = 'block';
				document.getElementById('overlay_close').style.display = 'block';
			},
			hide: function(){
				web.App.overlay.status = false;
				document.getElementById('overlay').style.display = 'none';
				document.getElementById('overlay_close').style.display = 'none';
				document.getElementById('overlay_iframe').src = '';
				document.getElementById('overlay_iframe').style.display = 'none';
				document.getElementById('overlay_inner').style.backgroundImage = 'none';
				document.getElementById('overlay_inner').className = 'overlay_loading';
				document.getElementById('overlay_inner').style.backgroundImage = 'url(inc/_images/loading.gif)';
			}
		}
	};
	web.App.overlay.action.init();
});
web.add('resize',function(){
	document.getElementById('overlay').style.height = web.Env['canvas'].height+'px';
	document.getElementById('uploader_overlay').style.height = web.Env['canvas'].height+'px';
	document.getElementById('overlay_inner').style.height = web.Env['canvas'].height+'px';
	document.getElementById('overlay_iframe').style.height = web.Env['canvas'].height+'px';
	document.getElementById('progress_wrapper').style.top = (web.Env['canvas'].height-24)/2+30+'px';
});
web.add('ready',function(){
	var elements = document.body.getElementsByTagName('a');
	var uri = location.href.split('#')[0];
	for(var i=0;i<elements.length;i++){
		var href = elements[i].href.replace(uri,'');
		if(href.match(/^#.*?$/)){
			elements[i].setAttribute('data-target',href.substring(1,href.length));
			elements[i].onclick = function(){
				var top = 0;
				var offsetTop = document.getElementById(this.getAttribute('data-target')).offsetTop;
				if(offsetTop > web.Env['contents']['height'] - web.Env['canvas']['height']){
					top = web.Env['contents']['height'] - web.Env['canvas']['height'];
				}
				else {
					top = offsetTop;
				};
				scroll(0,top,250);
				return false;
			};
		};
	};
	var hash = location.hash.substring(1,location.hash.length);
	if(document.getElementById(hash)){
		setTimeout(function(){
			var top = 0;
			var offsetTop = document.getElementById(hash).offsetTop;
			if(offsetTop > web.Env['contents']['height'] - web.Env['canvas']['height']){
				top = web.Env['contents']['height'] - web.Env['canvas']['height'];
			}
			else {
				top = offsetTop;
			};
			scroll(0,top,500);
		},100);
	};
});
function jump(obj){
	return false;
};
function easing(t,b,c,d){
	if ((t/=d/2) < 1) return c/2*t*t*t*t + b;
	return -c/2 * ((t-=2)*t*t*t - 2) + b;
};
function scroll(toY,toX,toMsec){
	var begin = new Date() - 0;
	var x = window.pageYOffset || document.body.scrollTop || 0;
	var y = window.pageXOffset || document.body.scrollLeft || 0;
	var moveX = toX - x;
	var moveY = toY - y;
	var duration = toMsec;
	var timer = setInterval(function(){
		var time = new Date() - begin;
		var cuX = Math.floor(easing(time, x, moveX, duration));
		var cuY = Math.floor(easing(time, y, moveY, duration));
		if(time > duration){
			clearInterval(timer);
			cuX = toX;
			cuY = toY;
		};
		window.scrollTo(cuY,cuX);
	},10);
};
web.add('ready',function(){
	if(document.getElementById('fileattached')){
		if(window.File && window.FileReader && window.FileList && window.Blob){
			document.getElementById('fileattached').onclick = function(){
				document.getElementById('file').click();
			};
			document.getElementById('file').onchange = function(){
				_FILE_CHG(this);
			};
		}
		else {
			document.getElementById('fileattached').style.display = 'none';
		};
		document.getElementById('fileattached_cancel').onclick = function(){
			document.getElementById('file').value = '';
			_FILE_CHG(document.getElementById('file'));
		};
	};
});
function _FILE_CHG(obj){
	if(obj.files.length > 0){
		var filesize = 0;
		for(var i=0;i<obj.files.length;i++){
			filesize += obj.files[i].size;
		};
		if(filesize < parseInt(document.getElementById('file').getAttribute('data-size-limit'))){
			var label = document.getElementById('fileattached').getAttribute('data-label');
			label = label.replace('$1',obj.files.length);
			label = label.replace('$2',_FILE_SIZE(filesize));
			document.getElementById('fileattached_label').innerHTML = label;
			document.getElementById('fileattached_label').className = 'icon_file';
		}
		else {
			var label = document.getElementById('file').getAttribute('data-size-limit-error');
			label = label.replace('$1',_FILE_SIZE(parseInt(document.getElementById('file').getAttribute('data-size-limit'))));
			document.getElementById('file').value = '';
			alert(label);
		};
		document.getElementById('fileattached_cancel').style.display = 'block';
	}
	else {
		var label = document.getElementById('fileattached_label').getAttribute('data-label');
		document.getElementById('fileattached_label').innerHTML = label;
		document.getElementById('fileattached_label').className = 'icon_upload';
		document.getElementById('fileattached_cancel').style.display = 'none';
	};
};
function _FILE_SIZE(size){
	var str = ' Byte';
	if(size >= (1024*1024*1024*1024)){
		size = ((size / (1024*1024*1024*1024))*100)/100;
		str = ' TB'
	}
	else if(size >= (1024*1024*1024)){
		size = ((size / (1024*1024*1024))*100)/100;
		str = ' GB'
	}
	else if(size >= (1024*1024)){
		size = ((size / (1024*1024))*100)/100;
		str = ' MB'
	}
	else if(size >= (1024)){
		size = ((size / 1024)*100)/100;
		str = ' KB'
	};
	return size.toFixed(1)+str;
};
web.App['audio'] = {
	Preload: ['notice'],
	Audio: [],
	Type: 'mp3',
	action: {
		init: function(){
			var _ = web.App.audio;
			var audio = new Audio();
			if(("" != audio.canPlayType("audio/ogg"))){
				_.Type = "ogg";
			};
			for(var i=0;i<_.Preload.length;i++){
				_.action.load(_.Preload[i]);
			};
		},
		play: function(id){
			var _ = web.App.audio;
			if(!_.Audio[id]){
				_.action.load(id);
			};
			_.Audio[id].currentTime = 0;
			_.Audio[id].muted = false;
			_.Audio[id].play();
		},
		load: function(id){
			var _ = web.App.audio;
			_.Audio[id] = new Audio();
			_.Audio[id].src = 'inc/_audio/' + id + '.' + _.Type;
			_.Audio[id].autobuffer = true;
			_.Audio[id].load();
		}
	}
};
web.add('ready',function(){
	web.App.audio.action.init();
});
web.App['check'] = {
	List: [],
	Current: 0,
	Handle: null,
	Interval: 5000,
	action: {
		init: function(){
			var _ = web.App.check;
			_.List = web.byClassName(document,'timeago');
			if(_.List.length > 0){
				_.action.run();
			};
		},
		run: function(){
			var _ = web.App.check;
			clearTimeout(_.Handle);
			_.Handle = setTimeout(function(){
				var json = _.List[_.Current].getAttribute('data-json');
				if(json){
					web.json(json + '?' + (new Date()-1),function(){
					});
				}
				else {
					_.Current++;
					_.Current = _.Current % _.List.length;
				};
			},_.Interval);
		},
		callback: function(t){
			var _ = web.App.check;
			var s = parseInt(_.List[_.Current].getAttribute('data-time'));
			if( (t*1000) > s ){
				web.App.audio.action.play('notice');
			};
			_.List[_.Current].setAttribute('data-time',t*1000);
			_.Current++;
			_.Current = _.Current % _.List.length;
			_.action.run();
		}
	}
};
web.add('ready',function(){
	var objects = web.byClassName(document,'filesize');
	for(var i=0;i<objects.length;i++){
		objects[i].innerHTML = ' (' + _FILE_SIZE(parseInt(objects[i].getAttribute('data-size'))) + ')';
	};
});
web.App['keybind'] = {
	Focus: false,
	action: {
		init: function(){
			document.getElementById('text').onkeydown = function(){
				web.App.keybind.action.enter();
			};
			document.getElementById('text').onblur = function(){
				web.App.keybind.Focus = false;
			};
		},
		enter: function(){
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt.key == 'Enter' && evt.shiftKey){
				evt.returnValue = false;
				entry();
				return false;
			};
		},
		move: function(evt){
			evt.which = null;
			return false;
		}
	}
};
web.add('ready',function(){
	if(document.getElementById('text')){
		web.App.keybind.action.init();
	};
});
window.document.onkeydown = function(evt){
	if(document.getElementById('text')){
		if(!web.App.keybind.Focus){
			if(evt.key == 'ArrowUp'){
				evt.returnValue = false;
				evt.which = null
				web.App.ui.action.up();
				return false;
			}
			else if(evt.key == 'ArrowDown'){
				evt.returnValue = false;
				evt.which = null
				web.App.ui.action.down();
				return false;
			};
		};
	};
};
function langsw(obj){
	var uri = location.href.split('?')[0];
	if(location.search){
		var p = location.href.split('?')[1].split('#')[0].split('&');
		var u = [];
		for(var i=0;i<p.length;i++){
			var nv = p[i].split('=');
			if(nv[0] != 'lang'){
				u.push(p[i]);
			};
		};
		u.push("lang="+obj.value);
		location.href = uri + '?' + u.join('&');
	}
	else {
		var u = [];
		u.push("lang="+obj.value);
		location.href = uri + '?' + u.join('&');
	};
};
web.add('ready',function(){
	var textarea = web.byClassName(document,'plaintext');
	for(var i=0;i<textarea.length;i++){
		var obj = textarea[i];
		var height = obj.scrollHeight || obj.offsetHeight;
		textarea[i].style.height = height + 'px';
	};
});
var postFormToggleStatus = false;
function postFormToggleSwitch(){
	var _ = web;
	var height = (_.Env['canvas']['height'] / 2);
	if(document.getElementById('chat').checked){
		height = height / 2;
	};
	if(postFormToggleStatus){
		document.getElementById('postform').style.marginBottom = '0px';
		postFormToggleStatus = false;
	}
	else {
		document.getElementById('postform').style.marginBottom = height + 'px';
		document.getElementById('text').focus();
		postFormToggleStatus = true;
	};
};
function entry(){
	if(document.getElementById('text').value != '' || document.getElementById('file').value != ''){
		web.App.overlay.action.posted();
		document.getElementById('submittime').value = parseInt(((new Date())-1) / 1000);
		document.getElementById('thread').submit();
	};
	return false;
};
function postFormResizing(){
	var _ = web;
	var height = _.Env['canvas']['height'] / 2;
	if(document.getElementById('chat').checked){
		height = height / 2;
	};
	document.getElementById('text').style.height = height + 'px';
	document.getElementById('postform').style.bottom = (height * -1) + 'px';
	if(postFormToggleStatus){
		document.getElementById('postform').style.marginBottom = height + 'px';
	};
};
web.add('ready',function(){
	var _ = web;
	if(document.getElementById('text')){
		document.getElementById('text').onfocus = function(){
			web.App.keybind.Focus = true;
			document.getElementById('focustime').value = parseInt(((new Date())-1) / 1000);
		};
	};
	if(document.getElementById('chat')){
		document.getElementById('chat').onchange = function(){
			postFormResizing();
		};
	};
	if(document.getElementById('postform')){
		postFormResizing();
		setTimeout(function(){
			document.getElementById('postform').style.opacity = 1;
		},500);
	};
	if(document.getElementById('formtoggle')){
		document.getElementById('formtoggle').onclick = function(){
			postFormToggleSwitch();
		};
	};
	if(document.getElementById('togglebar')){
		document.getElementById('togglebar').onclick = function(){
			postFormToggleSwitch();
		};
	};
});
web.add('resize',function(){
	var _ = web;
	if(document.getElementById('postform')){
		postFormResizing();
	};
});
function searchRes(){
	for(var ii=0;ii<document.getElementsByTagName('section').length;ii++){
		var tags = document.getElementsByTagName('section')[ii].getElementsByTagName('*');
		for(var iii=0;iii<tags.length;iii++){
			if(tags[iii].tagName == 'P' || tags[iii].tagName == 'LI'){
				tags[iii].ondblclick = function(){
					setRes(this);
				};
			};
		};
	};
};
function insertReply(str){
	if(web.$('text').value == ''){
		web.$('text').value = str + "\n";
	}
	else if(web.$('text').value.match(/\n$/)){
		web.$('text').value += str + "\n";
	}
	else {
		web.$('text').value += "\n" + str + "\n";
	};
};
function setRes(obj){
	var str = obj.innerHTML;
	str = str.replace(/<.*?>/ig,'');
	insertReply('> ' + str);
	if(!postFormToggleStatus){
		postFormToggleSwitch();
	};
};
function reply(obj){
	var str = "";
	console.log(obj.parentNode);
	for(var i=0;i<obj.parentNode.getElementsByTagName('section').length;i++){
		var tags = obj.parentNode.getElementsByTagName('section')[i].getElementsByTagName('*');
		for(var ii=0;ii<tags.length;ii++){
			if(tags[ii].tagName == 'P' || tags[ii].tagName == 'LI'){
				var html = tags[ii].innerHTML;
				html = html.replace(/<.*?>/ig,'');
				str += '> ' + html + "\n";
			};
		};
	};
	insertReply(str);
	if(!postFormToggleStatus){
		postFormToggleSwitch();
	};
};
web.add('ready',function(){
	if(document.getElementById('threads')){
		searchRes();
	};
});
web.App['resize'] = {
	Current: 0,
	Redirect: '',
	Que: [],
	process: function(){
		var _ = web.App.resize;
		if(_.Current < _.Que.length){
			_.json(_.Que[_.Current]);
		}
		else {
			window.parent.web.App.overlay.action.progress(100,'Image resizing...');
			setTimeout(function(){
				window.parent.web.App.submit.process();
			},500);
		};
	},
	callback: function(stat){
		var _ = web.App.resize;
		_.Current++;
		var par = parseInt((_.Current / _.Que.length) * 100);
		window.parent.web.App.overlay.action.progress(par,'Image resizing...');
		_.process();
	},
	json: function(key){
		var script = document.createElement('script');
		script.async = false;
		script.type = 'text/javascript';
		script.src = 'resize.php?key='+key;
		script.charset = 'UTF-8';
		document.body.appendChild(script);
	}
};
web.add('ready',function(){
	if(location.hash){
		var hash = location.hash.substring(1,location.hash.length);
		if(web.$('status_'+hash)){
			var div = document.createElement('div');
			div.id = 'status';
			div.innerHTML = web.$('status_'+hash).innerHTML;
			var e = document.getElementsByTagName('main')[0];
			e.insertBefore(div, e.firstChild);
			setTimeout(function(){
				web.$('status').style.display = 'none';
			},2000);
		};
	};
});
web.App['submit'] = {
	Close: false,
	process: function(){
		var _ = web.App.submit;
		document.getElementById('text').value = '';
		document.getElementById('file').value = '';
		_FILE_CHG(document.getElementById('file'));
		if(!document.getElementById('chat').checked){
			postFormToggleSwitch();
		};
		document.getElementById('progress_wrapper').style.display = 'none';
		web.App.overlay.action.hide();
		web.App.thread.action.check();
	}
};
web.App['thread'] = {
	Qty: 0,
	Dir: null,
	Handle: null,
	Interval: 5000,
	Lastmodified: null,
	Chat: false,
	action: {
		qty: function(){
			var obj = web.byClassName(document.getElementById('threads'),'qtyMax');
			for(var i=0;i<obj.length;i++){
				obj[i].innerHTML = '/'+web.App.thread.Qty;
			};
		},
		check: function(){
			clearTimeout(web.App.thread.Handle);
			web.json(web.App.thread.Dir+'update.json?time='+(new Date()-1));
		},
		update: function(html,sortable){
			var id = 'add_thread_'+(new Date()-1);
			var div = document.createElement('div');
			div.id = id;
			div.className = 'addthread';
			div.innerHTML = html;
			if(sortable){
				document.getElementById('threads').insertBefore(div, document.getElementById('threads').firstChild);
			}
			else {
				document.getElementById('threads').appendChild(div);
			};
			(function(){
				setTimeout(function(){
					scroll(0,web.App.ui.action.position(document.getElementById(id))[1],500);
					var objects = web.byClassName(document.getElementById(id),'timeago');
					for(var i=0;i<objects.length;i++){
						var obj = objects[i];
						timeago(obj);
					};
					searchRes();
					web.App.overlay.action.set(document.getElementById(id));
					document.getElementById(id).style.opacity = 1;
				},100);
			})();
			web.App.audio.action.play('notice');
			web.App.thread.action.qty();
			web.App.thread.action.run();
		},
		callback: function(qty){
			if(qty > web.App.thread.Qty){
				web.json('index.cgi?t='+web.GET['t']+'&app=json&since='+web.App.thread.Qty);
			}
			else {
				web.App.thread.action.run();
			};
			web.App.thread.Qty = qty;
		},
		run: function(){
			clearTimeout(web.App.thread.Handle);
			web.App.thread.Handle = setTimeout(function(){
				web.App.thread.action.check();
			},web.App.thread.Interval);
		}
	}
};
var timeagoObjects = [];
web.add('ready',function(){
	try {
		if(timeagoStrings){
			timeagoObjects = timeagoStrings.split(',');
			var objects = web.byClassName(document,'timeago');
			for(var i=0;i<objects.length;i++){
				var obj = objects[i];
				timeago(obj);
			};
		};
	}
	catch(e){
	};
});
function timeago(obj){
	var c = parseInt((new Date()-0) / 1000)
	var p = parseInt((new Date(parseInt(obj.getAttribute('data-time')))-0) / 1000);
	var t = c - p;
	obj.className = 'timeago';
	if(t < 60){
		obj.innerHTML = timeagoObjects[0].replace('$1',t);
		web.addClassName(obj,'timeago-lebel5');
		setTimeout(function(){
			timeago(obj);
		},1000);
	}
	else if(t < (60 * 60)){
		var tm = t / 60;
		if(tm < 5){
			web.addClassName(obj,'timeago-lebel4');
		}
		else if(tm < 10){
			web.addClassName(obj,'timeago-lebel3');
		}
		else if(tm < 30){
			web.addClassName(obj,'timeago-lebel2');
		}
		else {
			web.addClassName(obj,'timeago-lebel1');
		};
		obj.innerHTML = timeagoObjects[1].replace('$1',Math.round(t / 60));
		setTimeout(function(){
			timeago(obj);
		},10000);
	}
	else if(t < (60 * 60 * 24)){
		obj.innerHTML = timeagoObjects[2].replace('$1',Math.round(t / 3600));
		setTimeout(function(){
			timeago(obj);
		},10000);
	}
	else if(t < (60 * 60 * 24 * 30)){
		obj.innerHTML = timeagoObjects[3].replace('$1',Math.round(t / 86400));
		setTimeout(function(){
			timeago(obj);
		},10000);
	}
	else if(t < (60 * 60 * 24 * 365)){
		obj.innerHTML = timeagoObjects[4].replace('$1',Math.round(t / 2592000));
		setTimeout(function(){
			timeago(obj);
		},10000);
	}
	else {
		obj.innerHTML = timeagoObjects[5].replace('$1',Math.round(t / 31536000));
		setTimeout(function(){
			timeago(obj);
		},10000);
	};
};
web.App['ui'] = {
	Step: [],
	Current: null,
	Handle: null,
	action: {
		init: function(){
			document.getElementById('ui_up').onclick = function(){
				web.App.ui.action.up();
			};
			document.getElementById('ui_down').onclick = function(){
				web.App.ui.action.down();
			};
		},
		up: function(){
			var y = (document.documentElement.scrollTop || document.body.scrollTop);
			var obj = web.byClassName(document.getElementById('threads'),'post');
			var top = 0;
			for(var i=0;i<obj.length;i++){
				var objY = web.App.ui.action.position(obj[i])[1];
				if(objY < y){
					top = objY;
				}
				else {
					break;
				}
			};
			scroll(0,top,500);
		},
		down: function(){
			var y = (document.documentElement.scrollTop || document.body.scrollTop);
			var obj = web.byClassName(document.getElementById('threads'),'post');
			var top = 0;
			for(var i=0;i<obj.length;i++){
				var objY = web.App.ui.action.position(obj[i])[1];
				if(objY > y){
					top = objY;
					break;
				};
			};
			if(top){
				scroll(0,top,500);
			};
		},
		index: function(){
		},
		position: function(obj){
			var x=0,y=x;
			do x += obj.offsetLeft, y += obj.offsetTop; while (obj = obj.offsetParent);
			return [x,y];
		}
	}
};
web.add('ready',function(){
	if(uploader.enabled){
		web.addEvent(document.body,'dragover',uploader.action.on);
		web.addEvent(document.getElementById('uploader_overlay'),'dragover',uploader.action.over);
		web.addEvent(document.getElementById('uploader_overlay'),'drop',uploader.action.drop);
		web.addEvent(document.getElementById('uploader_overlay'),'dragenter',uploader.action.enter);
		web.addEvent(document.getElementById('uploader_overlay'),'dragleave',uploader.action.leave);
	};
});
var files = [];
var XMLhttpObj = null;
var uploader = {
	enabled: false,
	vars: {
		id: null,
		list: [],
		images: [],
		current: 0,
		XMLhttpObj: null
	},
	action: {
		on: function(e){
			e.stopPropagation();
			e.preventDefault();
			if(uploader.enabled){
				web.App.overlay.action.uploader.show();
			};
		},
		over: function(e){
			e.stopPropagation();
			e.preventDefault();
		},
		drop: function(e){
			if(e.dataTransfer.files.length > 0){
				uploader.enabled = false;
				uploader.vars.files = e.dataTransfer.files;
				uploader.vars.id = (new Date()-0);
				e.stopPropagation();
				e.preventDefault();
				web.App.overlay.action.uploader.hide();
				web.App.overlay.action.posted();
				web.App.overlay.action.progress(0);
				uploader.action.upload();
			}
			else {
				web.App.overlay.action.uploader.hide();
			};
		},
		enter: function(e){
			e.stopPropagation();
			e.preventDefault();
		},
		leave: function(e){
			e.stopPropagation();
			e.preventDefault();
			if(uploader.enabled){
				web.App.overlay.action.uploader.hide();
			};
		},
		upload: function(){
			var uploadFile = uploader.vars.files[uploader.vars.current];
			uploader.vars.XMLhttpObj = uploader.action.createXMLHttpRequest();
			uploader.vars.XMLhttpObj.onreadystatechange = uploader.action.callback;
			uploader.vars.XMLhttpObj.open('POST','index.cgi?app=upload&qty='+(uploader.vars.files.length-1)+'&id='+uploader.vars.id+'&filename='+encodeURIComponent(uploadFile.name)+'&phase='+uploader.vars.current+'&bin=1&t='+web.GET['t'],true);
			uploader.vars.XMLhttpObj.upload.addEventListener('progress', uploader.action.progress, false);
			uploader.vars.XMLhttpObj.setRequestHeader('Content-Type', 'application/octet-stream');
			uploader.vars.XMLhttpObj.setRequestHeader('X-File-Name', encodeURIComponent(uploadFile.name));
			if('getAsBinary' in uploadFile){
				uploader.vars.XMLhttpObj.sendAsBinary(uploadFile.getAsBinary());
			}
			else {
				uploader.vars.XMLhttpObj.send(uploadFile);
			};
		},
		progress: function(e){
			var block = 100 / uploader.vars.files.length;
			var percent = (block * Math.floor(event.loaded / event.total)) + (block * uploader.vars.current);
			web.App.overlay.action.progress(percent,'File uploading...');
		},
		callback: function(){
			if(uploader.vars.XMLhttpObj.readyState == 4 && uploader.vars.XMLhttpObj.status == 200){
				uploader.vars.current++;
				if(uploader.vars.XMLhttpObj.responseText != 'false'){
					web.App.resize.Que.push(uploader.vars.XMLhttpObj.responseText);
				};
				if(uploader.vars.current < uploader.vars.files.length){
					uploader.action.upload();
				}
				else {
					if(web.App.resize.Que.length > 0){
						web.App.resize.Redirect = 'index.cgi?t='+web.GET['t']+'&time='+(new Date()-0)+'#recency';
						web.App.resize.process();
					}
					else {
						location.href = 'index.cgi?t='+web.GET['t']+'&time='+(new Date()-0)+'#recency';
					};
				};
			};
		},
		createXMLHttpRequest: function(){
			var XMLhttpObject = null;
			try{
				XMLhttpObject = new XMLHttpRequest();
			}
			catch(e){
				try{
					XMLhttpObject = new ActiveXObject('Msxml2.XMLHTTP');
				}
				catch(e){
					try{
						XMLhttpObject = new ActiveXObject('Microsoft.XMLHTTP');
					}
					catch(e){
						return null;
					};
				};
			};
			return XMLhttpObject;
		},
	}
};
web.add('ready',function(){
	if(document.getElementById('threaduri')){
		document.getElementById('threadurivalue').value = document.getElementById('threaduri').href;
	};
});
web.initialize();

var web = {
	App: [],
	Env: [],
	GET: [],
	Extend: [],
	Title: document.title,
	callback: function(str){
		web.log(str);
	},
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
	},
	sanitizing: function(str){
		var before = new Array('&','"',"'","<",">","\n","\t","\n"," ",',');
		var after = new Array('&amp;','&quot;','&rsquo;',"&lt;","&gt;","<br />","  ","<br>","&nbsp;",'&#x2c;');
		for(var i=0;i<before.length;i++){
			str = str.replace(new RegExp(before[i],'g'), after[i]);
		};
		return str;
	},
	unsanitizing: function(str){
		var before = new Array('&amp;','&quot;','&rsquo;',"&lt;","&gt;","<br />","  ","<br>"," ",'&#x2c;','&nbsp;&nbsp;&nbsp;&nbsp;','&nbsp;');
		var after = new Array('&','"',"'","<",">","\n","\t","\n"," ",',',"\t"," ");
		for(var i=0;i<before.length;i++){
			str = str.replace(new RegExp(before[i],'g'), after[i]);
		};
		return str;
	}
};
web.log = function(str,level){
	var target = '';
	if(target == level || target == ''){
	};
};
web.App['keybind'] = {
	action: {
		init: function(){
			document.body.onkeyup = function(){
				web.App.keybind.action.keyup();
			};
		},
		keyup: function(){
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt.key == 'Tab' && evt.ctrlKey){
				evt.preventDefault();
				web.App.controller.action.tab();
				return false;
			}
			else if((evt.key == 'f' || evt.key == 'F') && evt.ctrlKey){
				evt.preventDefault();
				web.$('q').focus();
				return false;
			};
		}
	}
};
web.add('ready',function(){
	web.App.keybind.action.init();
});
web.add('resize',function(){
	var _ = web;
	document.getElementsByTagName('main')[0].style.width = (_.Env['canvas'].width - 240) + 'px';
	document.getElementsByTagName('main')[0].style.height = (_.Env['canvas'].height - 85) + 'px';
	document.getElementById('app_main').style.width = (_.Env['canvas'].width - 240) + 'px';
	document.getElementById('app_main').style.height = (_.Env['canvas'].height - 85) + 'px';
	document.getElementById('app_note').style.width = (_.Env['canvas'].width - 240) + 'px';
	document.getElementById('app_note').style.height = (_.Env['canvas'].height - 85 - 52 - 23 - 26) + 'px';
	document.getElementById('app_main_analyze_main').style.width = (_.Env['canvas'].width - 240) + 'px';
	document.getElementById('app_main_analyze_main').style.height = (_.Env['canvas'].height - 132) + 'px';
	document.getElementById('app_main_logs').style.height = (_.Env['canvas'].height - 132) + 'px';
	document.getElementById('app_main_logs_main').style.height = (_.Env['canvas'].height - 132) + 'px';
	document.getElementById('app_main_logs_timeline').style.width = (_.Env['canvas'].width - 560) + 'px';
	document.getElementById('app_main_logs_timeline').style.height = (_.Env['canvas'].height - 132) + 'px';
	document.getElementById('app_main_logs_todo').style.height = (_.Env['canvas'].height - 132 - 240 - 10) + 'px';
	document.getElementById('app_main_logs_form').style.width = (_.Env['canvas'].width - 560) + 'px';
	document.getElementById('app_main_logs_input').style.width = (_.Env['canvas'].width - 590) + 'px';
	document.getElementsByTagName('aside')[0].style.height = (_.Env['canvas'].height - 85 - 20) + 'px';
});
web.App['string'] = {
	TimeagoObjects: [],
	action: {
		init: function(){
			web.App.string.TimeagoObjects = web.Lang.timeago.split(',');
		},
		sec: function(obj,t){
			var timeagoObjects = web.App.string.TimeagoObjects;
			var ajust = 0;
			if(t == 0){
				web.App.audio.action.play('03_ALERT');
			};
			if(t < 0){
				t = t * -1;
				ajust = 6;
				if(t < 60*60){
					obj.style.color = '#F00';
					obj.style.fontWeight = 'bolder';
				}
				else if(t < (60*60*24)){
					obj.style.color = '#A00';
					obj.style.fontWeight = 'bolder';
				}
				else if(t < (60*60*24*3)){
					obj.style.color = '#800';
				}
				else {
					obj.style.color = '#600';
				};
			}
			else {
				if(t < 60*60){
					obj.style.color = '#080';
					obj.style.fontWeight = 'bolder';
				}
				else if(t < (60*60*24)){
					obj.style.color = '#060';
					obj.style.fontWeight = 'bolder';
				}
				else if(t < (60*60*24*3)){
					obj.style.color = '#666';
				}
				else {
					obj.style.color = '#999';
				};
			};
			if(t < 60){
				t = timeagoObjects[0+ajust].replace('$1',t);
			}
			else if(t < (60 * 60)){
				t = timeagoObjects[1+ajust].replace('$1',Math.round(t / 60 * 10) / 10);
			}
			else if(t < (60 * 60 * 24)){
				t = timeagoObjects[2+ajust].replace('$1',Math.round(t / 3600 * 10) / 10);
			}
			else if(t < (60 * 60 * 24 * 30)){
				t = timeagoObjects[3+ajust].replace('$1',Math.round(t / 86400 * 10) / 10);
			}
			else if(t < (60 * 60 * 24 * 365)){
				t = timeagoObjects[4+ajust].replace('$1',Math.round(t / 2592000 * 10) / 10);
			}
			else {
				t = timeagoObjects[5+ajust].replace('$1',Math.round(t / 31536000 * 10) / 10);
			};
			obj.innerHTML = t;
			return t;
		},
		time: function(t){
			if(t < 60){
				t = '00:00:' + web.App.string.action.digit(t);
			}
			else if(t < 3600){
				t = '00:' + web.App.string.action.digit(t/60) + ':' + web.App.string.action.digit(t%60)
			}
			else {
				t = web.App.string.action.digit(t/3600) + ':' + web.App.string.action.digit(((t%3600)/60)) + ':' + web.App.string.action.digit((t%60))
			};
			return t;
		},
		date: function(y,m,d){
			return y+'-'+web.App.string.action.digit(m)+'-'+web.App.string.action.digit(d);
		},
		digit: function(n){
			n = parseInt(n);
			if(n < 10){
				n = '0'+n;
			};
			return n;
		}
	}
};
web.add('ready',function(){
	web.App.string.action.init();
});
web.App['audio'] = {
	Mute: true,
	Audio: [],
	Type: 'mp3',
	Preload: ['01_TODO_FINISH','02_APP_SWITCH','03_ALERT','04_TIMER_END','05_TIMER_START','06_FOLDER','07_LIFELOG','08_UPDATE','09_DROP','10_REMOVE','11_SAVE'],
	action: {
		init: function(){
			if(window.localStorage){
				var s = window.localStorage;
				web.$('audio_button').onclick = function(){
					if(web.App.audio.Mute){
						web.App.audio.Mute = false;
						window.localStorage['WEBPAD_AUDIO'] = 1;
						this.className = '';
					}
					else {
						web.App.audio.Mute = true;
						window.localStorage['WEBPAD_AUDIO'] = 0;
						this.className = 'mute';
					};
				};
				if(s['WEBPAD_AUDIO'] == '1'){
					web.$('audio_button').className = '';
					web.App.audio.Mute = false;
				};
				var a = new Audio();
				if(("" != a.canPlayType("audio/ogg"))){
					web.App.audio.Type = "ogg";
				};
				if(!web.App.audio.Mute){
					for(var i=0;i<web.App.audio.Preload.length;i++){
						var type = web.App.audio.Preload[i];
						web.App.audio.Audio[type] = new Audio();
						web.App.audio.Audio[type].src = 'inc/_audio/' + type + "." + web.App.audio.Type;
						web.App.audio.Audio[type].autobuffer = true;
						web.App.audio.Audio[type].volume = 0.2;
						web.App.audio.Audio[type].load();
					};
				};
			}
			else {
				web.$('audio_button').style.display = 'none';
			};
		},
		play: function(type){
			if(!web.App.audio.Mute){
				if(web.App.audio.Audio[type]){
					web.App.audio.Audio[type].currentTime = 0;
					web.App.audio.Audio[type].play();
				}
				else {
					web.App.audio.Audio[type] = new Audio();
					web.App.audio.Audio[type].src = 'inc/_audio/' + type + "." + web.App.audio.Type;
					web.App.audio.Audio[type].autobuffer = true;
					web.App.audio.Audio[type].volume = 0.2;
					web.App.audio.Audio[type].onloadeddata = function(){
						this.currentTime = 0;
						this.play();
					};
					web.App.audio.Audio[type].load();
				};
			};
		}
	}
};
web.add('ready',function(){
	web.App.audio.action.init();
});
web.App['controller'] = {
	Current: null,
	Apps: ['note','logs','analyze'],
	AppsIndex: [],
	action: {
		init: function(){
			var _ = web;
			for(var i=0;i<_.App.controller.Apps.length;i++){
				_.App.controller.AppsIndex[_.App.controller.Apps[i]] = i;
			};
			web.$('nav_app_note').onclick = function(){
				web.App.controller.action.show('note');
			};
			web.$('nav_app_logs').onclick = function(){
				web.App.controller.action.show('logs');
			};
			web.$('nav_app_file').onclick = function(){
				web.App.controller.action.show('file');
			};
			web.$('nav_app_file').parentNode.style.display = 'none';
			web.$('nav_app_analyze').onclick = function(){
				web.App.controller.action.show('analyze');
			};
			web.$('nav_app_setting').onclick = function(){
				window.open('index.cgi?app=setting&key=' + web.GET['key']);
			};
			web.$('nav_app_logout').onclick = function(){
				location.href = 'index.cgi?key=' + web.GET['key'] + '&app=logout';
			};
			window.onfocus = function(){
				web.App.controller.action.initialize();
			};
			if(window.localStorage['webpad_current']){
				web.App.controller.action.show(window.localStorage['webpad_current']);
			}
			else {
				web.App.controller.action.show('logs');
			};
			setTimeout(function(){
			},1000);
		},
		tab: function(){
			var index = (web.App.controller.AppsIndex[web.App.controller.Current]+1) % web.App.controller.Apps.length;
			web.log(index,1);
			web.App.controller.action.show(web.App.controller.Apps[index]);
		},
		show: function(app){
			if(web.App.controller.Current != app){
				if(web.$('app_main_'+app)){
					web.App.audio.action.play('02_APP_SWITCH');
					web.App.controller.action.hide(web.App.controller.Current);
					web.$('app_main_'+app).style.opacity = '1';
					web.$('app_main_'+app).style.marginLeft = '0%';
					web.$('nav_app_'+app).style.borderBottom = 'solid 2px #DEA100';
					web.App.controller.Current = app;
					if(window.localStorage){
						window.localStorage.setItem('webpad_current',app);
					};
					web.App.controller.action.initialize();
				};
			};
		},
		initialize: function(){
			try {
				web.App[web.App.controller.Current].action.startup();
			}catch(e){};
		},
		hide: function(app){
			if(web.$('app_main_'+app)){
				web.$('app_main_'+app).style.opacity = '0';
				web.$('app_main_'+app).style.marginLeft = '-100%';
			};
			if(web.$('nav_app_'+app)){
				web.$('nav_app_'+app).style.borderBottom = 'none';
			};
		}
	}
};
web.add('ready',function(){
	web.App.controller.action.init();
});
web.App['object'] = {
	action: {
		init: function(){
			var _ = web;
			(function(){
				var div = document.createElement('div');
				div.id = 'mobile_todo';
				div.onclick = function(){
					if(web.$('app_main_logs_todo').className == ''){
						web.$('app_main_logs_todo').className = 'open'
					}
					else {
						web.$('app_main_logs_todo').className = ''
					};
				};
				document.body.appendChild(div);
			})();
			(function(){
				var div = document.createElement('div');
				div.id = 'mobile_folder';
				div.onclick = function(){
					console.log(web.$('finder').className);
					if(web.$('finder').className == ''){
						web.$('finder').className = 'open'
					}
					else {
						web.$('finder').className = ''
					};
				};
				document.body.appendChild(div);
			})();
			(function(){
				var div = document.createElement('div');
				div.id = 'mobile_calendar';
				div.onclick = function(){
					console.log(web.$('app_main_logs_calendar').className);
					if(web.$('app_main_logs_calendar').className == ''){
						web.$('app_main_logs_calendar').className = 'open'
					}
					else {
						web.$('app_main_logs_calendar').className = ''
					};
				};
				document.body.appendChild(div);
			})();
		}
	}
};
web.add('ready',function(){
	web.App.object.action.init();
});
web.App['search'] = {
	Interval: null,
	Cache: null,
	Toggle: false,
	Stat: false,
	action: {
		init: function(){
			var _ = web;
			_.$('search_toggle').onclick = function(){
				if(web.App.search.Toggle){
					_.removeClassName(_.$('search'),'open');
					web.App.search.Toggle = false;
				}
				else {
					_.addClassName(_.$('search'),'open');
					web.App.search.Toggle = true;
					_.$('q').focus();
				};
			};
			_.$('search').onsubmit = function(){
				return false;
			};
			_.$('search_clear').onclick = function(){
				web.$('q').value = '';
				clearTimeout(web.App.search.Interval);
				web.App.explorer.action.cd('root');
				web.App.search.Cache = null;
			};
			_.$('q').onkeyup = function(){
				clearTimeout(web.App.search.Interval);
				if(this.value != ''){
					_.$('search_clear').style.display = 'block';
					if(web.App.search.Cache != this.value){
						web.App.search.Interval = setTimeout(function(){
							web.App.search.action.search();
						},500);
					};
				}
				else {
					_.$('search_clear').style.display = 'none';
					web.App.search.Interval = setTimeout(function(){
						web.App.explorer.action.cd('root');
					},500);
				};
			};
		},
		search: function(){
			clearTimeout(web.App.search.Interval);
			web.App.search.Cache = web.$('q').value;
			var str = web.$('q').value;
			if(str != ''){
				web.App.search.Stat = true;
				web.json('index.cgi?key=' + web.GET['key'] + '&app=search&q=' + encodeURIComponent(str));
				web.log('search run','search');
			};
		},
		callback: function(note,logs,todo,path,index,id,parent){
			web.App.data.action.rebuild(note,logs,todo,path,index,id,parent);
			web.$('app_main_logs_timeline').scrollTop = 0;
			web.App.audio.action.play('12_SEARCH');
			setTimeout(function(){
				web.$('q').focus();
				web.App.search.Stat = false;
			},500);
		}
	}
};
web.add('ready',function(){
	web.App.search.action.init();
});
web.App['status'] = {
	Interval: null,
	action: {
		init: function(){
			var _ = web;
			var div = document.createElement('div');
			div.id = 'status_wrapper';
			var span = document.createElement('span');
			span.id = 'status_inner';
			span.innerHTML = 'Status';
			div.appendChild(span);
			document.body.appendChild(div);
		},
		show: function(text){
			clearTimeout(web.App.status.Interval);
			web.$('status_inner').innerHTML = text;
			web.$('status_wrapper').style.opacity = '1';
			web.$('status_wrapper').style.bottom = '20px';
			web.App.status.Interval = setTimeout(function(){
				web.$('status_wrapper').style.opacity = '0';
				web.$('status_wrapper').style.bottom = '-200px';
			},2000);
		}
	}
};
web.add('ready',function(){
	web.App.status.action.init();
});
web.App['timeago'] = {
	Interval: null,
	action: {
		rebuild: function(){
			clearTimeout(web.App.timeago.Interval);
			var obj = web.byClassName(document.body,'timeago');
			var t = (new Date()).getTime() / 1000;
			for(var i=0;i<obj.length;i++){
				var getTime = obj[i].getAttribute('data-gettime');
				var s = 0;
				if(getTime){
					s = getTime;
				}
				else {
					obj[i].title = obj[i].getAttribute('data-time');
					var time = obj[i].getAttribute('data-time').replace(/\-/ig,'/');
					s = (new Date(time)).getTime() / 1000;
					obj[i].setAttribute('data-gettime',s)
				};
				web.App.string.action.sec(obj[i],parseInt(t - s));
			};
			web.App.timeago.Interval = setTimeout(function(){
				web.App.timeago.action.rebuild();
			},1000);
		}
	}
};
web.add('ready',function(){
	web.App.timeago.action.rebuild();
});
web.App['data'] = {
	Uri: null,
	Note: [],
	Logs: [],
	Todo: [],
	Interval: null,
	Timer: 2000,
	action: {
		init: function(){
			web.App.data.Uri = web.App.Dir + 'index.json';
			web.App.data.Interval = setTimeout(function(){
				web.json(web.App.data.Uri+'?'+(new Date()-0));
			},web.App.data.Timer);
		},
		update: function(logs){
			web.App.logs.action.update(logs);
			clearTimeout(web.App.data.Interval);
			web.App.data.Interval = setTimeout(function(){
				web.json(web.App.data.Uri+'?'+(new Date()-0));
			},web.App.data.Timer);
		},
		index: function(index){
			clearTimeout(web.App.data.Interval);
			if(index > web.App.logs.Index){
				web.json('index.cgi?key=' + web.GET['key'] + '&app=update' + '&id=' + web.App.explorer.Current + '&index=' + web.App.logs.Index);
				web.App.logs.Index = index;
			}
			else {
				web.App.data.Interval = setTimeout(function(){
					web.json(web.App.data.Uri+'?'+(new Date()-0));
				},web.App.data.Timer);
			};
		},
		rebuild: function(note,logs,todo,path,index,id,parent){
			web.log(note,'search');
			web.log(logs,'search');
			web.log(todo,'search');
			web.log(path,'path');
			web.log(index,'index');
			web.log(id,'id');
			web.log(parent,'parent');
			web.App.data.Todo = todo;
			if(id){
				web.App.explorer.Current = id;
			};
			if(parent){
				web.App.explorer.Parent = parent;
			};
			web.App.explorer.action.rebuild(note,path);
			web.App.todo.action.rebuild(todo);
			web.App.calendar.action.update(todo);
			web.App.logs.action.rebuild(logs);
			web.App.note.action.newpad();
			web.App.controller.action.initialize();
		}
	}
};
web.add('ready',function(){
	web.App.data.action.init();
});
web.App['draganddrop'] = {
	action: {
		setDrop: function(obj){
			obj.ondrop = function(evt){
				web.App.audio.action.play('09_DROP');
				var id = evt.dataTransfer.getData("text");
				var toId = obj.getAttribute('data-dir-drag') || obj.id;
				if(id.match(/^todo_/)){
					if(web.$(id).getAttribute('data-parent')){
						web.App.todo.action.qtyChg(web.$(id).getAttribute('data-parent'),-1);
						web.$(id).setAttribute('data-parent',toId);
					};
					id = id.replace(/^todo_/ig,'');
					web.App.todo.action.dragTodo(id,toId);
				}
				else {
					if(id != toId){
						web.App.explorer.action.dragNote(id,toId);
					};
				};
				evt.preventDefault();
			};
			obj.ondragover = function(evt){
				evt.preventDefault();
			};
		},
		setDrag: function(obj){
			obj.setAttribute('draggable','true');
			obj.draggable = true;
			obj.ondragstart = function(evt){
				evt.dataTransfer.setData("text", event.target.id);
				this.style.opacity = '0.5';
			};
			obj.ondragend = function(){
				this.style.opacity = '1.0';
			};
		},
		dragover: function(){
		},
		dragstart: function(){
		}
	}
};
web.App['analyze'] = {
	action: {
		startup: function(){
			web.json("index.cgi?app=taskcheck&key=" + web.GET['key'] + '&width=' + web.Env['canvas'].width);
		},
		click: function(id){
			web.App.audio.action.play('01_TODO_FINISH');
			web.json("index.cgi?app=taskcheck&key=" + web.GET['key'] + '&id=' + id + '&width=' + web.Env['canvas'].width);
		},
		callback: function(html,json){
			web.$('app_main_analyze_table').innerHTML = html;
			web.App.graph.render({
				target: 'graph',
				padding: 10,
				width: 50,
				height: 200,
				pointSize: 12,
				label: [],
				relative: [false,false],
				average: [true,true],
				color: ['#3366CC','#DC3912'],
				data: json
			});
		},
		error: function(){
			console.log("Callback error");
		}
	}
};
web.App['lifecycle'] = {
	Status: false,
	Date: null,
	EndDate: null,
	Handle: null,
	action: {
		init: function(){
			var wrap = document.createElement('div');
			wrap.id = 'lifecycle_wrap';
			if(web.App.lifecycle.Status){
				wrap.className = 'green';
			};
			var inner = document.createElement('div');
			inner.id = 'lifecycle_inner';
			var stat = document.createElement('div');
			stat.id = 'lifecycle_stat';
			stat.innerHTML = '-';
			inner.appendChild(stat);
			var button = document.createElement('button');
			button.id = 'lifecycle_button';
			if(web.App.lifecycle.Status){
				button.innerHTML = web.Lang.cycleEnd;
			}
			else {
				button.innerHTML = web.Lang.cycleStart;
			};
			button.onclick = function(){
				web.App.lifecycle.action.toggle();
			};
			inner.appendChild(button);
			var bar = document.createElement('div');
			bar.id = 'lifecycle_bar';
			inner.appendChild(bar);
			wrap.appendChild(inner);
			document.body.appendChild(wrap);
			if(web.App.lifecycle.Status){
				web.App.lifecycle.Handle = setTimeout(function(){
					web.App.lifecycle.action.cycle();
				},1000);
			};
		},
		toggle: function(){
			web.App.audio.action.play('07_LIFELOG');
			web.json('index.cgi?key=' + web.GET['key'] + '&app=cycle');
		},
		cycle: function(){
			if(!web.App.lifecycle.EndDate){
				var ed = new Date(((web.App.lifecycle.Date)-0)+57600000);
				var h = ed.getHours();
				var m = ed.getMinutes();
				var s = ed.getSeconds();
				web.App.lifecycle.EndDate = web.App.todo.action.digit(h) + ':' + web.App.todo.action.digit(m) + ':' + web.App.todo.action.digit(s);
			};
			clearTimeout(web.App.lifecycle.Handle);
			if(web.App.lifecycle.Status){
				var n = parseInt(((new Date())-0) / 1000);
				var s = parseInt(((web.App.lifecycle.Date)-0) / 1000);
				var t = n - s;
				var p = 100 - (t / 57600 * 100);
				p = parseInt(p * 10) / 10;
				if(p < 10){
					web.$('lifecycle_wrap').className = 'red';
				}
				else if(p < 20){
					web.$('lifecycle_wrap').className = 'orange';
				}
				else {
					web.$('lifecycle_wrap').className = 'green';
				};
				var n = web.App.todo.action.sec2date(57600-t);
				web.$('lifecycle_bar').style.width = p+'%';
				web.$('lifecycle_stat').innerHTML = ' &nbsp; [ ' + p + '% ] &nbsp; ' + n + ' &nbsp; | &nbsp; ' + web.App.lifecycle.EndDate;
				if(web.App.lifecycle.Status){
					web.App.lifecycle.Handle = setTimeout(function(){
						web.App.lifecycle.action.cycle();
					},1000);
				};
			};
		},
		callback: function(stat){
			if(stat){
				clearTimeout(web.App.lifecycle.Handle);
				web.App.lifecycle.Status = true;
				web.App.lifecycle.Date = new Date(stat);
				web.$('lifecycle_wrap').className = 'green';
				web.$('lifecycle_button').innerHTML = web.Lang.cycleEnd;
				web.App.lifecycle.action.cycle();
			}
			else {
				clearTimeout(web.App.lifecycle.Handle);
				web.App.lifecycle.Status = false;
				web.App.lifecycle.Date = null;
				web.$('lifecycle_wrap').className = '';
				web.$('lifecycle_button').innerHTML = web.Lang.cycleStart;
				web.$('lifecycle_bar').style.width = '100%';
				web.$('lifecycle_stat').innerHTML = '-';
			};
		}
	}
};
web.add('ready',function(){
	web.App.lifecycle.action.init();
});
web.App['logs'] = {
	Status: false,
	Todo: false,
	Submit: null,
	Index: 0,
	action: {
		startup: function(){
			setTimeout(function(){
				if(!web.App.search.Stat){
					web.$('app_main_logs_input').focus();
				};
				web.App.logs.action.today();
			},100);
		},
		today: function(){
			setTimeout(function(){
				var date = new Date();
				var today = web.App.string.action.date(date.getFullYear(),date.getMonth() + 1,date.getDate());
				if(web.$('wrap_'+today)){
					var top = web.$('app_main_logs_timeline').scrollTop + web.$('wrap_'+today).getBoundingClientRect().top - web.$('app_main_logs_timeline').getBoundingClientRect().top - 60;
					if(top < 0){
						top = top * -1;
					};
					if(top > 200){
						web.$('app_main_logs_timeline').scrollTop = top;
					};
				};
			},100);
		},
		init: function(){
			var _ = web;
			_.$('app_main_logs_input').onkeyup = function(){
				web.App.logs.action.todo();
			};
			_.$('app_main_logs_form').onsubmit = function(){
				clearTimeout(web.App.logs.Submit);
				web.App.logs.Submit = setTimeout(function(){
					_.$('app_main_logs_input').disabled = true;
					web.App.logs.action.submit(false);
				},200);
				return false;
			};
			_.$('app_main_logs_input').focus();
		},
		submit: function(todo){
			var _ = web;
			if(_.$('app_main_logs_input').value != ''){
				var todoval = 0;
				if(todo){
					todoval = 1;
				};
				web.App.post.action.post('logs',[
					{
						name: 'form_text',
						value: _.$('app_main_logs_input').value
					},
					{
						name: 'form_parent',
						value: web.App.explorer.Current
					},
					{
						name: 'form_todo',
						value: todoval
					}
				]);
			};
		},
		rebuild: function(json){
			web.$('app_main_logs_timeline').innerHTML = '';
			var wrap = document.createElement('div');
			wrap.id = 'app_main_logs_timeline_inner';
			var before;
			var days;
			for(var i=0;i<json.length;i++){
				var date = json[i].date.split(' ')[0];
				if(before != date){
					if(before != undefined){
						wrap.appendChild(days);
					};
					days = web.App.logs.action.parent(date);
					before = date;
				};
				days.appendChild(web.App.logs.action.child(json[i]));
			};
			if(days){
				wrap.appendChild(days);
			};
			var spacer = document.createElement('div');
			spacer.id = 'spacer';
			wrap.appendChild(spacer);
			web.$('app_main_logs_timeline').appendChild(wrap);
			web.App.logs.action.today();
		},
		show: function(){
			setTimeout(function(){
				var obj = web.$('app_main_logs_timeline_inner').getElementsByTagName('section');
				for(var i=0;i<obj.length;i++){
					obj[i].style.opacity = 1;
				};
			},50);
		},
		update: function(json){
			web.log(json,'web.App.logs.action.update');
			var todoFlag = false;
			var status = false;
			var audioType = '08_UPDATE';
			for(var i=0;i<json.length;i++){
				if(json[i].todo == 'c'){
					web.log("TODO Complete",'web.App.logs.action.update');
					var newTodo = [];
					for(var ii=0;ii<web.App.data.Todo.length;ii++){
						if(json[i].date != web.App.data.Todo[ii].id){
							newTodo.push(web.App.data.Todo[ii]);
						}
						else {
							var id = 'tr_' + json[i].date;
							if(web.$(id)){
								web.$(id).remove();
							};
							if(web.$('signal_'+json[i].date)){
								web.$('signal_'+json[i].date).className = 'complete';
							};
						};
					};
					web.App.data.Todo = newTodo;
				}
				else if(json[i].todo == 's'){
					var id = json[i].date;
					web.App.todo.timer[id] = parseInt(json[i].parent);
					if(web.$('timer_'+id)){
						audioType = null;
						web.App.todo.action.timerStart(id);
						clearInterval(web.App.todo.timerHandle[id]);
						web.App.todo.timerHandle[id] = setInterval(function(){
							web.App.todo.timer[id]++;
							if(web.$('timer_'+id)){
								web.$('timer_'+id).innerHTML = web.App.todo.action.sec2date(web.App.todo.timer[id]);
							};
						},1000);
					};
				}
				else if(json[i].todo == 'e'){
					var id = json[i].date;
					if(web.$('timer_'+id)){
						audioType = '04_TIMER_END';
						web.App.todo.action.timerStop(id);
						web.$('timer_'+id).innerHTML = web.App.todo.action.sec2date(parseInt(json[i].parent));
						clearInterval(web.App.todo.timerHandle[id]);
					};
				}
				else if(json[i].parent == web.App.explorer.Current || web.App.explorer.Current == 'root'){
					if(json[i].todo == '1'){
						web.App.data.Todo.push(json[i]);
						web.log("todo add");
						todoFlag = true;
						web.$('app_main_logs_todo_list').insertBefore(web.App.todo.action.tr(json[i]), web.$('app_main_logs_todo_list').firstChild);
					};
					var date = json[i].date.split(' ')[0];
					var parent = 'wrap_' + date;
					if(!document.getElementById(parent)){
						var div = web.App.logs.action.parent(date);
						var obj = web.byClassName(web.$('app_main_logs_timeline_inner'),'date_wrap');
						var flag = true;
						for(var ii=0;ii<obj.length;ii++){
							if(obj[ii].id < parent){
								web.$('app_main_logs_timeline_inner').insertBefore(div, obj[ii]);
								flag = false;
								break;
							};
						};
						if(flag){
							web.$('app_main_logs_timeline_inner').insertBefore(div, web.$('spacer'));
						};
					};
					var obj = document.getElementById(parent).getElementsByTagName('section');
					var child = web.App.logs.action.child(json[i]);
					child.style.opacity = 0;
					var flag = true;
					for(var ii=0;ii<obj.length;ii++){
						if(obj[ii].getAttribute('data-date') <= json[i].date){
							obj[ii].parentNode.insertBefore(child, obj[ii]);
							flag = false;
							break;
						};
					};
					if(flag){
						document.getElementById(parent).appendChild(child);
					};
				}
				else {
					status = true;
				};
			};
			if(audioType){
				web.App.audio.action.play(audioType);
			};
			web.App.logs.action.show();
			web.App.logs.action.today();
			if(todoFlag){
				web.App.calendar.action.update(web.App.data.Todo);
			};
		},
		parent: function(date){
			var div = document.createElement('div');
			div.id = 'wrap_'+date;
			div.className = 'date_wrap';
			var h3 = document.createElement('h3');
			var span = document.createElement('span');
			span.innerHTML = date.replace(/\-/ig,'/');
			h3.appendChild(span);
			div.appendChild(h3);
			return div;
		},
		child: function(json){
			var section = document.createElement('section');
			section.setAttribute('data-date',json.date);
			var className = 'other';
			if(json.user == web.App.Id){
				className = 'my';
			};
			section.className = className;
			var h4 = document.createElement('h4');
			var em = document.createElement('em');
			em.id = 'signal_' + json.id;
			if(json.complete == 1){
				em.className = 'complete';
			}
			else if(json.todo == '1'){
				em.className = 'todo';
			};
			web.log(json,'child');
			h4.appendChild(em);
			var span = document.createElement('span');
			span.setAttribute('data-time',json.date);
			span.className = 'timeago';
			h4.appendChild(span);
			section.appendChild(h4);
			var img = document.createElement('img');
			if(json.picture){
				img.src = json.picture;
			}
			else {
				img.src = 'inc/_images/blank.png';
			};
			section.appendChild(img);
			var div = document.createElement('div');
			var p = document.createElement('p');
			p.innerHTML = json.text;
			div.appendChild(p);
			var ul = document.createElement('ul');
			var li = document.createElement('li');
			div.appendChild(ul);
			section.appendChild(div);
			return section;
		},
		gettime: function(date){
			return (new Date(date)).getTime();
		},
		todo: function(){
			var _ = web;
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt.key == 'Enter' && evt.shiftKey){
				_.$('app_main_logs_input').disabled = true;
				clearTimeout(web.App.logs.Submit);
				web.App.logs.action.submit(true);
			};
		},
		done: function(){
		},
		callback: function(){
			web.App.post.action.reset();
			web.$('app_main_logs_input').disabled = false;
			web.$('app_main_logs_input').value = '';
			web.$('app_main_logs_input').focus();
		}
	}
};
web.add('ready',function(){
	web.App.logs.action.init();
});
web.App['calendar'] = {
	Event: {},
	Today: {
		Date: null,
		Year: null,
		Month: null,
		Day: null
	},
	Current: null,
	action: {
		init: function(){
			var _ = web;
			_.App.calendar.action.preset();
			_.$('app_main_logs_calendar_prev').onclick = function(){
				_.App.calendar.action.move(-1);
			};
			_.$('app_main_logs_calendar_next').onclick = function(){
				_.App.calendar.action.move(1);
			};
		},
		preset: function(){
			var _ = web;
			_.App.calendar.Today.Date = new Date();
			_.App.calendar.Today.Year = _.App.calendar.Today.Date.getFullYear();
			_.App.calendar.Today.Month = _.App.calendar.Today.Date.getMonth() + 1;
			_.App.calendar.Today.Day = _.App.calendar.Today.Date.getDate();
			_.App.calendar.Today.Date = new Date(_.App.calendar.Today.Year+'/'+_.App.calendar.Today.Month+'/'+_.App.calendar.Today.Day+' 00:00:00');
			_.App.calendar.Current = new Date(_.App.calendar.Today.Year+'/'+_.App.calendar.Today.Month+'/1 00:00:00');
		},
		move: function(m){
			var _ = web;
			var day = _.App.calendar.Current.getDate();
			var month = _.App.calendar.Current.getMonth() + 1;
			var year = _.App.calendar.Current.getFullYear();
			month += m;
			if(month > 12){
				month = 1;
				year++;
			}
			else if(month < 1){
				month = 12;
				year--;
			};
			_.App.calendar.Current = new Date(year+'/'+month+'/1 00:00:00');
			_.App.calendar.action.rebuild();
		},
		update: function(todo){
			web.App.calendar.Event = {};
			for(var i=0;i<todo.length;i++){
				var date = todo[i].date.split(' ')[0];
				if(!web.App.calendar.Event[date]){
					web.App.calendar.Event[date] = todo[i].text;
				}
				else {
					web.App.calendar.Event[date] += '<br>' + todo[i].text;
				};
			};
			web.App.calendar.action.preset();
			web.App.calendar.action.rebuild();
		},
		rebuild: function(){
			var _ = web;
			var day = _.App.calendar.Current.getDate();
			var month = _.App.calendar.Current.getMonth() + 1;
			var year = _.App.calendar.Current.getFullYear();
			var week = _.App.calendar.Current.getDay();
			var className = new Array("sun","mon","tue","wed","thu","fri","sat");
			var weekName = web.Lang.calendarWeek.split(',');
			var monthName = web.Lang.calendarMonth.split(',');
			var days = new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
			_.$('app_main_logs_calendar_main').innerHTML = '';
			var str = web.Lang.calendarFormat;
			str = str.replace('$year',year);
			_.$('app_main_logs_calendar_h').innerHTML = str.replace('$month',monthName[month-1]);
			if(month == 2){
				if(year % 100 == 0 || year % 4 != 0){
					if(year % 400 == 0){
						days[2]++;
					}
				}
				else if(year % 4 == 0) {
					days[2]++;
				};
			};
			var table = document.createElement('table');
			var tr = document.createElement('tr');
			for(var i=0;i<weekName.length;i++){
				var td = document.createElement('td');
				td.innerHTML = weekName[i];
				td.className = className[i];
				tr.appendChild(td);
			};
			table.appendChild(tr);
			tr = document.createElement('tr');
			for(var i=week-1;i>=0;i--){
				var td = document.createElement('td');
				td.innerHTML = '&nbsp;';
				tr.appendChild(td);
			};
			for(var i=1;i<=days[month];i++){
				var str = web.App.string.action.date(year,month,i);
				var date = new Date(year+'/'+month+'/'+i+' 00:00:00');
				var td = document.createElement('td');
				var div = document.createElement('div');
				var className = [];
				div.innerHTML = i;
				div.setAttribute('data-day',month+'/'+i);
				div.onclick = function(){
					web.$('app_main_logs_input').value = this.getAttribute('data-day') + ' ' + web.$('app_main_logs_input').value;
					web.$('app_main_logs_input').focus();
				};
				if(date.getTime() < _.App.calendar.Today.Date.getTime()){
					className.push('backward');
				};
				if(web.App.calendar.Event[str]){
					className.push('event');
					var span = document.createElement('span');
					span.innerHTML = web.App.calendar.Event[str];
					div.appendChild(span);
				};
				div.className = className.join(' ');
				td.className = className[week];
				td.appendChild(div);
				tr.appendChild(td);
				if(week == 6){
					table.appendChild(tr);
					if(i < days[month]){
						tr = document.createElement('tr');
					};
					week = 0;
				}
				else {
					week++;
				};
			};
			while(week <= 6 && week != 0){
				var td = document.createElement('td');
				td.innerHTML = '&nbsp;';
				tr.appendChild(td);
				if(week == 6){
					table.appendChild(tr);
				};
				week++;
			};
			_.$('app_main_logs_calendar_main').appendChild(table);
		}
	}
};
web.add('ready',function(){
	web.App.calendar.action.init();
});
web.App['todo'] = {
	timer: [],
	timerHandle: [],
	categories: [],
	group: [],
	groupIndex: [],
	current: null,
	action: {
		init: function(){
		},
		digit: function(str){
			if(str < 10){
				return '0'+str;
			}
			else {
				return str;
			};
		},
		sec2date: function(n){
			var minus = '';
			if(n < 0){
				n *= -1;
				minus = '-';
			};
			var _ = web.App.todo.action;
			var h = _.digit(parseInt(n / 3600));
			var m = _.digit(parseInt(n / 60) % 60);
			var s = _.digit(parseInt(n % 60));
			return minus + h + ':' + m + ':' + s;
		},
		qtyChg: function(id,qty){
			if(web.$('group_'+id+'_qty')){
				var num = parseInt(web.$('group_'+id+'_qty').innerHTML);
				num += qty;
				if(num < 1){
				}
				else {
					web.$('group_'+id+'_qty').innerHTML = num;
				};
			};
		},
		dragTodo: function(from,to){
			web.json('index.cgi?key=' + web.GET['key'] + '&app=dragTodo&from=' + from + '&to=' + to);
		},
		dragTodoCallback: function(id,parentName,parentId){
			if(web.$('todo_'+id)){
				if(web.$('todo_parent_'+id)){
					web.$('todo_parent_'+id).innerHTML = parentName;
				}
				else {
					var span = document.createElement('span');
					span.id = 'todo_parent_' + id;
					span.className = 'parent';
					span.innerHTML = parentName;
					if(web.$('todo_'+id)){
						web.$('todo_'+id).insertBefore(span, web.$('todo_'+id).firstChild);
					};
				};
				web.$('todo_parent_'+id).parentNode.parentNode.parentNode.setAttribute('data-parent',parentId);
				if(!web.$('group_'+parentId+'_tr')){
					web.$('app_main_logs_todo_list').insertBefore(web.App.todo.action.th(parentId,parentName,0),web.$('app_main_logs_todo_list').firstChild);
				};
				if(web.$('group_'+parentId+'_tr')){
					web.$('group_'+parentId+'_tr').parentNode.insertBefore(
						web.$('todo_parent_'+id).parentNode.parentNode.parentNode.parentNode.removeChild(web.$('todo_parent_'+id).parentNode.parentNode.parentNode),
						web.$('group_'+parentId+'_tr').nextSibling);
					web.App.todo.action.qtyChg(parentId,1);
				};
				if(web.App.todo.current != 'group_'+parentId){
					setTimeout(function(){
						web.App.todo.action.folder(web.$('group_'+parentId));
					},50);
				}
				else {
					setTimeout(function(){
						web.App.todo.action.folder(web.$('group_'+parentId));
						setTimeout(function(){
							web.App.todo.action.folder(web.$('group_'+parentId));
						},50);
					},50);
				};
			};
		},
		complete: function(obj){
			obj.disabled = true;
			web.json('index.cgi?key=' + web.GET['key'] + '&app=complete&id=' + obj.getAttribute('data-id'));
		},
		timer: function(obj){
			web.json('index.cgi?key=' + web.GET['key'] + '&app=timer&id=' + obj.getAttribute('data-id'));
		},
		callback: function(text){
			web.log("callback"+text);
		},
		timerCallback: function(sw,id,time){
			if(sw){
				web.App.todo.timer[id] = time;
				if(web.$('timer_'+id)){
					web.App.todo.action.timerStart(id);
					clearInterval(web.App.todo.timerHandle[id]);
					web.App.todo.timerHandle[id] = setInterval(function(){
						web.App.todo.timer[id]++;
						if(web.$('timer_'+id)){
							web.$('timer_'+id).innerHTML = web.App.todo.action.sec2date(web.App.todo.timer[id]);
						};
					},1000);
				};
			}
			else {
				web.App.todo.action.timerStop(id);
				clearInterval(web.App.todo.timerHandle[id]);
			};
		},
		timerStart: function(id){
			if(web.$('timer_'+id)){
				web.$('tr_'+id).setAttribute('data-show',1);
				web.addClassName(web.$('timer_'+id),'active');
			};
		},
		timerStop: function(id){
			if(web.$('timer_'+id)){
				web.$('tr_'+id).removeAttribute('data-show');
				web.removeClassName(web.$('timer_'+id),'active');
			};
		},
		timerLoop: function(id){
			clearInterval(web.App.todo.timerHandle[id]);
			if(web.$('timer_'+id)){
				web.App.todo.timerHandle[id] = setInterval(function(){
					web.App.todo.timer[id]++;
					if(web.$('timer_'+id)){
						web.$('timer_'+id).innerHTML = web.App.todo.action.sec2date(web.App.todo.timer[id]);
					};
				},1000);
			};
		},
		show: function(id){
			var tr = web.$('app_main_logs_todo_list').getElementsByTagName("tr");
			for(var i=0;i<tr.length;i++){
				if(tr[i].getAttribute('data-parent') == id){
					web.addClassName(tr[i],'open');
				};
				if(tr[i].getAttribute('data-parent') == id || tr[i].getAttribute('data-show') || tr[i].getAttribute('data-today-show')){
					tr[i].style.display = 'table-row';
				};
			};
		},
		hide: function(id){
			var tr = web.$('app_main_logs_todo_list').getElementsByTagName("tr");
			for(var i=0;i<tr.length;i++){
				if(tr[i].getAttribute('data-parent') == id && !tr[i].getAttribute('data-show') && !tr[i].getAttribute('data-today-show')){
					tr[i].style.display = 'none';
				};
				if(tr[i].getAttribute('data-parent') == id){
					web.removeClassName(tr[i],'open');
				};
			};
		},
		rebuild: function(todo){
			todo.sort(function(a,b){
				if(b.date < a.date) return -1;
				if(b.date > a.date) return 1;
				return 0;
			});
			var _ = web;
			web.log(todo);
			_.$('app_main_logs_todo').innerHTML = '';
			var table = document.createElement('table');
			table.className = 'app_main_logs_todo_list';
			table.id = 'app_main_logs_todo_list';
			web.App.todo.group = [];
			web.App.todo.groupIndex = [];
			web.App.todo.categories = [];
			if(web.App.explorer.Current == 'root'){
				for(var i=0;i<todo.length;i++){
					if(todo[i].parentName){
						if(!web.App.todo.categories[todo[i].parentId]){
							web.App.todo.categories[todo[i].parentId] = [];
							web.App.todo.categories[todo[i].parentId].qty = 0;
							web.App.todo.categories[todo[i].parentId].id = todo[i].parentId;
							web.App.todo.categories[todo[i].parentId].name = todo[i].parentName;
							web.App.todo.categories[todo[i].parentId].node = [];
						};
						web.App.todo.categories[todo[i].parentId].node.push(todo[i]);
						web.App.todo.categories[todo[i].parentId].qty++;
					}
					else {
						table.appendChild(_.App.todo.action.tr(todo[i]));
					};
				};
				for(var prop in web.App.todo.categories){
					var t = web.App.todo.categories[prop];
					table.appendChild(_.App.todo.action.th(t.id,t.name,t.qty));
					for(var i=0;i<t.node.length;i++){
						table.appendChild(_.App.todo.action.tr(t.node[i]));
					};
				};
			}
			else {
				var tr = document.createElement('tr');
				var th = document.createElement('th');
				th.onclick = function(evt){
					web.App.explorer.action.cd('root');
					web.App.audio.action.play('06_FOLDER');
					evt.preventDefault();
				};
				th.oncontextmenu = function(evt){
					web.App.explorer.action.cd('root');
					web.App.audio.action.play('06_FOLDER');
					evt.preventDefault();
				};
				th.setAttribute('colspan',3);
				th.className = 'back';
				tr.appendChild(th);
				table.appendChild(tr);
				for(var i=0;i<todo.length;i++){
					table.appendChild(_.App.todo.action.tr(todo[i]));
				};
			};
			_.$('app_main_logs_todo').appendChild(table);
		},
		th: function(id,name,qty){
			var tr = document.createElement('tr');
			tr.id = 'group_' + id + '_tr';
			var th = document.createElement('th');
			th.oncontextmenu = function(evt){
				web.App.audio.action.play('06_FOLDER');
				web.App.explorer.action.cd(this.getAttribute('data-group-id'));
				evt.preventDefault();
			};
			th.setAttribute('colspan',3);
			th.setAttribute('data-group-id',id);
			th.id = 'group_' + id;
			th.innerHTML = name;
			var em = document.createElement('em');
			em.id = 'group_' + id + '_qty';
			em.innerHTML = qty;
			th.appendChild(em);
			th.setAttribute('data-dir-drag',id);
			web.App.draganddrop.action.setDrop(th);
			th.onclick = function(){
				web.App.audio.action.play('05_TIMER_START');
				web.App.todo.action.folder(this);
			};
			tr.appendChild(th);
			return tr;
		},
		folder: function(obj){
			if(obj.getAttribute('data-status') == 'open'){
				obj.setAttribute('data-status','close');
				obj.className = '';
				web.App.todo.action.hide(obj.getAttribute('data-group-id'));
				web.App.todo.current = null;
			}
			else {
				obj.setAttribute('data-status','open');
				obj.className = 'open';
				web.App.todo.action.show(obj.getAttribute('data-group-id'));
				if(web.App.todo.current != obj.id && web.App.todo.current){
					web.$(web.App.todo.current).setAttribute('data-status','close');
					web.$(web.App.todo.current).className = '';
					web.App.todo.action.hide(web.$(web.App.todo.current).getAttribute('data-group-id'));
				};
				web.App.todo.current = obj.id;
			};
		},
		tr: function(todo){
			var tr = document.createElement('tr');
			tr.setAttribute('id','tr_' + todo.id);
			tr.setAttribute('data-todo-id',todo.id);
			tr.setAttribute('data-todo-text',todo.text);
			var t = parseInt((((new Date())-0) - ((new Date(todo.date))-0)) / 1000);
			var minus = false;
			if(t < 0){
				t = t * -1;
				minus = true;
			};
			if(t < 86400 && minus){
				tr.setAttribute('data-today-show',1);
			};
			tr.oncontextmenu = function(){
				console.log(this.getAttribute('data-todo-id'));
				console.log(this.getAttribute('data-todo-text'));
				return false;
			};
			(function(){
				var td = document.createElement('td');
				td.setAttribute('valign','top');
				(function(){
					var span = document.createElement('span');
					web.App.todo.timer[todo.id] = todo.worktime;
					span.innerHTML = web.App.todo.action.sec2date(todo.worktime);
					span.className = 'timer';
					span.setAttribute('data-id',todo.id);
					span.id = 'timer_' + todo.id;
					span.onclick = function(){
						web.App.audio.action.play('05_TIMER_START');
						web.App.todo.action.timer(this);
					};
					if(todo.timer){
						tr.setAttribute('data-show',1);
						web.App.todo.timer[todo.id] += todo.time;
						setTimeout(function(){
							web.App.todo.action.timerStart(todo.id);
							web.App.todo.action.timerLoop(todo.id);
						},1000);
					};
					td.appendChild(span);
				})();
				(function(){
					var span = document.createElement('span');
					span.className = 'timeago';
					span.innerHTML = '-';
					span.setAttribute('data-time',todo.date);
					td.appendChild(span);
				})();
				tr.appendChild(td);
			})();
			(function(){
				var td = document.createElement('td');
				td.setAttribute('valign','top');
				var input = document.createElement('input');
				input.type = 'checkbox';
				input.id = todo.id + '_checkbox';
				input.setAttribute('data-id',todo.id);
				input.onclick = function(){
					web.App.audio.action.play('01_TODO_FINISH');
					web.App.todo.action.complete(this);
					web.App.todo.action.qtyChg(this.parentNode.parentNode.getAttribute('data-parent'),-1);
					this.parentNode.parentNode.remove();
				};
				td.appendChild(input);
				tr.appendChild(td);
			})();
			(function(){
				var td = document.createElement('td');
				td.setAttribute('valign','top');
				var label = document.createElement('label');
				label.id = 'todo_' + todo.id;
				label.setAttribute('data-todo-drag',todo.id);
				label.setAttribute('data-parent',todo.parentId);
				web.App.draganddrop.action.setDrag(label);
				label.for = todo.id + '_checkbox';
				label.setAttribute('for',todo.id + '_checkbox');
				if(todo.parentName){
					if(web.App.explorer.Current == 'root'){
						tr.setAttribute('data-parent',todo.parentId);
						if(!tr.getAttribute('data-show') && !tr.getAttribute('data-today-show')){
							tr.style.display = 'none';
						};
					};
					label.oncontextmenu = function(evt){
						web.App.explorer.action.cd(this.getAttribute('data-parent'));
						evt.preventDefault();
					};
					var span = document.createElement('span');
					span.id = 'todo_parent_' + todo.id;
					span.className = 'parent';
					span.innerHTML = todo.parentName;
					label.appendChild(span);
				};
				var strong = document.createElement('strong');
				strong.innerHTML = todo.text;
				label.appendChild(strong);
				td.appendChild(label);
				tr.appendChild(td);
			})();
			return tr;
		}
	}
};
web.add('ready',function(){
	web.App.todo.action.init();
});
web.App['note'] = {
	Status: false,
	CurrentId: "",
	CurrentWorktime: 0,
	TimerInterval: null,
	tool: {
		sbtoggle: false
	},
	Before: ['ｶﾞ','ｷﾞ','ｸﾞ','ｹﾞ','ｺﾞ','ｻﾞ','ｼﾞ','ｽﾞ','ｾﾞ','ｿﾞ','ﾀﾞ','ﾁﾞ','ﾂﾞ','ﾃﾞ','ﾄﾞ','ﾊﾞ','ﾋﾞ','ﾌﾞ','ﾍﾞ','ﾎﾞ','ﾊﾟ','ﾋﾟ','ﾌﾟ','ﾍﾟ','ﾎﾟ','ｦ','ｧ','ｨ','ｩ','ｪ','ｫ','ｬ','ｭ','ｮ','ｯ','ｰ','ｱ','ｲ','ｳ','ｴ','ｵ','ｶ','ｷ','ｸ','ｹ','ｺ','ｻ','ｼ','ｽ','ｾ','ｿ','ﾀ','ﾁ','ﾂ','ﾃ','ﾄ','ﾅ','ﾆ','ﾇ','ﾈ','ﾉ','ﾊ','ﾋ','ﾌ','ﾍ','ﾎ','ﾏ','ﾐ','ﾑ','ﾒ','ﾓ','ﾔ','ﾕ','ﾖ','ﾗ','ﾘ','ﾙ','ﾚ','ﾛ','ﾜ','ﾝ','Ａ','Ｂ','Ｃ','Ｄ','Ｅ','Ｆ','Ｇ','Ｈ','Ｉ','Ｊ','Ｋ','Ｌ','Ｍ','Ｎ','Ｏ','Ｐ','Ｑ','Ｒ','Ｓ','Ｔ','Ｕ','Ｖ','Ｗ','Ｘ','Ｙ','Ｚ','ａ','ｂ','ｃ','ｄ','ｅ','ｆ','ｇ','ｈ','ｉ','ｊ','ｋ','ｌ','ｍ','ｎ','ｏ','ｐ','ｑ','ｒ','ｓ','ｔ','ｕ','ｖ','ｗ','ｘ','ｙ','ｚ','＠','０','１','２','３','４','５','６','７','８','９','．','－','〜','｢','｣'],
	After: ['ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ','ヲ','ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ','ッ','ー','ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ン','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','@','0','1','2','3','4','5','6','7','8','9','.','-','～','「','」'],
	action: {
		tool: {
			pw: function(){
				var passwords = [];
				(function(){
					var chars = "acefghikmnstwx";
					var chars_length = chars.length - 1;
					var passwd = "";
					for(var i=0;i<4;i++){
						var key = Math.floor(Math.random() * chars.length);
						passwd += chars.substring(key,key+1);
					};
					passwords.push(passwd);
				})();
				(function(){
					var chars = "ABCDEFGHJKLMNPQRSTUVWXYZ";
					var chars_length = chars.length - 1;
					var passwd = "";
					for(var i=0;i<4;i++){
						var key = Math.floor(Math.random() * chars.length);
						passwd += chars.substring(key,key+1);
					};
					passwords.push(passwd);
				})();
				(function(){
					var chars = "23456789";
					var chars_length = chars.length - 1;
					var passwd = "";
					for(var i=0;i<4;i++){
						var key = Math.floor(Math.random() * chars.length);
						passwd += chars.substring(key,key+1);
					};
					passwords.push(passwd);
				})();
				for(var i=0;i<10;i++){
					var n1 = Math.floor(Math.random() * passwords.length);
					var n2 = Math.floor(Math.random() * passwords.length);
					var m = passwords[n1];
					passwords[n1] = passwords[n2];
					passwords[n2] = m;
				};
				web.$('app_note').value += passwords.join('-') + "\n";
			},
			sb: function(){
				if(web.App.note.tool.sbtoggle){
					web.$('app_note').value = web.$('app_note').value.toUpperCase();
					web.App.note.tool.sbtoggle = false;
				}
				else {
					web.$('app_note').value = web.$('app_note').value.toLowerCase();
					web.App.note.tool.sbtoggle = true;
				};
			},
			li: function(){
				var _ = web;
				var list = [];
				list = _.$('app_note').value.split("\n");
				if(_.$('app_note').value.indexOf('<li>') == -1){
					_.$('app_note').value = "<ul>\n<li>" + list.join("</li>\n<li>") + "</li>\n</ul>";
					_.$('app_note').select();
				}
				else {
					_.$('app_note').value = _.$('app_note').value.replace(/<li>/ig,"<li><a href=\"\">");
					_.$('app_note').value = _.$('app_note').value.replace(/<\/li>/ig,"</a></li>");
				};
			},
			lv: function(){
				var _ = web;
				var list = [];
				var result = "";
				list = _.$('app_note').value.split("\n");
				if(_.$('app_note').value.indexOf('<input') == -1){
					for(var i=0;i<list.length;i++){
						var val = list[i].replace("\r","");
						result += '<label><input type="radio" name="elementsname" value="'+val+'">'+val+'</label>'+"\n";
					};
					_.$('app_note').value = result;
					_.$('app_note').select();
				}
				else if(_.$('app_note').value.indexOf('"radio"') > -1){
					_.$('app_note').value = _.$('app_note').value.replace(/radio/ig,"checkbox");
				}
				else {
					_.$('app_note').value = _.$('app_note').value.replace(/checkbox/ig,"radio");
				};
			},
			sl: function(){
				var _ = web;
				var list = [];
				var result = "";
				list = _.$('app_note').value.split("\n");
				if(_.$('app_note').value.indexOf('<option') == -1){
					for(var i=0;i<list.length;i++){
						var val = list[i].replace("\r","");
						if(val != ''){
							result += '<option value="'+val+'">'+val+'</option>'+"\n";
						};
					};
					_.$('app_note').value = result;
					_.$('app_note').select();
				};
			}
		},
		startup: function(){
			setTimeout(function(){
				if(!web.App.search.Stat){
					web.$('app_note').focus();
				};
			},500);
		},
		date : function(){
			var d = window.document;
			var myDate = new Date();
			var year = myDate.getYear();
			var mon = myDate.getMonth()+1;
			if(mon < 10) mon = "0"+mon;
			var day = myDate.getDate();
			if(day < 10) day = "0"+day;
			var hour = myDate.getHours();
			if(hour < 10) hour = "0"+hour;
			var min = myDate.getMinutes();
			if(min < 10) min = "0"+min;
			if(year < 1900) year += 1900;
			return year + "-" + mon + "-" + day + ' ' + hour + ':' + min;
		},
		init: function(){
			var _ = web;
			_.$('app_note_tool_pw').onclick = web.App.note.action.tool.pw;
			_.$('app_note_tool_sb').onclick = web.App.note.action.tool.sb;
			_.$('app_note_tool_li').onclick = web.App.note.action.tool.li;
			_.$('app_note_tool_lv').onclick = web.App.note.action.tool.lv;
			_.$('app_note_tool_sl').onclick = web.App.note.action.tool.sl;
			_.$('app_note').onkeyup = function(){
				web.App.note.action.format();
			};
			_.$('app_note').onkeydown = function(){
				web.App.note.action.tab();
			};
			_.$('app_note').onkeypress = function(){
				web.App.note.action.control();
			};
			_.$('app_note_public').onclick = function(){
				web.$('app_note').focus();
			};
			_.$('app_command_new').onclick = _.App.note.action.newpad;
			_.$('app_command_save').onclick = _.App.note.action.save;
			_.$('app_command_todo').onclick = _.App.note.action.todo;
			_.$('app_command_remove').onclick = function(){
				_.App.note.action.remove(web.App.note.CurrentId);
			};
			_.$('app_command_dl').onclick = _.App.note.action.download;
			_.$('app_note').focus();
			web.App.note.action.timer();
		},
		timer: function(){
			web.App.note.CurrentWorktime++;
			web.$('app_note_worktime').innerHTML = web.App.string.action.time(web.App.note.CurrentWorktime);
			clearTimeout(web.App.note.TimerInterval);
			web.App.note.TimerInterval = setTimeout(function(){
				web.App.note.action.timer();
			},1000);
		},
		download: function(){
			if(web.App.note.CurrentId){
				location.href = 'index.cgi?key=' + web.GET['key'] + '&app=download&id=' + web.App.note.CurrentId;
			};
		},
		remove: function(id){
			if(id){
				web.App.audio.action.play('10_REMOVE');
				web.json('index.cgi?key=' + web.GET['key'] + '&app=remove&id=' + id);
			};
		},
		removeCallback: function(list,path){
			web.App.note.action.newpad();
			web.App.explorer.action.rebuild(list,path);
			web.App.status.action.show(web.Lang.statusRemove);
		},
		newpad: function(){
			var _ = web;
			_.$('app_note').value = web.App.note.action.date();
			if(_.$(web.App.note.CurrentId)){
				_.$(web.App.note.CurrentId).className = '';
			};
			web.App.note.CurrentId = '';
			web.App.note.CurrentWorktime = 0;
			_.$('app_note_public').checked = false;
			_.$('app_note_cdate').className = '';
			_.$('app_note_cdate').innerHTML = '-';
			_.$('app_note_udate').className = '';
			_.$('app_note_udate').innerHTML = '-';
			if(!web.App.search.Stat){
				_.$('app_note').focus();
			};
			document.title = web.Title;
		},
		open: function(id){
			web.json('index.cgi?key=' + web.GET['key'] + '&app=open' + '&id=' + id);
		},
		openCallback: function(json){
			var _ = web;
			_.App.note.CurrentId = json.id;
			_.App.note.CurrentWorktime = json.worktime;
			_.$('app_note_worktime').innerHTML = web.App.string.action.time(json.worktime);
			_.$('app_note').value = _.unsanitizing(json.text);
			_.$('app_note').selectionStart = 0;
			_.$('app_note').selectionEnd = 0;
			_.$('app_note').blur();
			_.$('app_note').focus();
			_.$('app_note_cdate').setAttribute('data-time',json.createDate);
			_.$('app_note_cdate').className = 'timeago';
			_.$('app_note_udate').setAttribute('data-time',json.updateDate);
			_.$('app_note_udate').className = 'timeago';
			if(json.public){
				_.$('app_note_public').checked = true;
			}
			else {
				_.$('app_note_public').checked = false;
			};
			document.title = json.name;
		},
		todo: function(){
			var _ = web;
			if(_.$('app_note').value != ''){
				web.App.post.action.post('todo',[
					{
						name: 'form_text',
						value: _.$('app_note').value
					},
					{
						name: 'form_parent',
						value: web.App.explorer.Current
					}
				]);
			};
		},
		todoCallback: function(){
			web.App.controller.action.show('logs');
		},
		save: function(){
			var _ = web;
			if(_.$('app_note').value != ''){
				web.App.audio.action.play('11_SAVE');
				var publicStatus = 0;
				if(_.$('app_note_public').checked){
					publicStatus = 1;
				};
				web.App.post.action.post('save',[
					{
						name: 'form_id',
						value: web.App.note.CurrentId
					},
					{
						name: 'form_text',
						value: _.$('app_note').value
					},
					{
						name: 'form_parent',
						value: web.App.explorer.Current
					},
					{
						name: 'form_worktime',
						value: web.App.note.CurrentWorktime
					},
					{
						name: 'form_public',
						value: publicStatus
					}
				]);
			};
		},
		saveCallback: function(id,parent,list,path,title,date){
			web.App.post.action.reset();
			document.title = title;
			web.App.note.CurrentId = id;
			web.$('app_note_udate').setAttribute('data-time',date);
			web.App.explorer.action.rebuild(list,path);
			web.App.status.action.show(web.Lang.statusSave);
		},
		control: function(){
			var _ = web;
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt != null){
				if ((evt.ctrlKey || evt.metaKey) && evt.which == 115){
					_.App.note.action.save();
					return false;
				}
				else if((evt.ctrlKey || evt.metaKey) && evt.which == 101){
					_.App.note.action.newpad();
					return false;
				};
			};
		},
		tab: function(){
			var _ = web;
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt.ctrlKey && !evt.metaKey){
				if (evt.keyCode == 83){
					if(evt.preventDefault){
						evt.preventDefault();
					};
					_.App.note.action.save();
					return false;
				}
				else if(evt.keyCode == 69){
					if(evt.preventDefault){
						evt.preventDefault();
					};
					_.App.note.action.newpad();
					return false;
				};
			}
			else if(!evt.ctrlKey && evt.metaKey){
				if (evt.keyCode == 83){
					if(evt.preventDefault){
						evt.preventDefault();
					};
					_.App.note.action.save();
					return false;
				}
				else if(evt.keyCode == 69){
					if(evt.preventDefault){
						evt.preventDefault();
					};
					_.App.note.action.newpad();
					return false;
				};
			}
			else if(evt.keyCode === 9){
				if(evt.preventDefault){
					evt.preventDefault();
				};
				web.log("tab insert");
				var elem = evt.target;
				var start = elem.selectionStart;
				var end = elem.selectionEnd;
				var value = elem.value;
				elem.value = "" + (value.substring(0, start)) + "\t" + (value.substring(end));
				elem.selectionStart = elem.selectionEnd = start + 1;
				return false;
			};
		},
		format: function(){
			var _ = web;
			var evt = arguments.callee.caller.arguments[0] || window.event;
			if(evt.key == 'Enter' && evt.shiftKey){
				var str = _.$('app_note').value;
				str = str.replace(/　/ig,' ');
				str = str.replace(/ \n/ig,"\n");
				while(str.match(/\t\n/ig)){
					str = str.replace(/\t\n/ig,"\n");
				};
				while(str.match(/ \n/ig)){
					str = str.replace(/ \n/ig,"\n");
				};
				while(str.match(/\n /ig)){
					str = str.replace(/\n /ig,"\n");
				};
				str = str.replace(/ /ig,' ');
				while(str.match(/\n\n\n/ig)){
					str = str.replace(/\n\n\n/ig,"\n\n");
				};
				while(str.match(/\n$/ig)){
					str = str.replace(/\n$/ig,"");
				};
				while(str.match(/^\n/ig)){
					str = str.replace(/^\n/ig,"");
				};
				for(var i=0;i<_.App.note.Before.length;i++){
					str = str.replace(new RegExp(_.App.note.Before[i],'g'), _.App.note.After[i]);
				};
				_.$('app_note').value = str;
			};
		}
	}
};
web.add('ready',function(){
	web.App.note.action.init();
});
web.App['task'] = {
	Status: false,
	Qty: 0,
	init: function(){
		var div = document.createElement('div');
		div.id = 'app_task_wrapper';
		var inner = document.createElement('div');
		inner.id = 'app_task_inner';
		var close = document.createElement('span');
		close.id = 'app_task_close';
		close.innerHTML = '&times;';
		close.onclick = function(){
			web.App.task.toggle();
		};
		inner.appendChild(close);
		var h2 = document.createElement('h2');
		h2.id = 'app_task_h2';
		h2.innerHTML = '100%';
		inner.appendChild(h2);
		var list = document.createElement('div');
		list.id = 'app_task_list_wrapper';
		var ul = document.createElement('ul');
		ul.id = 'app_task_list';
		(function(){
			var li = document.createElement('li');
			var label = document.createElement('label');
			var input = document.createElement('input');
			input.type = 'checkbox';
			label.appendChild(input);
			var span = document.createElement('span');
			span.innerHTML = 'BBS Pro 2 Development';
			label.appendChild(span);
			li.appendChild(label);
			ul.appendChild(li);
		})();
		inner.appendChild(list);
		div.appendChild(inner);
		document.body.appendChild(div);
	},
	toggle: function(){
		if(web.App.task.Status){
			web.App.task.Status = false;
			web.$('app_task_wrapper').style.marginTop = '-100vh';
		}
		else {
			web.App.task.Status = true;
			web.$('app_task_wrapper').style.marginTop = '-2px';
			web.json("index.cgi?app=taskcheck&key=" + web.GET['key']);
		};
	},
	show: function(json,flag,total,day){
		web.$('app_task_list_wrapper').innerHTML = '';
		var ul = document.createElement('ul');
		ul.className = 'app_task_list';
		var max = json.length;
		var qty = 0;
		for(var i=0;i<json.length;i++){
			var tmax = parseInt(json[i].day * (json[i].wday / 7));
			console.log(tmax);
			var par = parseInt(json[i].qty / tmax * 100);
			var li = document.createElement('li');
			var label = document.createElement('label');
			var input = document.createElement('input');
			input.type = 'checkbox';
			input.setAttribute('data-id',json[i].id);
			if(json[i].status){
				label.className = 'complete';
				input.checked = true;
				input.disabled = true;
				qty++;
			};
			label.appendChild(input);
			input.onchange = function(){
				if(this.checked){
					this.disabled = true;
					web.json("index.cgi?app=taskcheck&key=" + web.GET['key'] + "&id=" + this.getAttribute('data-id'));
				};
			};
			var span = document.createElement('span');
			span.innerHTML = json[i].text;
			label.appendChild(span);
			var em = document.createElement('em');
			em.innerHTML = '( ' + json[i].qty + ' [ ' + par + '% ] / ' + json[i].day + ' days / ' + json[i].date + ' )';
			label.appendChild(em);
			li.appendChild(label);
			ul.appendChild(li);
		};
		if(qty > 0){
			web.$('app_task_h2').innerHTML = parseInt(qty / max * 100) + '%';
		}
		else {
			web.$('app_task_h2').innerHTML = '0%';
		}
		web.$('app_task_list_wrapper').appendChild(ul);
		if(flag){
			web.App.audio.action.play('01_TODO_FINISH');
		};
	},
	error: function(){
		console.log("Task check Error");
	}
};
web.add('ready',function(){
	web.App.task.init();
});
web.App['explorer'] = {
	Current: 'root',
	Parent: null,
	Click: null,
	Interval: null,
	action: {
		click: function(obj){
			var _ = web;
			clearTimeout(_.App.explorer.Interval);
			if(_.App.explorer.Click && _.App.explorer.Click == obj.id){
				web.App.explorer.action.cd(obj.id);
				_.App.explorer.Click = null;
				return;
			};
			_.App.explorer.Click = obj.id;
			_.App.explorer.Interval = setTimeout(function(){
				if(_.App.explorer.Click) {
					if(_.$(web.App.note.CurrentId)){
						_.$(web.App.note.CurrentId).className = '';
					};
					web.App.note.CurrentId = obj.id;
					obj.className = 'current';
					web.App.note.action.open(obj.id);
				};
				_.App.explorer.Click = null;
			},250);
		},
		dragNote: function(from,to){
			web.json('index.cgi?key=' + web.GET['key'] + '&app=dragNote&from=' + from + '&to=' + to);
		},
		dragNoteCallback: function(id,parent,qty){
			web.$(id).parentNode.parentNode.removeChild(web.$(id).parentNode);
			if(web.$('qty_'+parent)){
				web.$('qty_'+parent).innerHTML = qty;
			}
			else if(web.$(parent)){
				var em = document.createElement('em');
				em.id = 'qty_' + parent;
				em.innerHTML = qty;
				web.$(parent).appendChild(em);
			};
		},
		cd: function(id){
			web.json('index.cgi?key=' + web.GET['key'] + '&app=cd&id=' + id);
		},
		cdCallback: function(id,parent,list,path){
			web.App.explorer.Current = id;
			web.App.explorer.Parent = parent;
			web.App.explorer.action.rebuild(list,path);
			web.App.note.action.newpad();
			web.App.controller.action.initialize();
		},
		path: function(path){
			var _ = web;
			_.$('nav_path').innerHTML = "";
			var ul = document.createElement('ul');
			for(var i=0;i<path.length;i++){
				var li = document.createElement('li');
				var span = document.createElement('span');
				span.innerHTML = path[i].name;
				span.setAttribute('data-id',path[i].id);
				span.onclick = function(){
					web.App.explorer.action.cd(this.getAttribute('data-id'));
				};
				li.appendChild(span);
				ul.appendChild(li);
			};
			_.$('nav_path').appendChild(ul);
		},
		rebuild: function(list,path){
			var _ = web;
			_.App.explorer.action.path(path);
			_.$('directories').innerHTML = "";
			if(_.App.explorer.Current != 'root'){
				var li = document.createElement('li');
				var span = document.createElement('span');
				span.setAttribute('data-dir-drag',web.App.explorer.Parent);
				web.App.draganddrop.action.setDrop(span);
				span.id = web.App.explorer.Parent;
				span.onclick = function(){
					web.App.explorer.action.cd(this.id);
					web.App.audio.action.play('05_TIMER_START');
				};
				span.innerHTML = '../';
				li.appendChild(span);
				_.$('directories').appendChild(li);
			};
			for(var i=0;i<list.length;i++){
				var li = document.createElement('li');
				li.className = 's1';
				li.setAttribute('data-id',list[i].id);
				if(i % 2 == 0){
					li.className = 's2';
				};
				var span = document.createElement('span');
				span.setAttribute('data-dir-drag',list[i].id);
				web.App.draganddrop.action.setDrop(span);
				web.App.draganddrop.action.setDrag(span);
				span.id = list[i].id;
				if(list[i].id == web.App.note.CurrentId){
					span.className = 'current';
				};
				span.innerHTML = list[i].name;
				span.oncontextmenu = function(){
					if(confirm('Remove OK ?')){
						_.App.note.action.remove(this.id);
						web.App.audio.action.play('10_REMOVE');
					};
					return false;
				};
				span.onclick = function(){
					web.App.audio.action.play('05_TIMER_START');
					if(this.id == web.App.note.CurrentId){
						web.App.explorer.action.cd(this.id);
					}
					else {
						if(_.$(web.App.note.CurrentId)){
							_.$(web.App.note.CurrentId).className = '';
						};
						web.App.note.CurrentId = this.id;
						this.className = 'current';
						web.App.note.action.open(this.id);
					};
				};
				if(list[i].qty > 0){
					var em = document.createElement('em');
					em.id = 'qty_' + list[i].id;
					em.innerHTML = list[i].qty;
					span.appendChild(em);
				};
				li.appendChild(span);
				_.$('directories').appendChild(li);
			};
		}
	}
};
web.add('ready',function(){
	web.App['post'] = {
		Status: false,
		action: {
			reset: function(){
				var _ = web;
				var elm = _.$('postform').getElementsByTagName('input');
				for(var i=0;i<elm.length;i++){
					elm[i].value = '';
				};
			},
			post: function(app,json){
				var _ = web;
				for(var i=0;i<json.length;i++){
					_.$(json[i].name).value = json[i].value;
				};
				_.$('postform').action = 'index.cgi?key=' + _.GET['key'] + '&app=' + app;
				_.$('postform').submit();
			}
		}
	};
});
web.App.graph = {
	render: function(c){
			var target = document.getElementById(c.target);
			target.style.background = '#FFF';
			var prefix = c.target + '_';
			var childs = target.getElementsByTagName('*');
			for(var i=0;i<childs.length;i++){
				childs[i].parentNode.removeChild(childs[i]);
			};
			target.style.width = c.width * c.data.length + 'px';
			target.style.height = c.height + 'px';
			target.style.position = 'relative';
			var canvas = document.createElement('canvas');
			canvas.id = prefix + 'canvas';
			canvas.width = c.width * c.data.length;
			canvas.height = c.height;
			target.appendChild(canvas);
			var cvs = document.getElementById(prefix + 'canvas');
			var ctx = cvs.getContext('2d');
			var label = [];
			var maxArr = [];
			var arch = [];
			for(var i=0;i<c.data.length;i++){
				label.push(c.data[i].shift());
				maxArr = maxArr.concat(c.data[i]);
				for(var ii=0;ii<c.data[i].length;ii++){
					if(!arch[ii]){
						arch[ii] = [];
						arch[ii].data = [];
						arch[ii].sum = 0;
						arch[ii].min = 0;
						arch[ii].max = 0;
						arch[ii].avg = 0;
						arch[ii].par = 0;
					};
					arch[ii].sum += c.data[i][ii];
					arch[ii].data.push(c.data[i][ii]);
				};
			};
			for(var ii=0;ii<c.data[0].length;ii++){
				arch[ii].min = arch[ii].data.reduce(function(a, b) {
					return Math.min(a, b);
				});
				arch[ii].max = arch[ii].data.reduce(function(a, b) {
					return Math.max(a, b);
				});
				arch[ii].avg = arch[ii].sum / arch[ii].data.length;
			};
			var max = maxArr.reduce(function(a, b) {
				return Math.max(a, b);
			});
			var digit = 10**String(parseInt(max)).length / 10;
			max += digit - (max % digit);
			for(var i=0;i<c.relative.length;i++){
				if(c.relative[i]){
					arch[i].par = (c.height - c.padding * 2 ) / arch[i].max;
				}
				else {
					arch[i].max = max;
					arch[i].par = (c.height - c.padding * 2 ) / max;
				};
			};
			var par = (c.height - c.padding * 2 ) / max;
			var points = [];
			var ajust = c.pointSize / 2;
			var i = digit;
			while(i <= (max+c.padding*2)){
				ctx.beginPath();
				ctx.lineWidth = 1;
				ctx.strokeStyle = '#EEE';
				ctx.moveTo(0,i*par+c.padding);
				ctx.lineTo(cvs.width,i*par+c.padding);
				ctx.stroke();
				if(max - i > 0){
					var span = document.createElement('span');
					span.style.position = 'absolute';
					span.style.top = (i*par+c.padding) + 'px';
					span.innerHTML = max - i;
					span.style.right = '100%';
					span.style.fontSize = '10px';
					span.style.border = 'none';
					span.style.background = 'none';
					span.style.padding = '0';
					span.style.color = '#999';
					span.style.textAlign = 'right';
					target.appendChild(span);
				};
				i += digit;
			};
			var i = 0;
			while(i <= c.width * c.data.length){
				ctx.beginPath();
				ctx.lineWidth = 0.3;
				ctx.strokeStyle = '#333';
				ctx.moveTo(i*c.width,0);
				ctx.lineTo(i*c.width,c.height-c.padding);
				ctx.stroke();
				i++;
			};
			for(var i=0;i<c.average.length;i++){
				if(c.average[i] && arch[i].avg){
					ctx.beginPath();
					ctx.lineWidth = 1;
					ctx.strokeStyle = c.color[i];
					var y = ((arch[i].max - arch[i].avg) * arch[i].par) + c.padding;
					ctx.moveTo(0,y);
					ctx.lineTo(c.width*c.data.length,y);
					ctx.stroke();
				};
			};
			for(var i=0;i<c.data.length;i++){
				for(var ii=c.data[i].length-1;ii>=0;ii--){
					if(!points[ii]){
						points[ii] = [];
					};
					if(!points[ii][i]){
						points[ii][i] = [];
					};
					var span = document.createElement('span');
					span.style.display = 'block';
					span.style.boxSizing = 'border-box';
					span.style.width = c.pointSize + 'px';
					span.style.height = c.pointSize + 'px';
					span.style.borderRadius = c.pointSize+'0px';
					span.style.border = 'solid 2px #FFF';
					span.style.position = 'absolute';
					span.style.margin = 0;
					span.setAttribute('data-id',prefix + i + '-' + ii);
					span.onmouseover = function(){
						document.getElementById(this.getAttribute('data-id')).style.display = 'inline-block';
					};
					span.onmouseout = function(){
						document.getElementById(this.getAttribute('data-id')).style.display = 'none';
					};
					var em = document.createElement('em');
					em.id = prefix + i + '-' + ii;
					em.style.width = 'auto';
					em.style.display = 'none';
					em.style.border = 'solid 2px #FFF';
					em.style.borderRadius = '5px';
					em.style.position = 'absolute';
					em.style.margin = 0;
					em.style.background = 'rgba(0,0,0,0.6)';
					em.style.padding = '0.1em 0.3em';
					em.style.color = '#FFF';
					em.style.fontSize = '10px';
					em.style.fontStyle = 'normal';
					em.innerHTML = c.data[i][ii];
					var left = c.width * i + (c.width / 2);
					span.style.left = left - ajust +'px';
					em.style.left = left - ajust + c.pointSize +'px';
					var top = ((arch[ii].max - c.data[i][ii]) * arch[ii].par);
					span.style.top = top - ajust + c.padding + 'px';
					em.style.top = top - ajust + c.padding - c.pointSize + 'px';
					points[ii][i].x = left;
					points[ii][i].y = top;
					span.style.background = c.color[ii];
					span.title = c.data[i][ii];
					target.appendChild(span);
					target.appendChild(em);
				};
			};
			var ajust = 0;
			for(var i=points.length-1;i>=0;i--){
				ctx.beginPath();
				ctx.lineWidth = 1;
				ctx.strokeStyle = c.color[i];
				ctx.moveTo(points[i][0].x+ajust,points[i][0].y+c.padding);
				for(var ii=1;ii<points[i].length;ii++){
					ctx.lineTo(points[i][ii].x+ajust,points[i][ii].y+c.padding);
				};
				ctx.stroke();
			};
	}
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
web.initialize();

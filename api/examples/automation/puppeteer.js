//!/usr/bin/env node

//
//	Browser Bubble Pro
//	CyDec Security
//	Copyright (c) 2022
//
//	https://www.cydecsecurity.com
//
//	Full API documentation can be found at https://www.cydecsecurity.com/bbapi.html
//
//	Example Requirements
// 		Node.js
//		npm i puppeteer
//		npm i websocket
//
//	This example shows how Browser Bubble Pro can be used with Puppeteer.
//
//	There is very little difference in Browser Bubble Pro API usage between using an 
//	automation framework and not.  The only difference when using an automation
//	framework is that you must wait for the BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT
//	message with the debug port details so that you can connect to the Bubble instance.
//
//	Using the .launch() method, or equivalent, in Puppeteer or Playwright is not supported.
//	You must connect to the instance after the Bubble has been launched.  Otherwise
//	Browser Bubble Pro will not recognize the browser execution even if the browser itself
//	has been added to the browser list.
// 
//	For this example, we first add the Chromium browser that was installed with 
//	Puppeteer.  The path for chrome.exe will be deep in the npm directory generally
//	under the c:\users\<username>\appdata\roaming\ directory.  The Puppeteer docs
//	specifically states that you should only use the bundled browsers however, your
//	existing browsers and profiles may work just fine.  Once the browser is
//	added, it returns a 'Browser ID' that is then used when creating a new Bubble.
//	When the Bubble is successfully created, it will return a 'Bubble ID.'  This,
//	in turn, is used to launch the Bubble.  As the docs state, launching a Bubble is an
//	async operation so it will return an 'Instance ID' but it is not in a ready 
//	state.  It's not until the client receives BB_SERVER_BUBBLE_SUB_ACTION_READY
//	is the Bubble ready.  BB_SERVER_BUBBLE_SUB_ACTION_FAILED is sent when the Bubble
//	fails to launch.  Because remote debugging is enabled, BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT
//	will be sent containing the details needed for the automation framework to
//	actually connect to the instance.  Once that information is available, you can
//	start performing whatever automation tasks you desire.  When you are ready to 
//	terminate the Bubble, you can use the automation framework API or Browser Bubble.
//

//--------------------------------------------------------
// BUBBLE CONSTS
//--------------------------------------------------------
const BB_SERVER = 'ws://localhost:8778/';

const BB_ERROR_NO_ERROR = 0;
const BB_ERROR_GENERIC_ERROR = -1;
const BB_ERROR_INVALID_PARAMETER = -3;
const BB_ERROR_INVALID_MODE = -26;

const BB_DATA_TYPE_STRING = 1;
const BB_DATA_TYPE_INTEGER = 2;
const BB_DATA_TYPE_JSON = 3;
const BB_DATA_TYPE_BINARY = 4;

const BB_LOG_LEVEL_DEBUG = 1;
const BB_LOG_LEVEL_ERROR = 2;
const BB_LOG_LEVEL_INFO = 3;
const BB_LOG_LEVEL_WARN = 4;
const BB_LOG_LEVEL_PRIORITY = 5;

const BB_SERVER_ACTION_STATUS = 0;
const BB_SERVER_STATUS_SUB_ACTION_CURRENT = 1;
const BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN = 2;
const BB_SERVER_STATUS_SUB_ACTION_LOG = 3;

const BB_SERVER_ACTION_BROWSER = 2;
const BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY = 1;
const BB_SERVER_BROWSER_SUB_ACTION_LIST = 2;
const BB_SERVER_BROWSER_SUB_ACTION_ADD = 3;
const BB_SERVER_BROWSER_SUB_ACTION_DELETE = 4;
const BB_SERVER_BROWSER_SUB_ACTION_UPDATE = 5;

const BB_SERVER_ACTION_SPEECH = 3;
const BB_SERVER_SPEECH_SUB_ACTION_LIST = 1;

const BB_SERVER_ACTION_DNS = 5;
const BB_SERVER_DNS_SUB_ACTION_LIST = 2;

const BB_SERVER_ACTION_PROXY = 6;
const BB_SERVER_PROXY_SUB_ACTION_LIST = 1;

const BB_SERVER_ACTION_VPN = 7;
const BB_SERVER_VPN_SUB_ACTION_LIST = 1;

const BB_SERVER_ACTION_BUBBLE = 8;
const BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED = 1;
const BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING = 2;
const BB_SERVER_BUBBLE_SUB_ACTION_CREATE = 3;
const BB_SERVER_BUBBLE_SUB_ACTION_DELETE = 4;
const BB_SERVER_BUBBLE_SUB_ACTION_UPDATE = 5;
const BB_SERVER_BUBBLE_SUB_ACTION_DETAILS = 6;
const BB_SERVER_BUBBLE_SUB_ACTION_GENERATE = 7;
const BB_SERVER_BUBBLE_SUB_ACTION_SHORTCUT = 8;
const BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH = 9;
const BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE = 10;
const BB_SERVER_BUBBLE_SUB_ACTION_NETWORK = 11;
const BB_SERVER_BUBBLE_SUB_ACTION_READY = 12;
const BB_SERVER_BUBBLE_SUB_ACTION_FAILED = 13;
const BB_SERVER_BUBBLE_SUB_ACTION_SHUTDOWN = 14;
const BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT = 15;

const BB_BUBBLE_SPOOF_TIMEZONE = 1;
const BB_BUBBLE_SPOOF_SCREEN = 2;
const BB_BUBBLE_SPOOF_CPU = 3;
const BB_BUBBLE_SPOOF_MEMORY = 4;
const BB_BUBBLE_SPOOF_TOUCHPOINTS = 5;
const BB_BUBBLE_SPOOF_FONTS = 6;
const BB_BUBBLE_SPOOF_LANGUAGE = 7;
const BB_BUBBLE_SPOOF_PLATFORM = 8;
//RESERVED = 9
const BB_BUBBLE_SPOOF_WEBGL = 10;
const BB_BUBBLE_SPOOF_MATH = 11;
const BB_BUBBLE_SPOOF_PERFTIMER = 12;
const BB_BUBBLE_SPOOF_WEBRTC = 13;
//RESERVED = 14
const BB_BUBBLE_SPOOF_MEDIA = 15;
const BB_BUBBLE_SPOOF_SPEECH = 16;
const BB_BUBBLE_SPOOF_BATTERY = 17;
const BB_BUBBLE_SPOOF_NETWORK = 18;

const BB_OS_DISABLED = 0;
const BB_OS_WIN7 = 1;
const BB_OS_WIN8 = 2;
const BB_OS_WIN81 = 4;
const BB_OS_WIN10 = 8;
const BB_OS_WIN11 = 16;
const BB_OS_CUSTOM = 32;

const BB_BATTERY_FLAG_PLUGGED_IN = 1;
const BB_BATTERY_FLAG_BATTERY_POWER = 2;
const BB_BATTERY_FLAG_NO_BATTERY = 4;

const BB_FONT_OPS_DISABLE = 1;
const BB_FONT_OPS_REMOVE_ALL_BUT_1 = 2;
const BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED = 4;
const BB_FONT_OPS_SET_OS = 8;
const BB_FONT_OPS_SET_CUSTOM = 16;

const BB_MATH_SPOOFING_OFF = 0;
const BB_MATH_SPOOFING_RANDOM = 1;
const BB_MATH_SPOOFING_SET = 2;

const BB_MEDIA_DEVICE_SPOOF_OFF = 0;
const BB_MEDIA_DEVICE_ENUM_RANDOM = 1;
const BB_MEDIA_DEVICE_ENUM_BLOCK = 2;
const BB_MEDIA_DEVICE_RENAME_NAMES = 4;
const BB_MEDIA_DEVICE_SET_SAMPLE = 8;

const BB_WEBGL_SPOOFING_OFF = 0;
const BB_WEBGL_SET_FEATURE_LEVEL = 1;
const BB_WEBGL_SET_IMAGE_RGB = 2;
const BB_WEBGL_RANDOMIZE_IMAGE_RBG = 4;

const BB_WEBGL_LEVEL_9_1 = 1;
const BB_WEBGL_LEVEL_9_2 = 2;
const BB_WEBGL_LEVEL_9_3 = 3;
const BB_WEBGL_LEVEL_10_0 = 4;
const BB_WEBGL_LEVEL_10_1 = 5;
const BB_WEBGL_LEVEL_11_0 = 6;
const BB_WEBGL_LEVEL_11_1 = 7;
const BB_WEBGL_LEVEL_12_0 = 8;
const BB_WEBGL_LEVEL_12_1 = 9;

const BB_BUBBLE_FLAG_ENCRYPT = 1;
const BB_BUBBLE_FLAG_WIPE_ON_CLOSE = 2;
const BB_BUBBLE_FLAG_CREATE_SHORTCUT = 4;
const BB_BUBBLE_FLAG_BORDER_COLOR = 8;
const BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ = 16;
const BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE = 32;
const BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE = 64;
const BB_BUBBLE_FLAG_DNS_BROWSER = 128;
const BB_BUBBLE_FLAG_DNS_BB = 256;
const BB_BUBBLE_FLAG_DNS_BLOCK = 512;
const BB_BUBBLE_FLAG_PROXY_SET = 1024;
const BB_BUBBLE_FLAG_VPN_SET = 2048;
const BB_BUBBLE_FLAG_CLEAN_SLATE = 4096;
const BB_BUBBLE_FLAG_DEBUG_PORT = 8192;

const BB_ICON_DIRECTORY_NONE = 0;
const BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP = 1;
const BB_ICON_DIRECTORY_ALL_USER_DESKTOP = 2;
const BB_ICON_DIRECTORY_USER_DEFINED = 3;

const BB_NETWORK_FLAG_ETHERNET = 1;
const BB_NETWORK_FLAG_WIFI = 2;

const BB_SPEECH_PROFILE = 1;
const BB_SPEECH_VOICE = 2;
const BB_SPEECH_PROFILE_VOICES = 3;

const BB_BROWSER_FIREFOX = 1;
const BB_BROWSER_EDGE = 2;
const BB_BROWSER_CHROME = 4;
const BB_BROWSER_BLISK = 8;
const BB_BROWSER_BRAVE = 16;
const BB_BROWSER_CANARY = 32;
const BB_BROWSER_CHROMIUM = 64;
const BB_BROWSER_IRIDIUM = 128;
const BB_BROWSER_IRON = 256;
const BB_BROWSER_OPERA = 512;
const BB_BROWSER_VIVALDI = 1024;
const BB_BROWSER_FIREFOX_NIGHTLY = 2048;
const BB_BROWSER_EPIC = 4096;
//User defined browsers.
const BB_BROWSER_EXTRA_1 = 262144;
const BB_BROWSER_EXTRA_2 = 524288;
const BB_BROWSER_EXTRA_3 = 1048576;
const BB_BROWSER_EXTRA_4 = 2097152;
const BB_BROWSER_EXTRA_5 = 4194304;
const BB_BROWSER_EXTRA_6 = 8388608;
const BB_BROWSER_EXTRA_7 = 16777216;
const BB_BROWSER_EXTRA_8 = 33554432;
//--------------------------------------------------------
//--------------------------------------------------------

var _messageId = 1;
var _messageCb = [];

const puppeteer = require('puppeteer');

var WebSocketClient = require('websocket').client;
var client = new WebSocketClient();
client.on('connectFailed', function(error) {
	console.log('There was an error connecting: ' + error.toString());
});

client.on('connect', function(connection) {
	console.log('Connected to Browser Bubble Pro');

	connection.on('error', function(error) {
		console.log("There was a connection error: " + error.toString());
	});

	connection.on('close', function() {
		console.log('The connection to Browser Bubble Pro has been closed.');
	});

	connection.on('message', function(message) {
		if (message.type === 'utf8') {
			try {
				//SERVER_RESPONSE
				//	Version: (int)
				//	ErrorCode: (int)
				//	DataType: (int)
				//	MessageID: (long)
				//	ReturnValue: (str)				
				var sr = JSON.parse(message.utf8Data);
				var ec = sr['ErrorCode']
				var msgId = sr['MessageID']

				if (sr['MessageID'] > 0) {
					if (sr['MessageID'] in _messageCb) {
						var cba = _messageCb[msgId];
						var act = cba[0];
						var suba = cba[1];
						var callback = cba[2];

						delete _messageCb[msgId];
		
						console.log("Received action (" + act + ", " + suba + ") response with message id of " + msgId + ".");
		
						if (sr['DataType'] == BB_DATA_TYPE_STRING) {
							if (ec == BB_ERROR_NO_ERROR) {
								console.log("\tThe operation was successful and returned: " + sr['ReturnValue']);
							} else {
								console.log("\tThe operation was failed and returned: " + sr['ReturnValue']);
							}
						} else if (sr['DataType'] == BB_DATA_TYPE_INTEGER) {
							if (act == BB_SERVER_ACTION_BROWSER) {
								if (suba == BB_SERVER_BROWSER_SUB_ACTION_ADD) {
									if (ec == BB_ERROR_NO_ERROR) {
										console.log("\tThe new browser id is " + sr['ReturnValue'] + ".");
									}
								}
							} else if (act == BB_SERVER_ACTION_BUBBLE) {
								if (suba == BB_SERVER_BUBBLE_SUB_ACTION_CREATE) {
									if (ec == BB_ERROR_NO_ERROR) {
										console.log("\tThe new Bubble id is " + sr['ReturnValue'] + ".");
									}
								} else if (suba == BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH) {
									if (ec == BB_ERROR_NO_ERROR) {
										console.log("\tThe launched Bubble instance id is " + sr['ReturnValue'] + ".");
									}
								}
							}
						}

						if (callback != undefined) {
							callback(msgId, act, suba, ec, sr['ReturnValue']);
						}
					}
				} else {
					if (sr['DataType'] == BB_DATA_TYPE_JSON) {
						var action = JSON.parse(sr['ReturnValue']);

						if (action['Action'] == BB_SERVER_ACTION_BUBBLE) {
							if (action['SubAction'] == BB_SERVER_BUBBLE_SUB_ACTION_READY) {
								//This is sent if the Bubble was launched successfully and
								//is in a ready state.
								
								//BUBBLE_LAUNCHED
								//	InstanceID: (long)
								//	BubbleID: (long)
								//	MountPoint: (str)
								//	PreLaunch: (LAUNCH_RESULT)
								//	PostLaunch: (LAUNCH_RESULT)
								var bl = JSON.parse(action['ValueString']);
								console.log(">> Bubble (" + bl['InstanceID'] + ") is ready for use.");
								console.log("\tBubble ID: " + bl['BubbleID']);
								console.log("\tMount: " + bl['MountPoint']);
								var lr = bl['PreLaunch'];
								console.log("\tPre Launch");
								console.log("\t\tError Code: " + lr['ErrorCode']);
								console.log("\t\tEval Result: " + lr['Eval']);
								console.log("\t\tOutput: " + lr['Output']);
								var lr = bl['PostLaunch'];
								console.log("\tPost Launch");
								console.log("\t\tError Code: " + lr['ErrorCode']);
								console.log("\t\tEval Result: " + lr['Eval']);
								console.log("\t\tOutput: " + lr['Output']);					
							} else if (action['SubAction'] == BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT) {
								//This is sent after Browser Bubble is able to capture the
								//information from the recently launched Bubble.  It's what
								//you need for the framework to connect to the browser.

								//BUBBLE_DEBUG_PORT
								//	InstanceID: (long)
								//	Port: (long)
								//	WsEndPoint: (str)
								var dbg = JSON.parse(action['ValueString']);
								console.log(">> Bubble (" + dbg['InstanceID'] + ") has debugging enabled.");
								console.log("\tPort: " + dbg['Port']);
								console.log("\tEndPoint: " + dbg['WsEndPoint']);

								(async () => {
									const browser = await puppeteer.connect({
										browserWSEndpoint: 'ws://localhost:' + dbg['Port'] + '/devtools/browser/' + dbg['WsEndPoint']
									});
						
									const page = await browser.newPage();
									await page.goto('https://www.browserleaks.com/javascript');
									await page.screenshot({ path: 'browserleaks.png', fullPage: true });
								
									//await browser.close();
								})();
							}
						}
					}
				}
			} catch(e) {
				console.log(e);
				console.trace();
			}
		}
	});

	function wrapWithServerRequest(data_type, msgId, obj) {
		//SERVER_REQUEST
		var sr = {};
		sr['Version'] = 1;
		sr['DataType'] = data_type;
		sr['MessageId'] = msgId;
		sr['RequestValue'] = obj;

		return JSON.stringify(sr);
	}

	function wrapAction(act, suba, valstr, callback = undefined) {
		var msgId = _messageId;
		_messageId += 1;
		_messageCb[msgId] = [act, suba, callback];

		//ACTION
		var a = {};
		a['Action'] = act;
		a['SubAction'] = suba;
		a['ValueString'] = valstr;

		return wrapWithServerRequest(BB_DATA_TYPE_JSON, msgId, JSON.stringify(a));
	}

	function browserAddedCallback(msgId, act, suba, ec, returnValue) {
		var browserId = parseInt(returnValue);
		createBubble(browserId);	
	}

	function addBrowser() {
		//Add a new browser.  You can use the ones installed with Puppeteer or Playwright
		//or you can use your existing browser installs (as long as it is compatible with
		//those automation frameworks).  This will return a browser ID that we then
		//use when we create a Bubble.

		//BROWSER_PROFILE
		//	ID: (long)
		//	Name: (str)
		//	BrowserType: (int)
		//	FilePath: (str)
		//	ProfilePath: (str)
		//	Enabled: (int)
		var ba = {};
		ba['ID'] = 0;
		ba['Name'] = "Chromium (Puppeteer)";
		ba['BrowserType'] = BB_BROWSER_CHROMIUM;
		ba['FilePath'] = "c:\\users\\cydec\\appdata\\roaming\\npm\\node_modules\\puppeteer\\.local-chromium\\win64-950341\\chrome-win\\chrome.exe";
		ba['ProfilePath'] = "c:\\users\\cydec\\appdata\\local\\chromium\\user data";
		ba['Enabled'] = 1;
	
		try {
			var act = wrapAction(BB_SERVER_ACTION_BROWSER, BB_SERVER_BROWSER_SUB_ACTION_ADD, JSON.stringify(ba), browserAddedCallback);
			connection.sendUTF(act);	
		} catch(e) {
			console.log(e);
			console.trace();
		}
	}

	function createBubble(browserId) {
		try {
			//LAUNCH_ACTIONS
			//	Pre: (str)
			//	Post: (str)
			//	Shutdown: (str)
			var l = {};
			l['Pre'] = "";
			l['Post'] = "";
			l['Shutdown'] = "";

			//BUBBLE_CREATE
			//	Name: (str)
			//	BrowserID: (long)
			//	DNSID: (long)
			//	ProxyList: (list[long])
			//	VPNID: (long)
			//	Launch: (LAUNCH_ACTIONS)
			//	Options: (int)
			//	BorderColor: (str)
			//	SpoofSettings: (dict[int, str])
			var bc = {};
			bc['Name'] = "New Bubble #" + getRandomInt(1, 1000000);
			bc['BrowserID'] = browserId;
			bc['DNSID'] = 0;
			bc['ProxyList'] = [];
			bc['VPNID'] = 0;
			bc['Launch'] = l;
			bc['Options'] = BB_BUBBLE_FLAG_WIPE_ON_CLOSE | BB_BUBBLE_FLAG_BORDER_COLOR | BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ | BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE | BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE;
			bc['BorderColor'] = "#ff0000";

			var ss = {};

			//SPOOF_TIMEZONE
			//	IANA: (str)
			//	Name: (str)
			//	Zone: (str)
			var tz = {};
			tz['IANA'] = "Asia/Bangkok";
			tz['Name'] = "SE Asia Standard Time";
			tz['Zone'] = "UTC+07:00";
			ss[BB_BUBBLE_SPOOF_TIMEZONE] = JSON.stringify(tz);

			ss[BB_BUBBLE_SPOOF_SCREEN] = "1600x900x16";
			ss[BB_BUBBLE_SPOOF_CPU] = "6";
			ss[BB_BUBBLE_SPOOF_MEMORY] = "12";
			ss[BB_BUBBLE_SPOOF_TOUCHPOINTS] = "3";

			//SPOOF_FONT
			//	Flags: (int)
			//	Extra: (long)
			var sf = {};
			sf['Flags'] = BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED;
			sf['Extra'] = 15;
			ss[BB_BUBBLE_SPOOF_FONTS] = JSON.stringify(sf);

			//LANGUAGE
			//	ID: (long)
			//	Name: (str)
			//	Code: (str)
			var sl = {};
			sl['ID'] = 2057;
			sl['Name'] = "English - United Kingdom";
			sl['Code'] = "en-GB";
			ss[BB_BUBBLE_SPOOF_LANGUAGE] = JSON.stringify(sl);

			//SPOOF_OS
			//	Windows: (int)
			//	Build: (int)
			var so = {};
			so['Windows'] = BB_OS_WIN7;
			so['Build'] = 0;
			ss[BB_BUBBLE_SPOOF_PLATFORM] = JSON.stringify(so);

			//SPOOF_WEBGL
			//	Spoof: (int)
			//	Offset: (int)
			//	Level: (int)
			var sw = {};
			sw['Spoof'] = BB_WEBGL_SET_FEATURE_LEVEL | BB_WEBGL_SET_IMAGE_RGB;
			sw['Offset'] = 123456;
			sw['Level'] = BB_WEBGL_LEVEL_10_0;
			ss[BB_BUBBLE_SPOOF_WEBGL] = JSON.stringify(sw);

			//SPOOF_MATH
			//	Flag: (int)
			//	Offset: (int)
			var sm = {};
			sm['Flag'] = BB_MATH_SPOOFING_RANDOM;
			sm['Offset'] = 0;
			ss[BB_BUBBLE_SPOOF_MATH] = JSON.stringify(sm);

			ss[BB_BUBBLE_SPOOF_PERFTIMER] = "1";
			ss[BB_BUBBLE_SPOOF_WEBRTC] = "1";

			//SPOOF_MEDIA
			//	Flags: (int)
			//	SetVal: (int)
			var sd = {};
			sd['Flags'] = BB_MEDIA_DEVICE_RENAME_NAMES | BB_MEDIA_DEVICE_SET_SAMPLE;
			sd['SetVal'] = 123456;
			ss[BB_BUBBLE_SPOOF_MEDIA] = JSON.stringify(sd);

			//SPOOF_BATTERY
			//	Flags: (int)
			//	Values1: (int)
			//	Values2: (int)
			//	Values3: (int)
			var sp = {};
			sp['Flags'] = BB_BATTERY_FLAG_BATTERY_POWER;
			sp['Values1'] = 56;
			sp['Values2'] = 25200;
			sp['Values3'] = 3600;
			ss[BB_BUBBLE_SPOOF_BATTERY] = JSON.stringify(sp);

			ss[BB_BUBBLE_SPOOF_NETWORK] = ''+BB_NETWORK_FLAG_ETHERNET;

			bc['SpoofSettings'] = ss;

			var act = wrapAction(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_CREATE, JSON.stringify(bc), bubbleCreatedCallback);
			connection.sendUTF(act);			
		} catch(e) {
			console.log(e);
			console.trace();
		}
	}

	function bubbleCreatedCallback(msgId, act, suba, ec, returnValue) {
		var bubbleId = parseInt(returnValue);
		launchBubble(bubbleId);
	}

	function launchBubble(bubbleId) {
		//The BB_BUBBLE_FLAG_DEBUG_PORT flag can be set when
		//creating the Bubble or when launching it.  It is 
		//added here just for demonstration purposes.

		var bl = {};
		bl['ID'] = bubbleId;
		bl['IsInstance'] = 0;
		bl['Flags'] = BB_BUBBLE_FLAG_DEBUG_PORT;
		bl['Password'] = "";
		bl['DNSID'] = 0;
		bl['ProxyList'] = [];
		bl['VPNID'] = 0;

		try {
			var act = wrapAction(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH, JSON.stringify(bl));
			connection.sendUTF(act);
		} catch(e) {
			console.log(e);
			console.trace();
		}		
	}

	if (connection.connected) {
		addBrowser();
	}

	function getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min) + min);
	}
});

client.connect(BB_SERVER);

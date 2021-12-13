#
#	Browser Bubble Pro
#	CyDec Security
#	Copyright (c) 2021
#
#	https://www.cydecsecurity.com
#
#	Full API documentation can be found at https://www.cydecsecurity.com/bbapi.html
#
#	Example Requirements
# 		Python 3.7+	
#		pip3 install websocket-client
#			https://websocket-client.readthedocs.io/en/latest/installation.html
#
#	This example runs through the full lifecycle for a Bubble with an async callback.
#

import websocket
import json
import traceback
import random
from queue import Queue
import threading
import _thread

# Uncomment to get websocket debug messages
#websocket.enableTrace(True)

#--------------------------------------------------------
# GLOBAL VARIABLES
#--------------------------------------------------------
_message_id = 1
_message_cb = {}
_ws_app = None
_send_queue = Queue()
_next_cmd = threading.Event()

_bubble_last_insert_id = 0
_bubble_running_id = 0
_bubble_saved_list = {}
_bubble_run_list = {}
_browser_list = {}
_dns_list = {}
_proxy_list = {}
_vpn_list = {}
_speech_profile_list = {}
#--------------------------------------------------------
#--------------------------------------------------------

#--------------------------------------------------------
# BUBBLE CONSTS
#--------------------------------------------------------
BB_SERVER = "ws://localhost:8778"

BB_ERROR_NO_ERROR = 0
BB_ERROR_GENERIC_ERROR = -1
BB_ERROR_INVALID_PARAMETER = -3
BB_ERROR_INVALID_MODE = -26

BB_DATA_TYPE_STRING = 1
BB_DATA_TYPE_INTEGER = 2
BB_DATA_TYPE_JSON = 3
BB_DATA_TYPE_BINARY = 4

BB_LOG_LEVEL_DEBUG = 1
BB_LOG_LEVEL_ERROR = 2
BB_LOG_LEVEL_INFO = 3
BB_LOG_LEVEL_WARN = 4
BB_LOG_LEVEL_PRIORITY = 5

BB_SERVER_ACTION_STATUS = 0
BB_SERVER_STATUS_SUB_ACTION_CURRENT = 1
BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN = 2
BB_SERVER_STATUS_SUB_ACTION_LOG = 3

BB_SERVER_ACTION_BROWSER = 2
BB_SERVER_BROWSER_SUB_ACTION_LIST = 2

BB_SERVER_ACTION_SPEECH = 3
BB_SERVER_SPEECH_SUB_ACTION_LIST = 1

BB_SERVER_ACTION_DNS = 5
BB_SERVER_DNS_SUB_ACTION_LIST = 2

BB_SERVER_ACTION_PROXY = 6
BB_SERVER_PROXY_SUB_ACTION_LIST = 1

BB_SERVER_ACTION_VPN = 7
BB_SERVER_VPN_SUB_ACTION_LIST = 1

BB_SERVER_ACTION_BUBBLE = 8
BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED = 1
BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING = 2
BB_SERVER_BUBBLE_SUB_ACTION_CREATE = 3
BB_SERVER_BUBBLE_SUB_ACTION_DELETE = 4
BB_SERVER_BUBBLE_SUB_ACTION_UPDATE = 5
BB_SERVER_BUBBLE_SUB_ACTION_DETAILS = 6
BB_SERVER_BUBBLE_SUB_ACTION_GENERATE = 7
BB_SERVER_BUBBLE_SUB_ACTION_SHORTCUT = 8
BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH = 9
BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE = 10
BB_SERVER_BUBBLE_SUB_ACTION_NETWORK = 11
BB_SERVER_BUBBLE_SUB_ACTION_READY = 12
BB_SERVER_BUBBLE_SUB_ACTION_FAILED = 13
BB_SERVER_BUBBLE_SUB_ACTION_SHUTDOWN = 14

BB_BUBBLE_SPOOF_TIMEZONE = 1
BB_BUBBLE_SPOOF_SCREEN = 2
BB_BUBBLE_SPOOF_CPU = 3
BB_BUBBLE_SPOOF_MEMORY = 4
BB_BUBBLE_SPOOF_TOUCHPOINTS = 5
BB_BUBBLE_SPOOF_FONTS = 6
BB_BUBBLE_SPOOF_LANGUAGE = 7
BB_BUBBLE_SPOOF_PLATFORM = 8
# RESERVED = 9
BB_BUBBLE_SPOOF_WEBGL = 10
BB_BUBBLE_SPOOF_MATH = 11
BB_BUBBLE_SPOOF_PERFTIMER = 12
BB_BUBBLE_SPOOF_WEBRTC = 13
# RESERVED = 14
BB_BUBBLE_SPOOF_MEDIA = 15
BB_BUBBLE_SPOOF_SPEECH = 16
BB_BUBBLE_SPOOF_BATTERY = 17
BB_BUBBLE_SPOOF_NETWORK = 18

BB_OS_DISABLED = 0
BB_OS_WIN7 = 1
BB_OS_WIN8 = 2
BB_OS_WIN81 = 4
BB_OS_WIN10 = 8
BB_OS_WIN11 = 16
BB_OS_CUSTOM = 32

BB_BATTERY_FLAG_PLUGGED_IN = 1
BB_BATTERY_FLAG_BATTERY_POWER = 2
BB_BATTERY_FLAG_NO_BATTERY = 4

BB_FONT_OPS_DISABLE = 1
BB_FONT_OPS_REMOVE_ALL_BUT_1 = 2
BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED = 4
BB_FONT_OPS_SET_OS = 8
BB_FONT_OPS_SET_CUSTOM = 16

BB_MATH_SPOOFING_OFF = 0
BB_MATH_SPOOFING_RANDOM = 1
BB_MATH_SPOOFING_SET = 2

BB_MEDIA_DEVICE_SPOOF_OFF = 0
BB_MEDIA_DEVICE_ENUM_RANDOM = 1
BB_MEDIA_DEVICE_ENUM_BLOCK = 2
BB_MEDIA_DEVICE_RENAME_NAMES = 4
BB_MEDIA_DEVICE_SET_SAMPLE = 8

BB_WEBGL_SPOOFING_OFF = 0
BB_WEBGL_SET_FEATURE_LEVEL = 1
BB_WEBGL_SET_IMAGE_RGB = 2
BB_WEBGL_RANDOMIZE_IMAGE_RBG = 4

BB_WEBGL_LEVEL_9_1 = 1
BB_WEBGL_LEVEL_9_2 = 2
BB_WEBGL_LEVEL_9_3 = 3
BB_WEBGL_LEVEL_10_0 = 4
BB_WEBGL_LEVEL_10_1 = 5
BB_WEBGL_LEVEL_11_0 = 6
BB_WEBGL_LEVEL_11_1 = 7
BB_WEBGL_LEVEL_12_0 = 8
BB_WEBGL_LEVEL_12_1 = 9

BB_BUBBLE_FLAG_ENCRYPT = 1
BB_BUBBLE_FLAG_WIPE_ON_CLOSE = 2
BB_BUBBLE_FLAG_CREATE_SHORTCUT = 4
BB_BUBBLE_FLAG_BORDER_COLOR = 8
BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ = 16
BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE = 32
BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE = 64
BB_BUBBLE_FLAG_DNS_BROWSER = 128
BB_BUBBLE_FLAG_DNS_BB = 256
BB_BUBBLE_FLAG_DNS_BLOCK = 512
BB_BUBBLE_FLAG_PROXY_SET = 1024
BB_BUBBLE_FLAG_VPN_SET = 2048

BB_ICON_DIRECTORY_NONE = 0
BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP = 1
BB_ICON_DIRECTORY_ALL_USER_DESKTOP = 2
BB_ICON_DIRECTORY_USER_DEFINED = 3

BB_NETWORK_FLAG_ETHERNET = 1
BB_NETWORK_FLAG_WIFI = 2

BB_SPEECH_PROFILE = 1
BB_SPEECH_VOICE = 2
BB_SPEECH_PROFILE_VOICES = 3

BB_BROWSER_FIREFOX = 1
BB_BROWSER_EDGE = 2
BB_BROWSER_CHROME = 4
BB_BROWSER_BLISK = 8
BB_BROWSER_BRAVE = 16
BB_BROWSER_CANARY = 32
BB_BROWSER_CHROMIUM = 64
BB_BROWSER_IRIDIUM = 128
BB_BROWSER_IRON = 256
BB_BROWSER_OPERA = 512
BB_BROWSER_VIVALDI = 1024
BB_BROWSER_FIREFOX_NIGHTLY = 2048
BB_BROWSER_EPIC = 4096
#User defined browsers.
BB_BROWSER_EXTRA_1 = 262144
BB_BROWSER_EXTRA_2 = 524288
BB_BROWSER_EXTRA_3 = 1048576
BB_BROWSER_EXTRA_4 = 2097152
BB_BROWSER_EXTRA_5 = 4194304
BB_BROWSER_EXTRA_6 = 8388608
BB_BROWSER_EXTRA_7 = 16777216
BB_BROWSER_EXTRA_8 = 33554432
#--------------------------------------------------------
#--------------------------------------------------------

def wrap_with_server_request(data_type, msg_id, obj):
	#SERVER_REQUEST
	sr = {}
	sr['Version'] = 1
	sr['DataType'] = data_type
	sr['MessageId'] = msg_id
	sr['RequestValue'] = obj

	return json.dumps(sr)

def wrap_action(act, suba, valstr, callback = None):
	global _message_id
	global _message_cb

	evt = threading.Event()

	msgId = _message_id
	_message_id += 1
	_message_cb[msgId] = [act, suba, evt, callback]

	#ACTION
	a = {}
	a['Action'] = act
	a['SubAction'] = suba
	a['ValueString'] = valstr

	return msgId, wrap_with_server_request(BB_DATA_TYPE_JSON, msgId, json.dumps(a))

def print_log_message(s):
	#LOG_MESSAGE
	#	ErrorCode int
	#	Level     int
	#	Location  string
	#	Message   string
		
	lm = json.loads(s)
	if lm['Level'] == BB_LOG_LEVEL_DEBUG:
		print("[$] " + lm['Message'])
	elif lm['Level'] == BB_LOG_LEVEL_ERROR:
		print("[!] " + lm['Message'])
	elif lm['Level'] == BB_LOG_LEVEL_INFO:
		print("[*] " + lm['Message'])
	elif lm['Level'] == BB_LOG_LEVEL_WARN:
		print("[>] " + lm['Message'])
	elif lm['Level'] == BB_LOG_LEVEL_PRIORITY:
		print("[!!!] " + lm['Message'])

def browser_type_to_name(browser_type):
	if browser_type == BB_BROWSER_FIREFOX:
		return "Firefox"
	if browser_type == BB_BROWSER_EDGE:
		return "Edge"
	if browser_type == BB_BROWSER_CHROME:
		return "Chrome"
	if browser_type == BB_BROWSER_BLISK:
		return "Blisk"
	if browser_type == BB_BROWSER_BRAVE:
		return "Brave"
	if browser_type == BB_BROWSER_CANARY:
		return "Chrome Canary"
	if browser_type == BB_BROWSER_CHROMIUM:
		return "Chromium"
	if browser_type == BB_BROWSER_IRIDIUM:
		return "Iridium"
	if browser_type == BB_BROWSER_IRON:
		return "Iron"
	if browser_type == BB_BROWSER_OPERA:
		return "Opera"
	if browser_type == BB_BROWSER_VIVALDI:
		return "Vivaldi"
	if browser_type == BB_BROWSER_FIREFOX_NIGHTLY:
		return "Firefox Nightly"
	if browser_type == BB_BROWSER_EPIC:
		return "Epic"

	return "Unknown"

def spoof_name_lookup(flag):
	flag = int(flag)

	if flag == BB_BUBBLE_SPOOF_TIMEZONE:
		return "Time Zone"
	if flag == BB_BUBBLE_SPOOF_SCREEN:
		return "Screen"
	if flag == BB_BUBBLE_SPOOF_CPU:
		return "CPU"
	if flag == BB_BUBBLE_SPOOF_MEMORY:
		return "Memory"
	if flag == BB_BUBBLE_SPOOF_TOUCHPOINTS:
		return "Touchpoints"
	if flag == BB_BUBBLE_SPOOF_FONTS:
		return "Fonts"
	if flag == BB_BUBBLE_SPOOF_LANGUAGE:
		return "Language"
	if flag == BB_BUBBLE_SPOOF_PLATFORM:
		return "OS"
	if flag == BB_BUBBLE_SPOOF_WEBGL:
		return "WebGL"
	if flag == BB_BUBBLE_SPOOF_MATH:
		return "Math"
	if flag == BB_BUBBLE_SPOOF_PERFTIMER:
		return "Performance Timer"
	if flag == BB_BUBBLE_SPOOF_WEBRTC:
		return "WebRTC"
	if flag == BB_BUBBLE_SPOOF_MEDIA:
		return "Media Devices"
	if flag == BB_BUBBLE_SPOOF_SPEECH:
		return "Speech Voices"
	if flag == BB_BUBBLE_SPOOF_BATTERY:
		return "Battery"
	if flag == BB_BUBBLE_SPOOF_NETWORK:
		return "Network"

	return "Unknown"

def print_dns_px_vpn(o, tabs):
	if o['DNSID'] > 0:
		if o['DNSID'] in _dns_list:
			print(tabs + "DNS: " + _dns_list[o['DNSID']])

	if len(o['ProxyList']) > 0:
		for px in o['ProxyList']:
			if px in _proxy_list:
				print(tabs + "Proxy: " + _proxy_list[px])

	if o['VPNID'] > 0:
		if o['VPNID'] in _vpn_list:
			print(tabs + "VPN: " + _vpn_list[o['VPNID']])

def print_bubble_options(ops, bc, tabs):
	print(tabs + "Options")
	if ops & BB_BUBBLE_FLAG_ENCRYPT:
		print(tabs + "\tEncrypt sandbox")
	if ops & BB_BUBBLE_FLAG_WIPE_ON_CLOSE:
		print(tabs + "\tSandbox wipe on close")
	if ops & BB_BUBBLE_FLAG_CREATE_SHORTCUT:
		print(tabs + "\tShortcut created")
	if ops & BB_BUBBLE_FLAG_BORDER_COLOR:
		print(tabs + "\tBorder color: " + bc)
	if ops & BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ:
		print(tabs + "\tAnti-exploit read")
	if ops & BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE:
		print(tabs + "\tAnti-exploit write")
	if ops & BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE:
		print(tabs + "\tAnti-exploit execute")
	if ops & BB_BUBBLE_FLAG_DNS_BROWSER:
		print(tabs + "\tBrowser DNS")
	if ops & BB_BUBBLE_FLAG_DNS_BB:
		print(tabs + "\tBrowser Bubble DNS")
		if ops & BB_BUBBLE_FLAG_DNS_BLOCK:
			print(tabs + "\t\tDNS blocking")
	if ops & BB_BUBBLE_FLAG_PROXY_SET:
		print(tabs + "\tProxy set")
	if ops & BB_BUBBLE_FLAG_VPN_SET:
		print(tabs + "\tVPN set")

def bubble_create_shortcut(id):
	#BUBBLE_SHORTCUT
	#	ID: (long)
	#	IsInstance: (int)
	#	Name: (str)
	#	IconLocation: (int)
	#	IconPath: (str)
	bs = {}
	bs['ID'] = id
	bs['IsInstance'] = 0
	bs['Name'] = "New Bubble Shortcut"
	bs['IconLocation'] = BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP
	bs['IconPath'] = 0
	wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_SHORTCUT, json.dumps(bs))

def bubble_generate_new():
	#BUBBLE_GENERATE
	#	BrowserID: (long)
	#	Count: (int)
	#	IconLocation: (int)
	#	IconPath: (str)

	try:
		#Generate two new Bubbles
		bg = {}
		#Just get a random browser from our list.
		browser_id, browser_name = random.choice(list(_browser_list.items()))
		bg['BrowserID'] = browser_id
		bg['Count'] = 2
		bg['IconLocation'] = BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP
		bg['IconPath'] = ""
		wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_GENERATE, json.dumps(bg))	
	except Exception as e:
		print(e)
		print(traceback.format_exc())

def bubble_create_new(callback=None):
	try:
		#LAUNCH_ACTIONS
		#	Pre: (str)
		#	Post: (str)
		#	Shutdown: (str)
		l = {}
		l['Pre'] = ""
		l['Post'] = ""
		l['Shutdown'] = ""

		#BUBBLE_CREATE
		#	Name: (str)
		#	BrowserID: (long)
		#	DNSID: (long)
		#	ProxyList: (list[long])
		#	VPNID: (long)
		#	Launch: (LAUNCH_ACTIONS)
		#	Options: (int)
		#	BorderColor: (str)
		#	SpoofSettings: (dict[int, str])
		bc = {}
		bc['Name'] = "New Bubble #" + str(random.randint(1, 1000000))

		browser_id = 0
		if len(_browser_list) > 0:
			browser_id, browser_name = random.choice(list(_browser_list.items()))
		bc['BrowserID'] = browser_id
		bc['DNSID'] = 0
		bc['ProxyList'] = []
		bc['VPNID'] = 0
		bc['Launch'] = l
		bc['Options'] = BB_BUBBLE_FLAG_WIPE_ON_CLOSE | BB_BUBBLE_FLAG_BORDER_COLOR | BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ | BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE | BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE
		bc['BorderColor'] = "#ff0000"

		ss = {}

		#SPOOF_TIMEZONE
		#	IANA: (str)
		#	Name: (str)
		#	Zone: (str)
		tz = {}
		tz['IANA'] = "Europe/Belgrade"
		tz['Name'] = "Central Europe Standard Time"
		tz['Zone'] = "UTC+01:00"
		ss[BB_BUBBLE_SPOOF_TIMEZONE] = json.dumps(tz)

		ss[BB_BUBBLE_SPOOF_SCREEN] = "1600x900x16"
		ss[BB_BUBBLE_SPOOF_CPU] = "6"
		ss[BB_BUBBLE_SPOOF_MEMORY] = "12"
		ss[BB_BUBBLE_SPOOF_TOUCHPOINTS] = "3"

		#SPOOF_FONT
		#	Flags: (int)
		#	Extra: (long)
		sf = {}
		sf['Flags'] = BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED
		sf['Extra'] = 15
		ss[BB_BUBBLE_SPOOF_FONTS] = json.dumps(sf)

		#LANGUAGE
		#	ID: (long)
		#	Name: (str)
		#	Code: (str)
		sl = {}
		sl['ID'] = 2057
		sl['Name'] = "English - United Kingdom"
		sl['Code'] = "en-GB"
		ss[BB_BUBBLE_SPOOF_LANGUAGE] = json.dumps(sl)

		#SPOOF_OS
		#	Windows: (int)
		#	Build: (int)
		so = {}
		so['Windows'] = BB_OS_WIN7
		so['Build'] = 0
		ss[BB_BUBBLE_SPOOF_PLATFORM] = json.dumps(so)

		#SPOOF_WEBGL
		#	Spoof: (int)
		#	Offset: (int)
		#	Level: (int)
		sw = {}
		sw['Spoof'] = BB_WEBGL_SET_FEATURE_LEVEL | BB_WEBGL_SET_IMAGE_RGB
		sw['Offset'] = 123456
		sw['Level'] = BB_WEBGL_LEVEL_10_0
		ss[BB_BUBBLE_SPOOF_WEBGL] = json.dumps(sw)

		#SPOOF_MATH
		#	Flag: (int)
		#	Offset: (int)
		sm = {}
		sm['Flag'] = BB_MATH_SPOOFING_RANDOM
		sm['Offset'] = 0
		ss[BB_BUBBLE_SPOOF_MATH] = json.dumps(sm)

		ss[BB_BUBBLE_SPOOF_PERFTIMER] = "1"
		ss[BB_BUBBLE_SPOOF_WEBRTC] = "1"

		#SPOOF_MEDIA
		#	Flags: (int)
		#	SetVal: (int)
		sd = {}
		sd['Flags'] = BB_MEDIA_DEVICE_RENAME_NAMES | BB_MEDIA_DEVICE_SET_SAMPLE
		sd['SetVal'] = 123456
		ss[BB_BUBBLE_SPOOF_MEDIA] = json.dumps(sd)

		if len(_speech_profile_list) > 0:
			speech_id, speech_name = random.choice(list(_speech_profile_list.items()))
			ss[BB_BUBBLE_SPOOF_SPEECH] = str(speech_id)

		#SPOOF_BATTERY
		#	Flags: (int)
		#	Values1: (int)
		#	Values2: (int)
		#	Values3: (int)
		sp = {}
		sp['Flags'] = BB_BATTERY_FLAG_BATTERY_POWER
		sp['Values1'] = 56
		sp['Values2'] = 25200
		sp['Values3'] = 3600
		ss[BB_BUBBLE_SPOOF_BATTERY] = json.dumps(sp)

		ss[BB_BUBBLE_SPOOF_NETWORK] = str(BB_NETWORK_FLAG_ETHERNET)

		bc['SpoofSettings'] = ss
		wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_CREATE, json.dumps(bc), callback)
	except Exception as e:
		print(e)
		print(traceback.format_exc())

def parse_response(res):
	global _message_cb
	global _bubble_last_insert_id
	global _bubble_running_id
	global _bubble_saved_list
	global _bubble_run_list
	global _browser_list
	global _dns_list
	global _proxy_list
	global _vpn_list
	global _speech_profile_list

	ec = BB_ERROR_GENERIC_ERROR
	msg_id = 0
	act = 0
	suba = 0
	evt = None
	callback = None

	try:
		#SERVER_RESPONSE
		#	Version: (int)
		#	ErrorCode: (int)
		#	DataType: (int)
		#	MessageID: (long)
		#	ReturnValue: (str)
		sr = json.loads(res)

		ec = sr['ErrorCode']
		msg_id = sr['MessageID']

		if sr['MessageID'] == -1:
			if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
				action = json.loads(sr['ReturnValue'])

				if action['Action'] == BB_SERVER_ACTION_STATUS:
					if action['SubAction'] == BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN:
						print(">> Browser Bubble Pro is shutting down: " + action['ValueString'])
					elif action['SubAction'] == BB_SERVER_STATUS_SUB_ACTION_LOG:
						print_log_message(action['ValueString'])

				elif action['Action'] == BB_SERVER_ACTION_BUBBLE:
					if action['SubAction'] == BB_SERVER_BUBBLE_SUB_ACTION_READY:
						#BUBBLE_LAUNCHED
						#	InstanceID: (long)
						#	BubbleID: (long)
						#	MountPoint: (str)
						#	PreLaunch: (LAUNCH_RESULT)
						#	PostLaunch: (LAUNCH_RESULT)
						bl = json.loads(action['ValueString'])
						print(">> Bubble (" + str(bl['InstanceID']) + ") is ready for use.")
						print("\tBubble ID: " + str(bl['BubbleID']))
						print("\tMount: " + bl['MountPoint'])
						lr = bl['PreLaunch']
						print("\tPre Launch")
						print("\t\tError Code: " + str(lr['ErrorCode']))
						print("\t\tEval Result: " + str(lr['Eval']))
						print("\t\tOutput: " + lr['Output'])
						lr = bl['PostLaunch']
						print("\tPost Launch")
						print("\t\tError Code: " + str(lr['ErrorCode']))
						print("\t\tEval Result: " + str(lr['Eval']))
						print("\t\tOutput: " + lr['Output'])

						# If the global options were such that network access is
						# blocked then we would eventually need to send the 
						# BB_SERVER_BUBBLE_SUB_ACTION_NETWORK command to unblock it.

					elif action['SubAction'] == BB_SERVER_BUBBLE_SUB_ACTION_FAILED:
						#BUBBLE_FAILED
						#	InstanceID: (long)
						#	ProcessId: (int)
						#	BrowserPath: (str)
						#	ErrorCode: (int)
						#	Log: (str)
						bf = json.loads(action['ValueString'])
						print(">> Bubble (" + str(bf['InstanceID']) + ") failed to load.")
						print("\tPID: " + str(bf['ProcessId']))
						print("\tPath: " + bf['BrowserPath'])
						print("\tError Code: " + str(bf['ErrorCode']))
						print("\tMessage: " + bf['Log'])
					elif action['SubAction'] == BB_SERVER_BUBBLE_SUB_ACTION_SHUTDOWN:
						#BUBBLE_SHUTDOWN
						#	InstanceID: (long)
						#	BubbleID: (long)
						#	ShutdownLaunch: (LAUNCH_RESULT)
						bs = json.loads(action['ValueString'])
						print(">> Bubble (" + str(bs['InstanceID']) + ") is shutting down.")

		elif sr['MessageID'] > 0:
			if sr['MessageID'] in _message_cb:
				act, suba, evt, callback = _message_cb[sr['MessageID']]
				del _message_cb[sr['MessageID']]

				print("<<< Received action (" + str(act) + ", " + str(suba) + ") response with message id of " + str(sr['MessageID']) + ".")

				if sr['DataType'] == BB_DATA_TYPE_STRING:
					print("\tThe operation returned: " + sr['ReturnValue'])

					if act == BB_SERVER_ACTION_BUBBLE:
						if suba == BB_SERVER_BUBBLE_SUB_ACTION_DELETE:
							_bubble_last_insert_id = 0
						elif suba == BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE:
							_bubble_running_id = 0
						#BB_SERVER_BUBBLE_SUB_ACTION_UPDATE

				elif sr['DataType'] == BB_DATA_TYPE_INTEGER:
					if act == BB_SERVER_ACTION_BUBBLE:
						if suba == BB_SERVER_BUBBLE_SUB_ACTION_CREATE:
							if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
								_bubble_last_insert_id = int(sr['ReturnValue'])
								print("\tThe new Bubble id is " + sr['ReturnValue'] + ".")

						elif suba == BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH:
							if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
								_bubble_running_id = int(sr['ReturnValue'])
								print("\tThe launched Bubble instance id is " + sr['ReturnValue'] + ".")

				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						
						if act == BB_SERVER_ACTION_BUBBLE:
							if suba == BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED:
								_bubble_saved_list = {}

								#BUBBLE_SAVED
								#	ID: (long)
								#	IsInstance: (int)
								#	Name: (str)
								#	ProfilePath: (str)
								#	BrowserID: (long)
								#	DNSID: (long)
								#	ProxyList: (list[long])
								#	VPNID: (long)
								#	Launch: (LAUNCH_ACTIONS)
								#	Options: (int)
								#	BorderColor: (str)
								#	SpoofSettings: (dict[int, str])

								bl = json.loads(sr['ReturnValue'])
								print("\tSAVED BUBBLES")
								for bs in bl:
									_bubble_saved_list[bs['ID']] = bs['Name']

									print("\t\t" + str(bs['ID']) + ": " + bs['Name'])
									print("\t\t\tBrowserID: " + str(bs['BrowserID']))
									if bs['BrowserID'] in _browser_list:
										print("\t\t\tBrowser Profile: " + _browser_list[bs['BrowserID']])

									if bs['IsInstance'] == 1:
										print("\t\t\tInstance: TRUE")
										print("\t\t\tProfile: " + bs['ProfilePath'])

									print_dns_px_vpn(bs, "\t\t\t")

									la = bs['Launch']
									if la['Pre'] != "":
										print("\t\t\tLaunch (Pre): " + la['Pre'])
									if la['Post'] != "":
										print("\t\t\tLaunch (Post): " + la['Post'])
									if la['Shutdown'] != "":
										print("\t\t\tLaunch (Shutdown): " + la['Shutdown'])

									if bs['Options'] > 0:
										print_bubble_options(bs['Options'], bs['BorderColor'], "\t\t\t")
										
									if len(bs['SpoofSettings']) > 0:
										print("\t\t\tSpoof Settings")
										for kv,js in bs['SpoofSettings'].items():
											print("\t\t\t\t" + spoof_name_lookup(kv))
								
							elif suba == BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING:
								_bubble_run_list = {}

								#BUBBLE_RUNNING
								#	InstanceID: (long)
								#	BubbleID: (long)
								#	DTG: (long)
								bl = json.loads(sr['ReturnValue'])
								print("\tRUNNING BUBBLES")
								if len(bl) == 0:
									print("\t\tNo Bubbles running.")
								else:
									for br in bl:
										_bubble_run_list[br['InstanceID']] = br['BubbleID']

										if br['BubbleID'] in _bubble_saved_list:
											print("\t\tName: " + _bubble_saved_list[br['BubbleID']])
											print("\t\t\tInstance ID: " + str(br['InstanceID']))
											print("\t\t\tDTG: " + str(br['DTG']))

							elif suba == BB_SERVER_BUBBLE_SUB_ACTION_DETAILS:
								#BUBBLE_QUERY
								#	InstanceID: (long)
								#	Name: (str)
								#	BrowserID: (long)
								#	BrowserPID: (int)
								#	DNSID: (long)
								#	ProxyList: (list[long])
								#	VPNID: (long)
								#	ProfilePath: (str)
								#	PreLaunch: (LAUNCH_RESULT)
								#	PostLaunch: (LAUNCH_RESULT)
								#	Options: (int)
								#	BorderColor: (str)
								#	SpoofSettings: (dict[int, str])

								#LAUNCH_RESULT
								#	ErrorCode: (int)
								#	Output: (str)
								#	Eval: (int)

								bq = json.loads(sr['ReturnValue'])

								print("\t" + str(bq['InstanceID']) + ": " + bq['Name'])
								print("\t\tBrowserID: " + str(bq['BrowserID']))
								if bq['BrowserID'] in _browser_list:
									print("\t\tBrowser Profile: " + _browser_list[bq['BrowserID']])
								print("\t\tBrowser PID: " + str(bq['BrowserPID']))
								print("\t\tProfile Path: " + bq['ProfilePath'])

								print_dns_px_vpn(bq, "\t\t")
								if bq['Options'] > 0:
									print_bubble_options(bq['Options'], bq['BorderColor'], "\t\t")

								if len(bq['SpoofSettings']) > 0:
									print("\t\tSpoof Settings")
									for kv,js in bq['SpoofSettings'].items():
										print("\t\t\t" + spoof_name_lookup(kv))

								lr = bq['PreLaunch']
								print("\t\tPre Launch")
								print("\t\t\tError Code: " + str(lr['ErrorCode']))
								print("\t\t\tEval Result: " + str(lr['Eval']))
								print("\t\t\tOutput: " + lr['Output'])

								lr = bq['PostLaunch']
								print("\t\tPost Launch")
								print("\t\t\tError Code: " + str(lr['ErrorCode']))
								print("\t\t\tEval Result: " + str(lr['Eval']))
								print("\t\t\tOutput: " + lr['Output'])

							elif suba == BB_SERVER_BUBBLE_SUB_ACTION_GENERATE:
								bl = json.loads(sr['ReturnValue'])
								print("\tGENERATED BUBBLE IDS")
								for id in bl:
									print("\t\t" + str(id))

						elif act == BB_SERVER_ACTION_BROWSER:
							if suba == BB_SERVER_BROWSER_SUB_ACTION_LIST:
								_browser_list = {}

								#BROWSER_PROFILE
								#	ID: (long)
								#	Name: (str)
								#	BrowserType: (int)
								#	FilePath: (str)
								#	ProfilePath: (str)
								#	Enabled: (int)
								bl = json.loads(sr['ReturnValue'])
								for br in bl:
									_browser_list[br['ID']] = br['Name']

						elif act == BB_SERVER_ACTION_DNS:
							if suba == BB_SERVER_DNS_SUB_ACTION_LIST:
								_dns_list = {}

								#DNS_SERVER
								#	ServerID: (long)
								#	ProviderID: (long)
								#	Provider: (str)
								#	Country: (str)
								#	DNSType: (int)
								#	Address: (str)
								#	Port: (int)
								dl = json.loads(sr['ReturnValue'])
								for dp in dl:
									_dns_list[dp['ProviderID']] = dp['Provider']

						elif act == BB_SERVER_ACTION_PROXY:
							if suba == BB_SERVER_PROXY_SUB_ACTION_LIST:
								_proxy_list = {}

								#PROXY_SERVER
								#	ID: (long)
								#	ProxyName: (str)
								#	Country: (COUNTRY)
								#	IP: (str)
								#	Port: (int)
								#	ProxyType: (int)
								#	Flags: (int)								
								pl = json.loads(sr['ReturnValue'])
								for px in pl:
									_proxy_list[px['ID']] = px['ProxyName']

						elif act == BB_SERVER_ACTION_VPN:
							if suba == BB_SERVER_VPN_SUB_ACTION_LIST:
								_vpn_list = {}

								#VPN_SERVER
								#	ID: (long)
								#	Provider: (str)
								#	Country: (COUNTRY)
								#	Adapter: (str)
								#	Address: (str)
								vl = json.loads(sr['ReturnValue'])
								for vp in vl:
									_vpn_list[vp['ID']] = vp['Provider']

						elif act == BB_SERVER_ACTION_SPEECH:
							if suba == BB_SERVER_SPEECH_SUB_ACTION_LIST:
								so = json.loads(sr['ReturnValue'])
								if so['Op'] == BB_SPEECH_PROFILE:
									sl = json.loads(so['Data'])
									for s in sl:
										_speech_profile_list[s['ID']] = s['Name']

						else:
							print("\t[!] Invalid or unknown Action.")
					else:
						print("\t[!] The Action was not successful.")
				else:
					print("\t[!] Unexpected data type.")
			else:
				print("[!] Invalid or unknown MessageID.")
		else:
			print("[!] Invalid or unknown MessageID.")

	except Exception as e:
		print(e)
		print(traceback.format_exc())

	if callback is not None:
		callback(2, msg_id, act, suba, ec)

	if evt is not None:
		evt.set()

def wrap_and_queue(act, suba, valstr, callback=None):
	msg_id, js = wrap_action(act, suba, valstr, callback)
	queue_for_send(msg_id, js)

def queue_for_send(msg_id, msg):
	o = {}
	o['Id'] = msg_id
	o['Data'] = msg

	_send_queue.put(o)

def send_queue_loop():
	try:
		while True:
			mo = _send_queue.get(block=True)

			msg_id = mo['Id']
			if msg_id in _message_cb:
				act,suba,evt,cb = _message_cb[msg_id]

				print(">>> Sending action (" + str(act) + ", " + str(suba) + ") with message id of " + str(msg_id) + ".")

				if cb is not None:
					cb(1, msg_id, act, suba, BB_ERROR_INVALID_MODE)

				message = mo['Data']
				_ws_app.send(message)

				#Wait for response or TODO: timeout
				evt.wait()

	except Exception as e:
		print(e)

def create_callback(w, msg_id, act, suba, errorcode):
	global _init_evt

	if w == 2 and errorcode == BB_ERROR_NO_ERROR:
		if act == BB_SERVER_ACTION_BUBBLE:
			if suba == BB_SERVER_BUBBLE_SUB_ACTION_CREATE:
				#Set our waiting event.
				_init_evt.set()

def init_callback(w, msg_id, act, suba, errorcode):
	if w == 2 and errorcode == BB_ERROR_NO_ERROR:
		if act == BB_SERVER_ACTION_BUBBLE:
			if suba == BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING:
				bubble_generate_new()
				bubble_create_new(create_callback)

def on_open(ws):
	print("[>] Connected to Browser Bubble Pro.")

	#Query for values we will use for our Bubbles.  This assumes
	#that you have already configured items.
	wrap_and_queue(BB_SERVER_ACTION_BROWSER, BB_SERVER_BROWSER_SUB_ACTION_LIST, "")
	wrap_and_queue(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_LIST, "")
	wrap_and_queue(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_LIST, "")
	wrap_and_queue(BB_SERVER_ACTION_VPN, BB_SERVER_VPN_SUB_ACTION_LIST, "")
	so = {}
	so['Op'] = BB_SPEECH_PROFILE
	so['ID'] = 0
	so['Data'] = ""
	wrap_and_queue(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))

	#Now query both saved and running Bubbles.
	wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED, "")
	wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING, "", init_callback)

def on_error(ws, error):
	print("[!] There was a websocket error.")
	print(error)
	print(traceback.format_exc())

def on_close(ws, close_status_code, close_msg):
	print("[*] The connection has been closed.")
	print("\tCode: " + str(close_status_code))
	if close_msg is not None:
		print("\tMessage: " + close_msg)

def on_message(ws, message):
	parse_response(message)

def websocket_thread():
	global _ws_app

	try:
		_thread.start_new_thread(send_queue_loop, ())

		_ws_app = websocket.WebSocketApp(BB_SERVER, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
		_ws_app.run_forever()
	except Exception as e:
		print(e)

def print_control_for_input():
	while True:
		print("Browser Bubble Pro Example")
		print("1) List Running Bubbles")
		print("2) Launch Bubble")
		print("3) Query Bubble")
		print("4) Terminate Bubble")
		print("5) Delete Bubble")
		print("6) Disconnect")

		try:
			act = int(input("Select your action... "))
		except Exception as e:
			act = 0

		if act >= 1 and act <= 6:
			print("")
			break

	return act

def next_command_callback(w, msg_id, act, suba, errorcode):
	global _next_cmd

	if w == 2:
		_next_cmd.set()

if __name__ == '__main__':
	try:
		random.seed()

		_init_evt = threading.Event()
		print("oOoOOo Browser Bubble Pro - Bubble Example oOOoOo")

		print("[>] Starting websocket thread.")
		_thread.start_new_thread(websocket_thread, ())
		
		#Wait for our initial commands to complete.
		_init_evt.wait()

		if _bubble_last_insert_id > 0:
			#Queue a command to create a shortcut.
			bubble_create_shortcut(_bubble_last_insert_id)
			#Relist to see our new Bubble
			wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED, "", next_command_callback)
			_next_cmd.wait()

			while True:
				_next_cmd.clear()

				act = print_control_for_input()
				if act == 1:
					wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING, "", next_command_callback)
					_next_cmd.wait()
				elif act == 2:
					if _bubble_last_insert_id > 0:
						#BUBBLE_LAUNCH
						#	ID: (long)
						#	IsInstance: (int)
						#	Flags: (int)
						#	Password: (str)
						#	DNSID: (long)
						#	ProxyList: (list[long])
						#	VPNID: (long)

						bl = {}
						bl['ID'] = _bubble_last_insert_id
						bl['IsInstance'] = 0
						bl['Flags'] = 0
						bl['Password'] = ""
						bl['DNSID'] = 0
						bl['ProxyList'] = []
						bl['VPNID'] = 0
						wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH, json.dumps(bl), next_command_callback)
						_next_cmd.wait()
					else:
						print("[!] The last insert Bubble ID is 0.")

				elif act == 3:
					if _bubble_running_id > 0:
						wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_DETAILS, str(_bubble_running_id), next_command_callback)
						_next_cmd.wait()
					else:
						print("[!] The last executed Bubble ID is 0.")

				elif act == 4:
					if _bubble_running_id > 0:
						#BUBBLE_TERMINATE
						#	InstanceID: (long)
						#	Wipe: (int)
						bt = {}
						bt['InstanceID'] = _bubble_running_id
						bt['Wipe'] = 0
						wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE, json.dumps(bt), next_command_callback)
						_next_cmd.wait()
					else:
						print("[!] The last executed Bubble ID is 0.")

				elif act == 5:
					if _bubble_last_insert_id > 0:
						#BUBBLE_DELETE
						#	ID: (long)
						#	IsInstance: (int)
						#	Wipe: (int)
						bd = {}
						bd['ID'] = _bubble_last_insert_id
						bd['IsInstance'] = 0
						bd['Wipe'] = 0
						wrap_and_queue(BB_SERVER_ACTION_BUBBLE, BB_SERVER_BUBBLE_SUB_ACTION_DELETE, json.dumps(bd), next_command_callback)
						_next_cmd.wait()
					else:
						print("[!] The last insert Bubble ID is 0.")

				elif act == 6:
					_ws_app.close()
					break

		else:
			print("[!] The test Bubble was not created.  Exiting...")
			_ws_app.close()

	except Exception as e:
		print(e)
		print(traceback.format_exc())

	print("[>] Example complete.")

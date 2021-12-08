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
#	This example queries Browser Bubble Pro for the list of installed browsers.
#	Expected output should be similar to this:
#
#	Brave
#   	 Name: Brave
#        Path: c:\program files (x86)\bravesoftware\brave-browser\application\brave.exe
#        Profile Path: c:\users\bubble\appdata\local\bravesoftware\brave-browser\user data\
#	Firefox
#        Name: Firefox
#        Path: c:\program files\mozilla firefox\firefox.exe
#        Profile Path: c:\users\bubble\appdata\roaming\mozilla\firefox\profiles\asdfasdf.default\
#	Firefox Nightly
#        Name: Firefox Nightly
#        Path: c:\program files\firefox nightly\firefox.exe
#        Profile Path: c:\users\bubble\appdata\roaming\mozilla\firefox\profiles\asdfasdf.default-nightly-1\
#	Chrome
#        Name: Chrome
#        Path: c:\program files (x86)\google\chrome\application\chrome.exe
#        Profile Path: c:\users\bubble\appdata\local\google\chrome\user data\
#	Edge
#        Name: Edge
#        Path: c:\program files (x86)\microsoft\edge\application\msedge.exe
#        Profile Path: c:\users\bubble\appdata\local\microsoft\edge\user data\

import websocket
import json
import traceback

# Uncomment to get websocket debug messages
#websocket.enableTrace(True)

#--------------------------------------------------------
# GLOBAL VARIABLES
#--------------------------------------------------------
_message_id = 1
_message_cb = {}
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

BB_SERVER_ACTION_BROWSER = 2
BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY = 1

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

def wrap_action(act, suba, valstr):
	global _message_id

	msgId = _message_id
	_message_id += 1
	_message_cb[msgId] = [act, suba]

	#ACTION
	a = {}
	a['Action'] = act
	a['SubAction'] = suba
	a['ValueString'] = valstr

	return wrap_with_server_request(BB_DATA_TYPE_JSON, msgId, json.dumps(a))

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

def parse_response(res):
	act = 0
	suba = 0

	try:
		#SERVER_RESPONSE
		#	Version: (int)
		#	ErrorCode: (int)
		#	DataType: (int)
		#	MessageID: (long)
		#	ReturnValue: (str)
		sr = json.loads(res)
		
		if sr['DataType'] == BB_DATA_TYPE_JSON:
			if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
				if sr['MessageID'] > 0:
					if sr['MessageID'] in _message_cb:
						act, suba = _message_cb[sr['MessageID']]
						del _message_cb[sr['MessageID']]

						if act == BB_SERVER_ACTION_BROWSER:
							if suba == BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY:
								#BROWSER_INSTALL
								#	BrowserType int
								#	BrowserName string
								#	FilePath    string
								#	ProfilePath string
								#	ProfileName string
								bl = json.loads(sr['ReturnValue'])
								for br in bl:
									bn = browser_type_to_name(br['BrowserType'])
									print(bn)
									print("\tName: " + br['BrowserName'])
									print("\tPath: " + br['FilePath'])
									print("\tProfile Path: " + br['ProfilePath'])
						else:
							print("!!! Invalid or unknown Action.")
					else:
						print("!!! Invalid or unknown MessageID.")
				else:
					print("!!! Invalid or unknown MessageID.")
			else:
				print("!!! The Action was not successful.")
		else:
			print("!!! Unexpected data type.")
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

if __name__ == '__main__':
	try:
		ws = websocket.WebSocket()
		ws.connect(BB_SERVER)

		act = wrap_action(BB_SERVER_ACTION_BROWSER, BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

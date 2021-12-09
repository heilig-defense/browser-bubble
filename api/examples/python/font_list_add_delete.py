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
#	This example sets and queries font profiles.
#

import websocket
import json
import traceback
import random

# Uncomment to get websocket debug messages
#websocket.enableTrace(True)

#--------------------------------------------------------
# GLOBAL VARIABLES
#--------------------------------------------------------
_message_id = 1
_message_cb = {}

_font_last_insert_id = 0
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

BB_SERVER_ACTION_FONT = 4
BB_SERVER_FONT_SUB_ACTION_LIST = 1
BB_SERVER_FONT_SUB_ACTION_CREATE = 2
BB_SERVER_FONT_SUB_ACTION_DELETE = 3
BB_SERVER_FONT_SUB_ACTION_UPDATE = 4
BB_SERVER_FONT_SUB_ACTION_INSTALL = 5

BB_FONT_OP_PROFILE = 1
BB_FONT_OP_FONT_ITEM = 2

BB_OS_DISABLED = 0
BB_OS_WIN7 = 1
BB_OS_WIN8 = 2
BB_OS_WIN81 = 4
BB_OS_WIN10 = 8
BB_OS_WIN11 = 16
BB_OS_CUSTOM = 32
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

	print("Sending action (" + str(act) + ", " + str(suba) + ") with message id of " + str(msgId) + ".")

	return wrap_with_server_request(BB_DATA_TYPE_JSON, msgId, json.dumps(a))

def parse_response(res):
	global _font_last_insert_id

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

		if sr['MessageID'] > 0:
			if sr['MessageID'] in _message_cb:
				act, suba = _message_cb[sr['MessageID']]
				del _message_cb[sr['MessageID']]

				print("Received action (" + str(act) + ", " + str(suba) + ") response with message id of " + str(sr['MessageID']) + ".")

				if sr['DataType'] == BB_DATA_TYPE_INTEGER:
					if act == BB_SERVER_ACTION_FONT:
						if suba == BB_SERVER_FONT_SUB_ACTION_CREATE:
							_font_last_insert_id = int(sr['ReturnValue'])
							print("The new font profile id is " + sr['ReturnValue'] + ".")

				elif sr['DataType'] == BB_DATA_TYPE_STRING:
					print("\tThe operation returned: " + sr['ReturnValue'])

				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						
						if act == BB_SERVER_ACTION_FONT:
							if suba == BB_SERVER_FONT_SUB_ACTION_LIST:
								#FONT_RESPONSE
								#	Op   int
								#	Data string
								fr = json.loads(sr['ReturnValue'])
								fl = json.loads(fr['Data'])
								if fr['Op'] == BB_FONT_OP_PROFILE:
									print("FONT PROFILES")
									for f in fl:
										print(str(f['FontID']) + ": " + f['Name'])
										for i in f['Fonts']:
											print("\t" + str(i['FontFileID']) + ": " + i['FontName'])
											print("\t\t" + i['FontPath'])
								elif fr['Op'] == BB_FONT_OP_FONT_ITEM:
									print("FONTS")
									for i in fl:
										print(str(i['FontFileID']) + ": " + i['FontName'])
										print("\t" + i['FontPath'])

						else:
							print("\t!!! Invalid or unknown Action.")
					else:
						print("\t!!! The Action was not successful.")
				else:
					print("\t!!! Unexpected data type.")
			else:
				print("!!! Invalid or unknown MessageID.")
		else:
			print("!!! Invalid or unknown MessageID.")

	except Exception as e:
		print(e)
		print(traceback.format_exc())	

if __name__ == '__main__':
	try:
		ws = websocket.WebSocket()
		ws.connect(BB_SERVER)

		#FONT_ITEM
		#	FontFileID: (long)
		#	FontName: (str)
		#	FontPath: (str)

		#FONT_PROFILE
		#	FontID: (long)
		#	Name: (str)
		#	Fonts: (list[FONT_ITEM])

		#FONT_INSTALL
		#	OS: (int)
		#	FontPath: (str)

		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_LIST, str(BB_FONT_OP_PROFILE))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		# List all installed system fonts.  System fonts are indexed
		# when Browser Bubble Pro loads for the first time (or if the
		# database needs to be rebuilt).  Fonts can be manually reindexed
		# however, it may corrupt existing profiles.
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_LIST, str(BB_FONT_OP_FONT_ITEM))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Attempt to perform a font install with an invalid folder path.
		fi = {}
		fi['OS'] = BB_OS_WIN81
		fi['FontPath'] = "e:\\invalid\\font\\path"
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_INSTALL, json.dumps(fi))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Create a new font profile.
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_CREATE, "New Font Profile #1")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List all font profiles to see the new entry.
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_LIST, str(BB_FONT_OP_PROFILE))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		# When updating a font profile, ALL existing fonts are removed and replaced with
		# the ones in the 'Fonts' field.  For this example, the FONT_ITEM values are
		# hardcoded and specific to the test machine however for a production script, 
		# these values would have to be captured based on listing output of installed fonts.	
		fl = []
		f = {}
		f['FontFileID'] = 1
		f['FontName'] = 'Arial (TrueType)'
		f['FontPath'] = 'c:\\windows\\fonts\\arial.ttf'
		fl.append(f)

		f = {}
		f['FontFileID'] = 2
		f['FontName'] = 'Arial Black (TrueType)'
		f['FontPath'] = 'c:\\windows\\fonts\\ariblk.ttf'
		fl.append(f)

		f = {}
		f['FontFileID'] = 3
		f['FontName'] = 'Arial Bold (TrueType)'
		f['FontPath'] = 'c:\\windows\\fonts\\arialbd.ttf'
		fl.append(f)

		fp = {}
		fp['FontID'] = _font_last_insert_id
		fp['Name'] = ""		#Name field is ignored for updates
		fp['Fonts'] = fl
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_UPDATE, json.dumps(fp))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now list all font profiles to see our added fonts.
		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_LIST, str(BB_FONT_OP_PROFILE))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		act = wrap_action(BB_SERVER_ACTION_FONT, BB_SERVER_FONT_SUB_ACTION_DELETE, str(_font_last_insert_id))
		ws.send(act)
		res = ws.recv()
		parse_response(res)		

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

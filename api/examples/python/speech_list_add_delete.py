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
#	This example sets and queries speech profiles and voices.  These are
#	only used if speech spoofing is enabled.
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

_speech_last_insert_id = 0
_voice_last_insert_id = 0
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

BB_SERVER_ACTION_SPEECH = 3
BB_SERVER_SPEECH_SUB_ACTION_LIST = 1
BB_SERVER_SPEECH_SUB_ACTION_CREATE = 2
BB_SERVER_SPEECH_SUB_ACTION_DELETE = 3
BB_SERVER_SPEECH_SUB_ACTION_UPDATE = 4

#SPEECH
#   Op
BB_SPEECH_PROFILE = 1
BB_SPEECH_VOICE = 2
BB_SPEECH_PROFILE_VOICES = 3

BB_SPEECH_AGE_ADULT = 1
BB_SPEECH_AGE_CHILD = 2

BB_SPEECH_SEX_FEMALE = 1
BB_SPEECH_SEX_MALE = 2
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
	global _speech_last_insert_id
	global _voice_last_insert_id

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

				if sr['DataType'] == BB_DATA_TYPE_STRING:
					print("\tThe operation returned: " + sr['ReturnValue'])

				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						
						if act == BB_SERVER_ACTION_SPEECH:
							if suba == BB_SERVER_SPEECH_SUB_ACTION_LIST:

								so = json.loads(sr['ReturnValue'])
								if so['Op'] == BB_SPEECH_PROFILE:
									sl = json.loads(so['Data'])
									print("\tSPEECH PROFILES")
									for s in sl:
										print("\t\t" + str(s['ID']) + ": " + s['Name'])

								elif so['Op'] == BB_SPEECH_VOICE:
									vl = json.loads(so['Data'])
									print("\tSPEECH VOICES")
									for v in vl:
										print("\t\t" + str(v['ID']) + ": " + v['Name'])
										print("\t\t\tAge: " + str(v['Age']))
										print("\t\t\tSex: " + str(v['Sex']))
										l = v['Language']
										print("\t\t\tLanguage: " + str(l['ID']) + " - " + l['Name'] + ", " + l['Code'])

								elif so['Op'] == BB_SPEECH_PROFILE_VOICES:
									vl = json.loads(so['Data'])
									print("\tSPEECH PROFILE VOICES")
									for v in vl:
										print("\t\t" + str(v['ID']) + ": " + v['Name'])
										print("\t\t\tAge: " + str(v['Age']))
										print("\t\t\tSex: " + str(v['Sex']))
										l = v['Language']
										print("\t\t\tLanguage: " + str(l['ID']) + " - " + l['Name'] + ", " + l['Code'])
										
							elif suba == BB_SERVER_SPEECH_SUB_ACTION_CREATE:
								so = json.loads(sr['ReturnValue'])
								if so['Op'] == BB_SPEECH_PROFILE:
									print("\tThe new speech profile id is " + str(so['ID']) + ".")
									_speech_last_insert_id = int(so['ID'])
								elif so['Op'] == BB_SPEECH_VOICE:
									print("\tThe new voice id is " + str(so['ID']) + ".")
									_voice_last_insert_id = int(so['ID'])
								elif so['Op'] == BB_SPEECH_PROFILE_VOICES:
									print("\tThe voice id " + so['Data'] + " has been added to profile profile id " + str(so['ID']) + ".")

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

		#LANGUAGE
		#	ID: (long)
		#	Name: (str)
		#	Code: (str)

		#SPEECH
		#	Op: (int)
		#	ID: (long)
		#	Data: (str)

		#SPEECH_VOICE
		#	ID: (long)
		#	Name: (str)
		#	Language: (LANGUAGE)
		#	Age: (int)
		#	Sex: (int)

		#List the current speech profiles.
		so = {}
		so['Op'] = BB_SPEECH_PROFILE
		so['ID'] = 0
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Create a new speech profile.
		so['Op'] = BB_SPEECH_PROFILE
		so['Data'] = "New Speech Profile 1"
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_CREATE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist to see the new profile.
		so['Op'] = BB_SPEECH_PROFILE
		so['ID'] = 0
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Create a new speech voice.
		l = {}
		l['ID'] = 2057
		l['Name'] = "English - United Kingdom"
		l['Code'] = "en-GB"

		sv = {}
		sv['ID'] = 0
		sv['Name'] = "Male Voice #1"
		sv['Language'] = l
		sv['Age'] = BB_SPEECH_AGE_ADULT
		sv['Sex'] = BB_SPEECH_SEX_MALE

		so['Op'] = BB_SPEECH_VOICE
		so['Data'] = json.dumps(sv)
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_CREATE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist to see the new voice.
		so['Op'] = BB_SPEECH_VOICE
		so['ID'] = 0
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		so['Op'] = BB_SPEECH_PROFILE_VOICES
		so['ID'] = _speech_last_insert_id
		so['Data'] = str(_voice_last_insert_id)
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_CREATE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist to see the voice attached to the profile.
		so['Op'] = BB_SPEECH_PROFILE_VOICES
		so['ID'] = _speech_last_insert_id
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Update the existing voice entry.
		l = {}
		l['ID'] = 1033
		l['Name'] = "English - United State"
		l['Code'] = "en-US"

		sv = {}
		sv['ID'] = _voice_last_insert_id
		sv['Name'] = "Female Voice #1"
		sv['Language'] = l
		sv['Age'] = BB_SPEECH_AGE_CHILD
		sv['Sex'] = BB_SPEECH_SEX_FEMALE

		so['Op'] = BB_SPEECH_VOICE
		so['ID'] = _voice_last_insert_id
		so['Data'] = json.dumps(sv)
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_UPDATE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List voices to see the updated entry.
		so['Op'] = BB_SPEECH_VOICE
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Delete the voice from the profile.
		so['Op'] = BB_SPEECH_PROFILE_VOICES
		so['ID'] = _speech_last_insert_id
		so['Data'] = str(_voice_last_insert_id)
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_DELETE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist to see the voice deleted from the profile.
		so['Op'] = BB_SPEECH_PROFILE_VOICES
		so['ID'] = _speech_last_insert_id
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Delete the voice.
		so['Op'] = BB_SPEECH_VOICE
		so['ID'] = _voice_last_insert_id
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_DELETE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List voices to make sure it was deleted.
		so['Op'] = BB_SPEECH_VOICE
		so['ID'] = 0
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Delete the profile.
		so['Op'] = BB_SPEECH_PROFILE
		so['ID'] = _speech_last_insert_id
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_DELETE, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List profiles to make sure it was deleted.
		so['Op'] = BB_SPEECH_PROFILE
		so['ID'] = 0
		so['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_SPEECH, BB_SERVER_SPEECH_SUB_ACTION_LIST, json.dumps(so))
		ws.send(act)
		res = ws.recv()
		parse_response(res)		

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

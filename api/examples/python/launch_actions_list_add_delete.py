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
#	This example sets and queries launch actions.
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

_action_last_insert_id = 0
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

BB_SERVER_ACTION_LAUNCH = 9
BB_SERVER_LAUNCH_SUB_ACTION_LIST = 1
BB_SERVER_LAUNCH_SUB_ACTION_CREATE = 2
BB_SERVER_LAUNCH_SUB_ACTION_DELETE = 3
BB_SERVER_LAUNCH_SUB_ACTION_UPDATE = 4

BB_LAUNCH_ACTION_OP_START_PRE = 1
BB_LAUNCH_ACTION_OP_START_POST = 2
BB_LAUNCH_ACTION_OP_START_CLOSE = 4
BB_LAUNCH_ACTION_OP_WAIT_NONE = 8
BB_LAUNCH_ACTION_OP_WAIT_COMPLETE = 16
BB_LAUNCH_ACTION_OP_WAIT_EVAL = 32
BB_LAUNCH_ACTION_OP_EVAL_IS = 64
BB_LAUNCH_ACTION_OP_EVAL_IS_NOT = 128
BB_LAUNCH_ACTION_OP_EVAL_CONTAINS = 256
BB_LAUNCH_ACTION_OP_EVAL_CONTAINS_NOT = 512
BB_LAUNCH_ACTION_OP_ACTION_CANCEL = 1024
BB_LAUNCH_ACTION_OP_ACTION_IGNORE = 2048
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
	global _action_last_insert_id

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
					if act == BB_SERVER_ACTION_LAUNCH:
						if suba == BB_SERVER_LAUNCH_SUB_ACTION_CREATE:
							_action_last_insert_id = int(sr['ReturnValue'])
							print("The new launch action id is " + sr['ReturnValue'] + ".")

				elif sr['DataType'] == BB_DATA_TYPE_STRING:
					print("\tThe operation returned: " + sr['ReturnValue'])

				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						
						if act == BB_SERVER_ACTION_LAUNCH:
							if suba == BB_SERVER_LAUNCH_SUB_ACTION_LIST:
								#LAUNCH_ACTION
								#	ID: (long)
								#	Name: (str)
								#	Flags: (int)
								#	EvalValue: (str)
								#	ProcessPath: (str)
								#	CommandLine: (str)
								#	Timeout: (int)

								lal = json.loads(sr['ReturnValue'])
								for la in lal:
									print(str(la['ID']) + ": " + la['Name'])
									print("\tProcess: " + la['ProcessPath'])
									if la['CommandLine'] != "":
										print("\tCommandLine: " + la['CommandLine'])
									print("\tFlags: " + str(la['Flags']))
									if la['Flags'] & BB_LAUNCH_ACTION_OP_START_PRE:
										print("\t\tRuns: Pre-Bubble")
									elif la['Flags'] & BB_LAUNCH_ACTION_OP_START_POST:
										print("\t\tRuns: Post-Bubble")
									elif la['Flags'] & BB_LAUNCH_ACTION_OP_START_CLOSE:
										print("\t\tRuns: Bubble Close")

									if la['Flags'] & BB_LAUNCH_ACTION_OP_WAIT_NONE:
										print("\t\tWait: None")
									elif la['Flags'] & BB_LAUNCH_ACTION_OP_WAIT_COMPLETE:
										print("\t\tWait: Complete or Timeout")
										print("\t\t\tTimeout: " + str(la['Timeout']))
									elif la['Flags'] & BB_LAUNCH_ACTION_OP_WAIT_EVAL:
										print("\t\tWait: Complete and Eval or Timeout")
										print("\t\t\tTimeout: " + str(la['Timeout']))
										print("\t\t\tEval Value: " + la['EvalValue'])

										if la['Flags'] & BB_LAUNCH_ACTION_OP_EVAL_IS:
											print("\t\t\t\tEval Condition: IS")
										elif la['Flags'] & BB_LAUNCH_ACTION_OP_EVAL_IS_NOT:
											print("\t\t\t\tEval Condition: IS NOT")
										elif la['Flags'] & BB_LAUNCH_ACTION_OP_EVAL_CONTAINS:
											print("\t\t\t\tEval Condition: CONTAINS")
										elif la['Flags'] & BB_LAUNCH_ACTION_OP_EVAL_CONTAINS_NOT:
											print("\t\t\t\tEval Condition: CONTAINS NOT")

										if la['Flags'] & BB_LAUNCH_ACTION_OP_ACTION_CANCEL:
											print("\t\t\t\tEval Action: Cancel")
										elif la['Flags'] & BB_LAUNCH_ACTION_OP_ACTION_IGNORE:
											print("\t\t\t\tEval Action: Ignore")

									print("\tEval Value: " + la['EvalValue'])

							else:
								print("\t!!! Invalid or unknown Sub-Action.")
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

		#LAUNCH_ACTION
		#	ID: (long)
		#	Name: (str)
		#	Flags: (int)
		#	EvalValue: (str)
		#	ProcessPath: (str)
		#	CommandLine: (str)
		#	Timeout: (int)

		#List the current launch actions.
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		la = {}
		la['ID'] = 0
		la['Name'] = "New Launch Action 1"
		la['Flags'] = BB_LAUNCH_ACTION_OP_START_PRE | BB_LAUNCH_ACTION_OP_WAIT_EVAL | BB_LAUNCH_ACTION_OP_EVAL_CONTAINS | BB_LAUNCH_ACTION_OP_ACTION_IGNORE
		la['EvalValue'] = "Notepad Eval Value"
		la['ProcessPath'] = "c:\\windows\\notepad.exe"
		la['CommandLine'] = ""
		la['Timeout'] = 10
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_CREATE, json.dumps(la))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist to see the newly added launch action.
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Update the launch action.
		la = {}
		la['ID'] = _action_last_insert_id
		la['Name'] = "New Launch Action 1"
		la['Flags'] = BB_LAUNCH_ACTION_OP_START_POST | BB_LAUNCH_ACTION_OP_WAIT_EVAL | BB_LAUNCH_ACTION_OP_EVAL_CONTAINS_NOT | BB_LAUNCH_ACTION_OP_ACTION_CANCEL
		la['EvalValue'] = "Wordpad Eval Value"
		la['ProcessPath'] = "c:\\windows\\wordpad.exe"
		la['CommandLine'] = "newfile.rtf"
		la['Timeout'] = 15
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_UPDATE, json.dumps(la))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Relist launch actions to examine the update.
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Delete the launch action.
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_DELETE, str(_action_last_insert_id))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
						
		#Finally relist to ensure it was deleted.
		act = wrap_action(BB_SERVER_ACTION_LAUNCH, BB_SERVER_LAUNCH_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

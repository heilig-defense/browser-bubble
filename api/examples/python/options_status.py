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
#	This example sets and queries global option values and status.
#

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

_ops_dns = 0
_ops_aex = 0
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

BB_SERVER_ACTION_STATUS = 0
BB_SERVER_STATUS_SUB_ACTION_CURRENT = 1
BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN = 2
BB_SERVER_STATUS_SUB_ACTION_LOG = 3

BB_SERVER_ACTION_OPTIONS = 1
BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE = 1
BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE = 2
BB_SERVER_OPTIONS_SUB_ACTION_REINIT = 3

#OPTIONS_XET
#   Op
BB_OPTIONS_XET_FLAGS = 1
BB_OPTIONS_XET_LICENSE = 2
BB_OPTIONS_XET_ADAPTER = 3
BB_OPTIONS_XET_ADAPTER_LIST = 4
BB_OPTIONS_XET_GLOBAL_DNS = 5
BB_OPTIONS_XET_GLOBAL_AEX = 6

#   SubOp (XET_FLAGS)
BB_OPTIONS_FLAG_AUTO_BUBBLE = 1
BB_OPTIONS_FLAG_BLOCK_NET = 2
BB_OPTIONS_FLAG_TERMINATE_ON_EXIT = 4
BB_OPTIONS_FLAG_DELETE_PROFILE = 8
BB_OPTIONS_FLAG_USE_VHD_SANDBOX = 16
BB_OPTIONS_FLAG_VERBOSE_DNS_LOG = 32

#LICENSE FLAGS
BB_LICENSE_STATUS_INVALID = 0
BB_LICENSE_STATUS_VALID = 1
BB_LICENSE_STATUS_TRIAL = 2
BB_LICENSE_STATUS_EXPIRED = 3
BB_LICENSE_STATUS_REVOKED = 4

#LOG LEVEL FLAGS
BB_LOG_LEVEL_DEBUG = 1
BB_LOG_LEVEL_ERROR = 2
BB_LOG_LEVEL_INFO = 3
BB_LOG_LEVEL_WARN = 4
BB_LOG_LEVEL_PRIORITY = 5
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

def print_current_status(s):
	#STATUS
	#	License: (int)
	#	Drivers: (int)
	#	Browsers: (int)
	#	Options: (int)
	#	InitErrors: (dict[int, str])
	#	Update: (int)
	#	UpdateVersion: (str)
	#	UpdateMessage: (str)
	#	SavedBubbles: (int)
	#	RunningBubbles: (int)
	stat = json.loads(s)
	print(stat)

	print(">>> CURRENT STATUS <<<")
	if stat['Browsers'] == BB_ERROR_NO_ERROR:
		print("\tBrowsers: OK")
	else:
		print("\tBrowsers: Error (" + str(stat['Browsers']) + ")")

	if stat['Drivers'] == BB_ERROR_NO_ERROR:
		print("\tDrivers: OK")
	else:
		print("\tDrivers: Error (" + str(stat['Drivers']) + ")")

	if stat['License'] == BB_ERROR_NO_ERROR:
		print("\tLicense: OK")
	else:
		print("\tLicense: Error (" + str(stat['License']) + ")")

	if stat['Options'] == BB_ERROR_NO_ERROR:
		print("\tOptions: OK")
	else:
		print("\tOptions: Error (" + str(stat['Options']) + ")")

	print("\tUpdate: " + str(stat['Update']))
	if stat['Update'] == 1:
		print("\t\tNew Version: " + stat['UpdateVersion'])
		if stat['UpdateMessage'] != "":
			print("\t\tMessage: " + stat['UpdateMessage'])

	print("\tSaved Bubbles: " + str(stat['SavedBubbles']))
	print("\tRunning Bubbles: " + str(stat['RunningBubbles']))

	if len(stat['InitErrors']) > 0:
		print("\tInitialization Errors")
		for key, value in stat['InitErrors'].items():
			print("\t\t" + str(key) + ": " + value)

def parse_response(res):
	global _ops_aex
	global _ops_dns

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

		if sr['MessageID'] == -1:
			action = json.loads(sr['ReturnValue'])
			if action['Action'] == BB_SERVER_ACTION_STATUS:
				if action['SubAction'] == BB_SERVER_STATUS_SUB_ACTION_LOG:
					print_log_message(action['ValueString'])
				elif action['SubAction'] == BB_SERVER_STATUS_SUB_ACTION_CURRENT:
					print_current_status(action['ValueString'])
				elif action['SubAction'] == BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN:
					print("Browser Bubble Pro is shutting down.")

		elif sr['MessageID'] > 0:
			print("Received action (" + str(act) + ", " + str(suba) + ") response with message id of " + str(sr['MessageID']) + ".")

			if sr['MessageID'] in _message_cb:
				act, suba = _message_cb[sr['MessageID']]
				del _message_cb[sr['MessageID']]

				if sr['DataType'] == BB_DATA_TYPE_STRING:
					if act == BB_SERVER_ACTION_STATUS:
						if suba == BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN:
							print("\tThe shutdown command returned: " + sr['ReturnValue'])
					elif act == BB_SERVER_ACTION_OPTIONS:
						if suba == BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE:
							print("\tThe set options command returned an error code of " + str(sr['ErrorCode']) + ".")
							print("\t\t" + sr['ReturnValue'])
				
				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:

						if act == BB_SERVER_ACTION_STATUS:
							if suba == BB_SERVER_STATUS_SUB_ACTION_CURRENT:
								print_current_status(sr['ReturnValue'])

						elif act == BB_SERVER_ACTION_OPTIONS:
							#OPTIONS_XET
							#	Op: (int)
							#	SubOp: (int)
							#	Data: (str)
							ops = json.loads(sr['ReturnValue'])
							if suba == BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE:
								if ops['Op'] == BB_OPTIONS_XET_FLAGS:
									print("\tOptions flags set.")
								elif ops['Op'] == BB_OPTIONS_XET_LICENSE:
									print("\tLicense key set.")
								elif ops['Op'] == BB_OPTIONS_XET_ADAPTER:
									print("\tNetwork adapater set.")
								elif ops['Op'] == BB_OPTIONS_XET_GLOBAL_AEX:
									print("\tGlobal anti-exploit protection option set.")
								elif ops['Op'] == BB_OPTIONS_XET_GLOBAL_DNS:
									print("\tGlobal DNS option set.")
										
							elif suba == BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE:
								if ops['Op'] == BB_OPTIONS_XET_FLAGS:
									flg = ops['SubOp']

									print("\tOPTION FLAGS")
									if flg == 0:
										print("\t\tNo options set")
									else:
										if flg & BB_OPTIONS_FLAG_AUTO_BUBBLE:
											print("\t\tAuto Bubble browsers: TRUE")
										if flg & BB_OPTIONS_FLAG_BLOCK_NET:
											print("\t\tBlock browser network access: TRUE")
										if flg & BB_OPTIONS_FLAG_TERMINATE_ON_EXIT:
											print("\t\tClose browsers on Browser Bubble exit: TRUE")
										if flg & BB_OPTIONS_FLAG_DELETE_PROFILE:
											print("\t\tAuto delete browser data: TRUE")
										if flg & BB_OPTIONS_FLAG_USE_VHD_SANDBOX:
											print("\t\tVHD sandbox: TRUE")
										if flg & BB_OPTIONS_FLAG_VERBOSE_DNS_LOG:
											print("\t\tDNS logging: TRUE")

								elif ops['Op'] == BB_OPTIONS_XET_LICENSE:
									#LICENSE
									#	LicenseKey: (str)
									#	Status: (int)
									#	Expires: (str)
									#	Entitlements: (int)
									#	EndpointCount: (int)									
									lic = json.loads(ops['Data'])

									print("\tLICENSE")
									print("\t\tKey: " + lic['LicenseKey'])
									if lic['Status'] == BB_LICENSE_STATUS_INVALID:
										print("\t\tStatus: Invalid")
									elif lic['Status'] == BB_LICENSE_STATUS_VALID:
										print("\t\tStatus: Valid")
									elif lic['Status'] == BB_LICENSE_STATUS_TRIAL:
										print("\t\tStatus: Trial")
									elif lic['Status'] == BB_LICENSE_STATUS_EXPIRED:
										print("\t\tStatus: Expired")
									elif lic['Status'] == BB_LICENSE_STATUS_REVOKED:
										print("\t\tStatus: Revoked")
									print("\t\tExpires: " + lic['Expires'])
									print("\t\tEndpoints: " + str(lic['EndpointCount']))
								elif ops['Op'] == BB_OPTIONS_XET_ADAPTER:
									#ADAPTER
									#	Name: (str)
									#	MAC: (str)
									#	IP4: (str)
									#	IP6: (str)
									#	Gateway: (dict[str, str])
									#	IsDefault (int)
									#	IsWifi: (int)

									na = json.loads(ops['Data'])						
									print("\tDefault Network Adapter")
									print("\t\t" + na['Name'])
									print("\t\t\t" + na['MAC'])
									print("\t\t\t" + na['IP4'])
								elif ops['Op'] == BB_OPTIONS_XET_ADAPTER_LIST:
									nal = json.loads(ops['Data'])
									for na in nal:
										print("\t" + na['Name'])
										print("\t\t" + na['MAC'])
										print("\t\t" + na['IP4'])
								elif ops['Op'] == BB_OPTIONS_XET_GLOBAL_DNS:
									if ops['SubOp'] == 1:
										print("\tDNS: TRUE")
										_ops_dns = 1
									else:
										print("\tDNS: FALSE")
										_ops_dns = 0
								elif ops['Op'] == BB_OPTIONS_XET_GLOBAL_AEX:
									if ops['SubOp'] == 1:
										print("\tAnti-Exploit: TRUE")
										_ops_aex = 1
									else:
										print("\tAnti-Exploit: FALSE")
										_ops_aex = 0
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

		#Query current status.
		act = wrap_action(BB_SERVER_ACTION_STATUS, BB_SERVER_STATUS_SUB_ACTION_CURRENT, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Query global options.

		#OPTIONS_XET
		#	Op: (int)
		#	SubOp: (int)
		#	Data: (str)
		ops = {}
		ops['Op'] = BB_OPTIONS_XET_FLAGS
		ops['SubOp'] = 0
		ops['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		ops['Op'] = BB_OPTIONS_XET_LICENSE
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		ops['Op'] = BB_OPTIONS_XET_ADAPTER
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		ops['Op'] = BB_OPTIONS_XET_ADAPTER_LIST
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		ops['Op'] = BB_OPTIONS_XET_GLOBAL_DNS
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		ops['Op'] = BB_OPTIONS_XET_GLOBAL_AEX
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Set global options.

		#Toggle DNS filtering
		ops['Op'] = BB_OPTIONS_XET_GLOBAL_DNS
		ops['SubOp'] = 1 if _ops_dns == 0 else 0
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		#Toggle anti-exploit
		ops['Op'] = BB_OPTIONS_XET_GLOBAL_AEX
		ops['SubOp'] = 1 if _ops_aex == 0 else 0
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)
		
		#Set the license key.  The license is not verified with this
		#command.  It simply writes the key to the registry.  It will
		#be validated the next time Browser Bubble starts or when the
		#BB_SERVER_OPTIONS_SUB_ACTION_REINIT command is sent (assuming
		#that initialization was not intially successful).  If Browser
		#Bubble Pro already initialized, then re-init has no effect.
		ops['Op'] = BB_OPTIONS_XET_LICENSE
		ops['SubOp'] = 0
		ops['Data'] = "INVALID LICENSE KEY"
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Shutdown Browser Bubble Pro
		act = wrap_action(BB_SERVER_ACTION_STATUS, BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN, "shutdown")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

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
#	This example sets and queries proxy and VPN entries.
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

_adapter_list = []
_proxy_last_insert_id = 0
_vpn_last_insert_id = 0
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

BB_SERVER_ACTION_PROXY = 6
BB_SERVER_PROXY_SUB_ACTION_LIST = 1
BB_SERVER_PROXY_SUB_ACTION_CREATE = 2
BB_SERVER_PROXY_SUB_ACTION_DELETE = 3
BB_SERVER_PROXY_SUB_ACTION_UPDATE = 4

BB_SERVER_ACTION_VPN = 7
BB_SERVER_VPN_SUB_ACTION_LIST = 1
BB_SERVER_VPN_SUB_ACTION_CREATE = 2
BB_SERVER_VPN_SUB_ACTION_DELETE = 3
BB_SERVER_VPN_SUB_ACTION_UPDATE = 4

#OPTIONS_XET
#   Op
BB_OPTIONS_XET_FLAGS = 1
BB_OPTIONS_XET_LICENSE = 2
BB_OPTIONS_XET_ADAPTER = 3
BB_OPTIONS_XET_ADAPTER_LIST = 4
BB_OPTIONS_XET_GLOBAL_DNS = 5
BB_OPTIONS_XET_GLOBAL_AEX = 6

#PROXY TYPE FLAGS
BB_PROXY_TYPE_HTTPS = 1
BB_PROXY_TYPE_SOCKS4 = 2
BB_PROXY_TYPE_SOCKS5 = 3

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

def parse_response(res):
	global _proxy_last_insert_id
	global _vpn_last_insert_id

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

		elif sr['MessageID'] > 0:
			print("Received action (" + str(act) + ", " + str(suba) + ") response with message id of " + str(sr['MessageID']) + ".")

			if sr['MessageID'] in _message_cb:
				act, suba = _message_cb[sr['MessageID']]
				del _message_cb[sr['MessageID']]

				if sr['DataType'] == BB_DATA_TYPE_STRING:
					print("\tThe operation returned: " + sr['ReturnValue'])					
				elif sr['DataType'] == BB_DATA_TYPE_INTEGER:
					if act == BB_SERVER_ACTION_PROXY:
						if suba == BB_SERVER_PROXY_SUB_ACTION_CREATE:
							_proxy_last_insert_id = int(sr['ReturnValue'])
							print("\tThe new proxy ID is " + sr['ReturnValue'] + ".")
					elif act == BB_SERVER_ACTION_VPN:
						if suba == BB_SERVER_VPN_SUB_ACTION_CREATE:
							_vpn_last_insert_id = int(sr['ReturnValue'])
							print("\tThe new VPN ID is " + sr['ReturnValue'] + ".")

				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						
						if act == BB_SERVER_ACTION_OPTIONS:
							if suba == BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE:
								ops = json.loads(sr['ReturnValue'])

								if ops['Op'] == BB_OPTIONS_XET_ADAPTER_LIST:
									nal = json.loads(ops['Data'])
									for na in nal:
										_adapter_list.append(na)

										print("\t" + na['Name'])
										print("\t\t" + na['MAC'])
										print("\t\t" + na['IP4'])

						elif act == BB_SERVER_ACTION_PROXY:
							if suba == BB_SERVER_PROXY_SUB_ACTION_LIST:
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
									print("\t" + str(px['ID']) + ": " + px['ProxyName'])
									print("\t\tAddress: " + px['IP'] + ":" + str(px['Port']))
									c = px['Country']
									print("\t\tCountry: " + c['Code'] + " - " + c['Name'])
									if px['ProxyType'] == BB_PROXY_TYPE_HTTPS:
										print("\t\tProxy Type: HTTPS")
									elif px['ProxyType'] == BB_PROXY_TYPE_SOCKS4:
										print("\t\tProxy Type: SOCKS4")
									elif px['ProxyType'] == BB_PROXY_TYPE_SOCKS5:
										print("\t\tProxy Type: SOCKS5")
									
						elif act == BB_SERVER_ACTION_VPN:
							if suba == BB_SERVER_VPN_SUB_ACTION_LIST:
								#VPN_SERVER
								#	ID: (long)
								#	Provider: (str)
								#	Country: (COUNTRY)
								#	Adapter: (str)
								#	Address: (str)
								vl = json.loads(sr['ReturnValue'])
								for vp in vl:
									print("\t" + str(vp['ID']) + ": " + vp['Provider'])
									print("\t\tAdapter: " + vp['Adapter'])
									print("\t\tAddress: " + vp['Address'])
									c = vp['Country']
									print("\t\tCountry: " + c['Code'] + " - " + c['Name'])

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

		#First we need to query the list of network adapters on the system
		#for when we create a new VPN entry.  For this example, it will just
		#pick a random adapter from the list but for a production script,
		#you will need to use the correct adapter associated with your VPN solution.

		#OPTIONS_XET
		#	Op: (int)
		#	SubOp: (int)
		#	Data: (str)
		ops = {}
		ops['Op'] = BB_OPTIONS_XET_ADAPTER_LIST
		ops['SubOp'] = 0
		ops['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_OPTIONS, BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE, json.dumps(ops))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		print("### PROXY ###")

		#List current proxies.
		act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#COUNTRY
		#	Code: (str)	
		#	Name: (str)	

		#PROXY_SERVER
		#	ID: (long)
		#	ProxyName: (str)
		#	Country: (COUNTRY)
		#	IP: (str)
		#	Port: (int)
		#	ProxyType: (int)
		#	Flags: (int)

		#Create a new proxy server item.
		c = {}
		c['Code'] = "DE"
		c['Name'] = "Germany"

		px = {}
		px['ID'] = 0
		px['ProxyName'] = "Test Proxy 1"
		px['Country'] = c
		px['IP'] = "127.0.0.1"
		px['Port'] = 8081
		px['ProxyType'] = BB_PROXY_TYPE_SOCKS5
		px['Flags'] = 0
		act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_CREATE, json.dumps(px))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List proxies to view our addition.
		act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		if _proxy_last_insert_id > 0:
			px['ID'] = _proxy_last_insert_id
			px['ProxyName'] = "Test Proxy 1"
			px['Country'] = c
			px['IP'] = "127.0.0.2"
			px['Port'] = 8082
			px['ProxyType'] = BB_PROXY_TYPE_SOCKS5
			px['Flags'] = 0
			act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_UPDATE, json.dumps(px))
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#List proxies to view our update.
			act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_LIST, "")
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#Delete our added proxy.
			act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_DELETE, str(_proxy_last_insert_id))
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#List proxies one last time.
			act = wrap_action(BB_SERVER_ACTION_PROXY, BB_SERVER_PROXY_SUB_ACTION_LIST, "")
			ws.send(act)
			res = ws.recv()
			parse_response(res)
		else:
			print("The last proxy insert ID is not valid.")

		#------------------------------------------------------------

		print("### VPN ###")

		#List current VPNs.
		act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_VPN_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#VPN_SERVER
		#	ID: (long)
		#	Provider: (str)
		#	Country: (COUNTRY)
		#	Adapter: (str)
		#	Address: (str)

		netadapter = random.choice(_adapter_list)

		#Add a new VPN entry.
		vpn = {}
		vpn['ID'] = 0
		vpn['Provider'] = "Test VPN 1"
		vpn['Country'] = c
		vpn['Adapter'] = netadapter['Name']
		vpn['Address'] = "" #Address is ignored
		act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_PROXY_SUB_ACTION_CREATE, json.dumps(vpn))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List VPNs to view our addition.
		act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_VPN_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		if _vpn_last_insert_id > 0:
			c['Code'] = "US"
			c['Name'] = "United States"
			
			#Update the VPN entry.
			vpn['ID'] = _vpn_last_insert_id
			vpn['Provider'] = "Test VPN 1"
			vpn['Country'] = c
			vpn['Adapter'] = netadapter['Name']
			vpn['Address'] = "" #Address is ignored
			act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_PROXY_SUB_ACTION_UPDATE, json.dumps(vpn))
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#List VPNs to view our update.
			act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_VPN_SUB_ACTION_LIST, "")
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#Delete our added VPN.
			act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_PROXY_SUB_ACTION_DELETE, str(_vpn_last_insert_id))
			ws.send(act)
			res = ws.recv()
			parse_response(res)

			#List VPNs one last time.
			act = wrap_action(BB_SERVER_ACTION_VPN, BB_SERVER_VPN_SUB_ACTION_LIST, "")
			ws.send(act)
			res = ws.recv()
			parse_response(res)
		else:
			print("The last VPN insert ID is not valid.")

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

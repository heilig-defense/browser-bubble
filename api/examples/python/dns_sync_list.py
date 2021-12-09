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
#	This example tests various DNS related commands from syncing providers and sinkholes
#	to adding and removing new entries and listing and searching.
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

_dns_last_inset_id = 0
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

BB_SERVER_ACTION_DNS = 5
BB_SERVER_DNS_SUB_ACTION_SYNC = 1
BB_SERVER_DNS_SUB_ACTION_LIST = 2
BB_SERVER_DNS_SUB_ACTION_CREATE = 3
BB_SERVER_DNS_SUB_ACTION_DELETE = 4
BB_SERVER_DNS_SUB_ACTION_UPDATE = 5
BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH = 6

BB_DNS_TYPE_DNS_OVER_TLS = 1
BB_DNS_TYPE_DNS_OVER_HTTPS = 2
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
	global _dns_last_inset_id

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
					if act == BB_SERVER_ACTION_DNS:
						if suba == BB_SERVER_DNS_SUB_ACTION_SYNC:
							print("\tThe DNS sync operation returned: " + sr['ReturnValue'])
						elif suba == BB_SERVER_DNS_SUB_ACTION_DELETE:
							print("\tThe DNS delete operation returned: " + sr['ReturnValue'])
						else:
							print("\t!!! Invalid or unknown Sub-Action.")
					else:
						print("\t!!! Invalid or unknown Action.")

				elif sr['DataType'] == BB_DATA_TYPE_INTEGER:
					if act == BB_SERVER_ACTION_DNS:
						if suba == BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH:
							fnd = sr['ReturnValue']
							tf = "FALSE"
							if fnd == "1":
								tf = "TRUE"
							print("\tSinkhole value found: " + tf)
						else:
							print("\t!!! Invalid or unknown Sub-Action.")
					else:
						print("\t!!! Invalid or unknown Action.")
							
				elif sr['DataType'] == BB_DATA_TYPE_JSON:
					if sr['ErrorCode'] == BB_ERROR_NO_ERROR:
						if act == BB_SERVER_ACTION_DNS:
							if suba == BB_SERVER_DNS_SUB_ACTION_LIST:
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
									print("\t" + str(dp['ServerID']) + ": " + dp['Address'])
									print("\t\tProviderID: " + str(dp['tProviderID']))
									print("\t\tProvider: " + dp['Provider'])
									print("\t\tCountry: " + dp['Country'])
									if dp['DNSType'] == BB_DNS_TYPE_DNS_OVER_TLS:
										print("\t\tPort: " + str(dp['Port']))
										print("\t\tType: DNS-Over-TLS")
									else:
										print("\t\tType: DNS-Over-HTTPS")
							elif suba == BB_SERVER_DNS_SUB_ACTION_CREATE:
								dop = json.loads(sr['ReturnValue'])
								if dop['DNS'] == 1:
									print("\tThe new DNS server has an ID value of " + str(dop['ID']) + ".")
									_dns_last_inset_id = dop['ID']
								else:
									print("\tThe DNS sinkhole entry has been added.")

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

		#DNS_OP
		#	DNS (int)
		#	ID (long)
		#	Data (str)
		dns = {}
		dns['DNS'] = 1
		dns['ID'] = 0
		dns['Data'] = ""
		#First sync DNS providers.
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_SYNC, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List all DNS servers.
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now create a new DNS server entry
		#DNS_SERVER
		#	ServerID: (long)
		#	ProviderID: (long)
		#	Provider: (str)
		#	Country: (str)
		#	DNSType: (int)
		#	Address: (str)
		#	Port: (int)
		svr = {}
		svr['ServerID'] = 0
		#Either the ProviderID or Provider name 
		#field must be valid.
		svr['ProviderID'] = 0
		svr['Provider'] = "CyDec Security"
		svr['Country'] = "US"
		svr['DNSType'] = BB_DNS_TYPE_DNS_OVER_HTTPS
		svr['Address'] = "https://dns.cydecsecurity.com/dns-query"
		svr['Port'] = 443

		dns['DNS'] = 1
		dns['Data'] = json.dumps(svr)
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_CREATE, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List all servers to make sure the new entry is there.
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now try to delete a server with an invalid ID.
		dns['DNS'] = 1
		dns['ID'] = -1
		dns['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_DELETE, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now delete the new server.
		dns['DNS'] = 1
		dns['ID'] = _dns_last_inset_id
		dns['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_DELETE, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#List all servers one last time.
		dns['ID'] = 0
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_LIST, "")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now sync DNS sinkholes.
		dns['DNS'] = 0
		dns['ID'] = 0
		dns['Data'] = ""
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_SYNC, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Add new sinkhole item.
		dns['DNS'] = 0
		dns['Data'] = "facebook.com"
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_CREATE, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now search sinkholes for our added domain.
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH, "facebook.com")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Delete the sinkhole item.
		dns['DNS'] = 0
		dns['Data'] = "facebook.com"
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_DELETE, json.dumps(dns))
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		#Now search sinkholes for our deleted domain.
		act = wrap_action(BB_SERVER_ACTION_DNS, BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH, "facebook.com")
		ws.send(act)
		res = ws.recv()
		parse_response(res)

		ws.close()
	except Exception as e:
		print(e)
		print(traceback.format_exc())	

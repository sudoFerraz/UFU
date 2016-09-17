#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import socket
import sys
import thread
import urlparse
import threading

databaseDict = {}
currentKeyNumber = 1
lock = threading.Lock()

def message200ok(key, value):
	msg = """HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>200 OK</title>
		</head><body>
		<h1>Key: """ + str(key) + """</h1>
		<p>Value: """ + value + """</p>
		</body></html>"""
	return msg

def message201Created(key, value):
	msg = """HTTP/1.1 201 Created\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>201 Created</title>
		</head><body>
		<h1>Key: """ + str(key) + """</h1>
		<p>Value: """ + value + """</p>
		</body></html>"""
	return msg

def message204NoContent():
	msg = """HTTP/1.0 204 No Content\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>204 No Content</title>
		</head><body>
		<h1>Success</h1>
		</body></html>"""
	return msg

def message400BadRequest():
	msg = """HTTP/1.0 400 Bad Request\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>400 Bad Request</title>
		</head><body>
		<h1>Bad Request</h1>
		<p>Your request was invalid.</p>
		</body></html>"""
	return msg

def message404NotFound(key):
	msg = """HTTP/1.0 404 Not Found\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>404 Not Found</title>
		</head><body>
		<h1>Not Found</h1>
		<p>The requested Key """ + str(key) + """ was not found on this server.</p>
		</body></html>"""
	return msg

def message501NotImplemented():
	msg = """HTTP/1.0 501 Not Implemented\nContent-Type: text/html\nConnection: Closed\r\n\r\n
		<!DOCTYPE HTML PUBLIC>
		<html><head>
		<title>501 Not Implemented</title>
		</head><body>
		<h1>Not Implemented</h1>
		<p>The server does not support the functionality required to fulfill the request.</p>
		</body></html>"""
	return msg

def queryGET(key):
	if key in databaseDict:
		return databaseDict[key]
	else:
		return None

def queryPOST(key, value):
	global databaseDict
	if key in databaseDict:
		return False
	else:
		databaseDict[key] = value
		return True

def queryPUT(key, value):
	global databaseDict
	if key in databaseDict:
		databaseDict[key] = value
		return databaseDict[key]
	else:
		return None

def queryDELETE(key):
	global databaseDict
	if key in databaseDict:
		del databaseDict[key]
		return True
	else:
		return False

def executeGET(clientsocket, dataString):
	key = dataString[1].replace('/', '')
	if not key.isdigit():
		clientsocket.sendall(message400BadRequest()) # OK
	else:
		key = int(key)
		with lock:
			queryResult = queryGET(key)
			if queryResult is not None:
				clientsocket.sendall(queryResult) #OK
			else:
				clientsocket.sendall(message404NotFound(key)) # OK

def executePOST(clientsocket, dataString):
	key = dataString[1].replace('/', '')
	if not key.isdigit():
		clientsocket.sendall(message400BadRequest())

	else:
		#TODO put in a new method
		postData = dataString[-1].split('&')
		dataToBeInserted = None
		for data in postData:
			if data.split('=')[0] == 'data':
				dataToBeInserted = urlparse.parse_qs(data)['data'][0]
				break
		#TODO ver se checagem esta correta
		if dataToBeInserted is not None and len(dataToBeInserted) <= 1000:
			#TODO sincronizar mutex
			with lock:
				key = int(key)
				global currentKeyNumber
				returnValue = queryPOST(key, dataToBeInserted)
				if returnValue == True:
					clientsocket.sendall(message201Created(key, dataToBeInserted)) #OK
				else:
					clientsocket.sendall(message400BadRequest())
		else:
			clientsocket.sendall(message400BadRequest()) #OK

def executePUT(clientsocket, dataString):
	key = dataString[1].replace('/', '')
	if not key.isdigit():
		clientsocket.sendall(message400BadRequest())
	else:
		putData = dataString[-1].split('&')
		modifiedData = None
		for data in putData:
			if data.split('=')[0] == 'data':
				modifiedData = urlparse.parse_qs(data)['data'][0]
				break
		#TODO sincronizar mutex
		if modifiedData is not None and len(modifiedData) <= 1000:
			with lock:
				key = int(key)
				queryResult = queryPUT(key, modifiedData)
				if queryResult is not None:
					clientsocket.sendall(message200ok(key, queryResult)) # OK
				else:
					clientsocket.sendall(message404NotFound(key)) #nao achou a key retorna 404
		else:
			clientsocket.sendall(message400BadRequest()) #OK

def executeDELETE(clientsocket, dataString):
	key = dataString[1].replace('/', '')
	if not key.isdigit():
		clientsocket.sendall(message400BadRequest())
	else:
		key = int(key)
		#TODO sincronizar mutex
		with lock:
			queryResult = queryDELETE(key)
			if queryResult == True:
				clientsocket.sendall(message204NoContent()) #OK
			else:
				clientsocket.sendall(message404NotFound(key)) #OK

def communicateWithClient(clientsocket, address):
	clientsocket.settimeout(0.2)
	print "Connection from: " + str(address)

	data = ''
	while True:
		try:
			data += clientsocket.recv(1024)
		except socket.timeout , e:
			break

	if data == '':
		print("Error: Failed to receive message from " + str(address))
		return

	splittedRequest = splitHTTPRequest(str(data))
	if splittedRequest[0] == "GET":
		executeGET(clientsocket, splittedRequest)

	elif splittedRequest[0] == "POST":
		executePOST(clientsocket, splittedRequest)

	elif splittedRequest[0] == "PUT":
		executePUT(clientsocket, splittedRequest)

	elif splittedRequest[0] == "DELETE":
		executeDELETE(clientsocket, splittedRequest)
	else:
		clientsocket.sendall(message501NotImplemented())

	clientsocket.close()

def splitHTTPRequest(dataString):
	parsedRequest = dataString.replace('\r', '')
	parsedRequest = parsedRequest.replace('\n', ' ')
	return parsedRequest.split(' ')

def main():
	parser = argparse.ArgumentParser(description='Begin Connection.')
	parser.add_argument("port",help='port number',type=int)
	args = parser.parse_args()

	port = args.port

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) ## reuse previous address
	serversocket.bind(('localhost', port))

	print("Waiting ...\n")
	serversocket.listen(10)

	while True:
		(clientsocket, address) = serversocket.accept()
		try:
		   thread.start_new_thread(communicateWithClient, (clientsocket, address))
		except:
		   print "Error: unable to start thread"

main()

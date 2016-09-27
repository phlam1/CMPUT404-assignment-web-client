#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
	from urlparse import urlparse
	input_parse = urlparse(url)

	#test
	print("scheme= " + input_parse.scheme + "\n")
	print("Network location= " + input_parse.netloc + "\n")
	print("port= " + str(input_parse.port) + "\n")
	print("host name= " + input_parse.hostname + "\n")
	print("path= " + input_parse.path + "\n")
	print("query= " + input_parse.query + "\n")

	return input_parse.port

    def connect(self, host, port):
        # use sockets!

	#code from lab2
	clientSocket.bind(("0.0.0.0",8001))
	clientSocket = socket.socket((host,port), socket.SOCK_STREAM)
	clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
	(incomingSocket, address) = clientSocket.accept()
	print "we got a connetion from %s!" % (str(address))

        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
	return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
		#test
		print("command= " + command + "\n")
		print("url= " + url + "\n")
		print("args= " + str(args) + "\n")
		host_port = self.get_host_port(url)

		print("host_port= " + str(host_port) + "\n")
		
		return self.POST( url, args )
        else:

		#test
		print("command= " + command + "\n")
		print("url= " + url + "\n")
		print("args= " + str(args) + "\n")
       
		host_port = self.get_host_port(url)

		print("host_port= " + str(host_port) + "\n")

	     	return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   

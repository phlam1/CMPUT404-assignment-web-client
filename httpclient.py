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
    def __init__(self, code=500, body="Server Error"):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        from urlparse import urlparse
        input_url = urlparse(url)

        return input_url.port, input_url.hostname, input_url.path, input_url.query
        
    def connect(self, host, port=80):
        # use sockets!
        #code from lab2

    	self.destinationSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	try:
    		self.destinationSocket.connect((host,port))
    	except Exception as e:
    		self.code = 404
    	self.destinationSocket.setblocking(0)
    	
    	self.destinationSocket.sendall(self.full_request)
        self.recvall(self.destinationSocket)
        return None

    def get_code(self, data):
    	code_line = data.split()
    	self.code = int(code_line[1])
        return None

    def get_headers(self,data):
    	#returns response headers
    	index = data.split("\r\n\r\n")
    	self.headers = index[0]
        return None

    def get_body(self, data):
    	index = data.split("\r\n\r\n")
    	self.body = index[1]
    	

    # read everything from the socket
    def recvall(self, sock):
    
    	#test
        buffer = bytearray()
        done = False
        while not done:
            skip = False
            try:
            	part = sock.recv(1024)
            except socket.error, exception:
            	if exception.errno == 11:
            		skip = True
            	else:
            		self.code = 404
            if not skip:
            	if (part):
                	buffer.extend(part)
            	else:
                	done = not part
        self.data = str(buffer)

    def GET(self, url, args=None):
    	port, host, path, query  = self.get_host_port(url)
        if path == "" or path == "/":
        	req = 'GET / HTTP/1.1\r\n'
        else:
            	req = 'GET /' + path + ' HTTP/1.1\r\n'
        headers = "User-Agent: HTTPclient\r\n" + "Host: " + host + "\r\n" + "Accept: */*\r\n\r\n"
    
        #set up default port
        if (port == None):
        	port = 80
            
        self.full_request = req + headers
        self.connect(host, port)
        print(self.data)
        self.get_code(self.data)
        self.get_body(self.data)
        self.get_headers(self.data)
        return HTTPResponse(self.code, self.body)
        
        
    def POST(self, url, args=None):
    	port, host, path, query  = self.get_host_port(url)
    	
    	if (args != None):
    		encoded = urllib.urlencode(args)
    		headers = "User-Agent: HTTPclient\r\n" + "Host: " + host + "\r\n" + "Accept: */*\r\n" + "Content-Length: " + str(len(encoded)) + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + encoded
    	else:
    		headers = "User-Agent: HTTPclient\r\n" + "Host: " + host + "\r\n" + "Accept: */*\r\n" + "Content-Length: 0\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n\r\n"

        if path == "" or path == "/":
        	req = 'POST / HTTP/1.1\r\n'
        else:
            	req = 'POST /' + path + ' HTTP/1.1\r\n'

        #headers = "User-Agent:  \r\n" + "Host: " + host + "\r\n" + "Accept: */*\r\n\r\n"
    
        #set up default port
        if (port == None):
        	port = 80
            
        self.full_request = req + headers
        self.connect(host, port)
        print(self.data)
        self.get_code(self.data)
        self.get_body(self.data)
        self.get_headers(self.data)
        return HTTPResponse(self.code, self.body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
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



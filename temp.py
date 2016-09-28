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
        input_url = urlparse(url)
        host = input_url.hostname
        if input_url.port:
            port = input_url.port
        else:
            port = 80
        return host, port

    def connect(self, host, port):
        # use sockets!
        print "This is the port " + str(port) + " This is the host " + str(host) + "\n"

    	destinationSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	destinationSocket.connect((host,int(port)))
        
        return destinationSocket

    def get_code(self, data):
    	code_line = data.split()
    	print("get_code --> " + str(code_line[1]) + "\n")
    	self.code = code_line[1]
        return None

    #Still need to implement
    def get_headers(self,data):
        return None

    def get_body(self, data):
        full = data.split("/r/n/r/n")
        body = data[1]
	print ("get_body --> " + body)
        return body

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
        host, port = self.get_host_port(url)
        print "This is the port " + str(port) +  " This is the host " + str(host) + "\n"
        req = "GET" + ' / ' + host + ' ' + 'HTTP/1.1\r\n'
        headers = "Content-Type: application/x-www-form-urlencoded\r\n" + "Host: " + host + "\r\n" + "Accept: */*\r\n" + "\r\n"
        full_request = req + headers
        d_socket = self.connect(host, port)
        data = self.recvall(d_socket)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        return HTTPResponse(code, body)

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

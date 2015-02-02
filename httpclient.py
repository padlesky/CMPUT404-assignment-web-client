#!/usr/bin/env python
# coding: utf-8
# Copyright 2015 Pranjali Pokharel, Aaron Padlesky
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
#import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):

        #creating initial socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as msg:
            print 'Failed to create socket. Error code:' +str(msg[0])+ ' , Error message: ' + msg[1]
            sys.exit()
        
        print 'Socket Created'

        try:
            remote_ip = socket.gethostbyname(host)

        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        print 'Ip address of ' + host + ' is ' + remote_ip

        #Connect to remote server
        s.connect((remote_ip, port))
        print 'Socket Connected to ' + host + ' on ip ' + remote_ip
        return s

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
        urlInfo = urlparse(url)
        port = urlInfo.port
        if port == None:
            port = 80
        netLocation = urlInfo.netloc
        tempHost = netLocation.split(':')
        host = tempHost[0]
        if host == None:
            host = 'localhost'
        serverSocket = self.connect(host, port)
        serverSocket.send("GET HTTP/1.1\r\n")
        serverSocket.send("Host: %s\r\n\n" %host)
        self.data = serverSocket.recv(1024).strip()
        code = 500
        print self.data
        body = ""
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, command, url, args=None):
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
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    

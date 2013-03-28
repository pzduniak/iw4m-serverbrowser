# FourDeltaOne.net masterserver query
# Quake3 protocol reader
# Author: FaceHunter
# Slightly modified by Orange

import socket
import struct
import collections
import select
import sys

sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP

def GetServers():
	iplist = []
	list = []
	errlist = []
	UDP_IP = "iw4.prod.fourdeltaone.net"
	UDP_PORT = 20810
	MESSAGE = "\xFF\xFF\xFF\xFFgetservers IW4 61586 full empty\x00"

	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	while 1:
		data = sock.recv(5000)
		if data:
			a = data.split("\\")
			for x in a:
				if len(x) != 6:
					errlist.append( "ERROR: %s %i" % (x, len(x)) )
				else:
					list.append(x)
		if "EOT" in data:
			break
	for x in list[1:]:
		x = x.strip("\\")
		try:
			b = struct.unpack("!BBBBBB",x)
			iplist.append(str(b[0])+"."+str(b[1])+"."+str(b[2])+"."+str(b[3])+":"+str(int(b[4])*256+int(b[5])))
		except struct.error as e:
			errlist.append( "ERROR: "+str(e.args[0])+" "+str(len(x)) )
	return iplist
	
def GetInfo(ip,port):

	UDP_IP = ip
	UDP_PORT = port
	MESSAGE = "\xFF\xFF\xFF\xFFgetinfo\x00"

	try:
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		ready = select.select([sock], [], [], 4)
		if ready[0]:
			data = sock.recv(4096)
			try:
				hostname = data.split("hostname\\")[1].split("\\")[0]
				gametype = data.split("gametype\\")[1].split("\\")[0]
				clients = data.split("clients\\")[1].split("\\")[0]
				mapname = data.split("mapname\\")[1].split("\\")[0]
				hardcore = data.split("hc\\")[1].split("\\")[0]
				version = data.split("shortversion\\")[1].split("\\")[0]
				maxclients = data.split("sv_maxclients\\")[1].split("\\")[0]
				#fs_game = data.split("fs_game\\")[1].split("\\")[0]
				address = ip + ":" + str(port)

				return {"hostname":hostname, "gametype":gametype, "clients":clients, "mapname":mapname, "hardcore":hardcore,"version":version,"maxclients":maxclients,"address":address} #"fs_game":fs_game
			except:
				return False
		else:
			return False
	except socket.error, msg:
		return False
		
def GetPlayers(ip,port):

	UDP_IP = ip
	UDP_PORT = port
	MESSAGE = "\xFF\xFF\xFF\xFFgetstatus\x00"

	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	ready = select.select([sock], [], [], 5)
	if ready[0]:
		data = sock.recv(4096)
		nicklist = []
		a = data.split('\n')
		for x in a[2:]:
			try:
				x = x.split('"')[1].split('"')[0]
				nicklist.append(x)
			except:
				pass
		return nicklist
	else:
		return False
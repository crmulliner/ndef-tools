#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import sys
import bluetooth

class CollinsBtNfcAdapter:
	def __init__(self, bdaddr = None, channel = 25):
		self.__channel = channel
		self.__bdaddr = bdaddr
		self.__sock = None
		self.__data = None
		self.__uid = None
		
	def setChannel(self, channel):
		self.__channel = channel
		
	def setBdaddr(self, bdaddr):
		self.__bdaddr = bdaddr
		
	def connect(self):
		self.__sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.__sock.connect((self.__bdaddr, self.__channel))
		
	def disconnect(self):
		if self.__sock != None:
			self.__sock.close()
	
	def __parseReadTag(self, data):
		if data == None or len(data) <= 0:
			self.__data = None
			return None
		# ugly hack
		lines = data.splitlines(0)
		l = lines[2].split(":")
		l1 = l[1].strip("\n")
		self.__data = l1
	
	def __readTag(self):
		send_data = "8\nReadTag\n"
		self.__sock.send(send_data)
		reading = 1
		rd = ""
		while (reading):
			rd = rd + self.__sock.recv(1024)
			if rd.find("\n") != -1:
				lines = rd.splitlines(0)
				rlen = int(lines[0])
			if len(rd) == rlen + len(lines[0]) + 1:
				reading = 0
			if rlen == 0:
				return None
		recv_data = ""
		return rd
	
	def readTag(self):
		trying = 2
		while (trying):
			if self.__sock != None:
				data = self.__readTag()
				if trying == 0:
					self.disconnect()
				self.__parseReadTag(data)
				return self.__data
			else:
				self.connect()
			trying = trying - 1
		return None
	
	def __writeTag(self, data):
		send_data = "WriteTag\nDATA:" + data + "\n"
		sd_len = str(len(send_data)) + "\n"
		# ugly hack, needed for strange behavior of Nokia 6212 classic
		self.__sock.settimeout(1)
		self.__sock.sendall(sd_len)
		self.__sock.sendall("WriteTag\n")
		self.__sock.sendall("DATA:" + data + "\n")
		try:
			self.__sock.recv(1)
		except bluetooth.btcommon.BluetoothError:
			pass
		
		
	def writeTag(self, data):
		trying = 2
		while (trying):
			if self.__sock != None:
				self.__writeTag(data)
				if trying == 0:
					self.disconnect()
				return 1
			else:
				self.connect()
			trying = trying - 1
		return 0
		
	def quickWrite(self, data, bdaddr, channel):
		self.setChannel(channel)
		self.setBdaddr(bdaddr)
		d = self.writeTag(data)
		self.disconnect()
		return d
			
	def quickRead(self, bdaddr, channel):
		self.setChannel(channel)
		self.setBdaddr(bdaddr)
		d = self.readTag()
		self.disconnect()
		return d

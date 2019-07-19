#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import Utils
import NDEFMessage

class NokiaBluetoothTag:
	def __init__(self):
		self.__my_type = "nokia.com:bt"
		self.__my_tnf = 0x04
		self.__conf = 0
		self.__bdaddr = "00:00:00:00:00:00"
		self.__cod = 0x000680
		self.__shortname = "NokiaBluetoothTag"
		self.__authinfo = None
	
	def getTnf(self):
		return self.__my_tnf
	
	def getType(self):
		return self.__my_type
		
	def setConfiguration(self, conf):
		self.__conf = conf
		
	def getConfiguration(self):
		return self.__conf
		
	def setBdaddr(self, bdaddr):
		self.__bdaddr = bdaddr

	def getBdaddr(self):
		return self.__bdaddr
		
	def __bdaddr2bin(self):
		b = ""
		b = b + chr(Utils.fromHex(self.__bdaddr[0:2]))
		b = b + chr(Utils.fromHex(self.__bdaddr[3:5]))
		b = b + chr(Utils.fromHex(self.__bdaddr[6:8]))
		b = b + chr(Utils.fromHex(self.__bdaddr[9:11]))
		b = b + chr(Utils.fromHex(self.__bdaddr[12:14]))
		b = b + chr(Utils.fromHex(self.__bdaddr[15:17]))
		return b
		
	def setClassOfDevice(self, cod):
		self.__cod = cod
		
	def setAuthInfo(self, authinfo):
		self.__authinfo = authinfo
		
	def setShortName(self, name):
		self.__shortname = name
	
	def getClassOfDevice(self):
		return self.__cod
		
	def getAuthInfo(self):
		return self.__authinfo
		
	def getShortName(self):
		return self.__shortname
		
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setType(self.__my_type)
		rec.setTnf(self.__my_tnf)
		payload = ""
		payload = payload + chr(self.__conf & 0xFF)
		payload = payload + self.__bdaddr2bin()
		payload = payload + chr(self.__cod >> 16 & 0xFF)
		payload = payload + chr(self.__cod >> 8 & 0xFF)
		payload = payload + chr(self.__cod & 0xFF)
		if self.__authinfo != None:
			payload = payload + self.__authinfo
		else:
			for i in range(0, 16):
				payload = payload + chr(0)
		l = len(self.__shortname)
		payload = payload + chr(l & 0xFF)
		#print str(ord(chr(l & 0xFF)))
		payload = payload + self.__shortname
		rec.setPayload(payload)
		return rec
	
	def __parsePayload(self, payload):
		self.__conf = ord(payload[0])
		pp = 1
		self.__bdaddr = ""
		for i in range(0, 6):
			self.__bdaddr = self.__bdaddr + Utils.toHex(ord(payload[pp+i]))
			if i < 5:
				self.__bdaddr = self.__bdaddr + ":"
		pp = pp + 6
		self.__cod = (ord(payload[pp]) << 16) | (ord(payload[pp + 1]) << 8) | ord(payload[pp + 2])
		pp = pp + 3
		self.__authinfo = []
		for i in range(0, 16):
			self.__authinfo.append(payload[pp])
			pp = pp + 1
		ls = ord(payload[pp])
		pp = pp + 1
		self.__shortname = ""
		for i in range(0, ls):
			self.__shortname = self.__shortname + payload[pp]
			pp = pp + 1
	
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayload()
			self.__parsePayload(payload)


# for testing
if __name__ == "__main__":
	t1 = NokiaBluetoothTag()
	t1.setBdaddr("00:11:22:33:44:55")
	t1.setShortName("123 Test Bla 321")
	t1.setConfiguration(55)
	t1.setClassOfDevice(0x112233)
	t1.setAuthInfo("1234567890123456")
	rt1 = t1.getNDEFRecord()
	rt2 = NokiaBluetoothTag()
	rt2.fromRawData(rt1.getHex(), 1)
	print rt2.getBdaddr()
	print rt2.getConfiguration()
	print rt2.getClassOfDevice()
	print rt2.getShortName()
	print rt2.getAuthInfo()

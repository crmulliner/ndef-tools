#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import Utils
import NDEFMessage

#
# This is incomplete, the station frequency is not yet converted
# feel free to implement the conversion
# what are the two zeros (0) at the end of the payload for??
#

class NokiaRadiostationTag:
	def __init__(self, station = None, name = None):
		self.__my_type = "nokia.com:rf"
		self.__my_tnf = 0x04
		self.__station = station
		self.__name = name
	
	def getTnf(self):
		return self.__my_tnf
	
	def getType(self):
		return self.__my_type
		
	def setStation(self, station):
		self.__station = station

	def getStation(self):
		return self.__station
		
	def setName(self, name):
		self.__name = name

	def getName(self):
		return self.__name
		
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setType(self.__my_type)
		rec.setTnf(self.__my_tnf)
		payload = self.__station + self.__name + chr(0) + chr(0)
		rec.setPayload(payload)
		return rec
	
	def __parsePayload(self, payload):
		self.__station = payload[0:3]
		self.__name = payload[3:len(payload)-2]
	
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayload()
			self.__parsePayload(payload)


# for testing
if __name__ == "__main__":
	t1 = NokiaRadiostationTag(chr(1)+chr(2)+chr(3),"Test Station")
	rt1 = t1.getNDEFRecord()
	t2 = NokiaRadiostationTag()
	t2.fromRawData(rt1.getHex(), 1)
	print t1.getStation()
	print t2.getName()

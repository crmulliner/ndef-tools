#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import Utils
import NDEFMessage

class NokiaProfileTag:
	def __init__(self, profile = None):
		self.__my_type = "nokia.com:pf"
		self.__my_tnf = 0x04
		self.__profile = profile
	
	def getTnf(self):
		return self.__my_tnf
	
	def getType(self):
		return self.__my_type
		
	def setProfile(self, profile):
		self.__profile = profile

	def getProfile(self):
		return self.__profile
		
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setType(self.__my_type)
		rec.setTnf(self.__my_tnf)
		payload = chr(self.__profile)
		rec.setPayload(payload)
		return rec
	
	def __parsePayload(self, payload):
		if type(payload) == int or len(payload) >= 1:
			self.__profile = payload
	
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayload()
			self.__parsePayload(payload)


# for testing
if __name__ == "__main__":
	t1 = NokiaProfileTag(2)
	rt1 = t1.getNDEFRecord()
	t2 = NokiaProfileTag()
	t2.fromRawData(rt1.getHex(), 1)
	print t1.getProfile()
	print ord(t2.getProfile())

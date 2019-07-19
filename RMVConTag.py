#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NDEFMessage
import Utils

class RMVConTag:
	def __init__(self):
		self.__my_tnf = 0x04
		self.__my_type = "rmv.de:hst"
		self.__raw_data = []
		self.__station_id = 0
		self.__len = 0
		self.__station_name_len = 0
		self.__station_name = ""
		self.__tag_sig_len = 0
		self.__tag_sig = []
		self.__valid = 0
		
	def getTnf(self):
		return self.__my_tnf
		
	def getType(self):
		return self.__my_type
		
	def isValid(self):
		return self.__valid
	
	def setLength(self, length):
		self.__len = length
		
	def getLength(self):
		return self.__len
	
	def getStationId(self):
		return self.__station_id

	def setStationId(self, sid):
		self.__station_id = sid

	def getStationName(self):
		return self.__station_name
		
	def setStationName(self, name):
		self.__station_name = name
		self.__station_name_len = len(name)
		
	def setStationNameLength(self, length):
		self.__station_name_len = length
		
	def getStationNameLength(self):
		return self.__station_name_len
		
	def getSignature(self):
		return self.__tag_sig
		
	def setSignature(self, sig):
		self.__tag_sig = sig
		self.__tag_sig_len = len(sig)
		
	def getSignatureLen(self):
		return self.__tag_sig_len
		
	def setSignatureLen(self, length):
		self.__tag_sig_len = length

	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			self.__raw_data = rec.getPayload()
			self.__parseRaw()
	
	# ugly hack
	def cmp(self, a, b):
		if type(a) == int and type(b) == int:
			return a == b
		elif type(a) == int and type(b) == chr:
			return a == ord(b)
		elif type(b) == int and type(a) == chr:
			return b == ord(a)
	
	def __parseRaw(self):
		self.__valid = 1
		# -- static bytes --
		if self.cmp(self.__raw_data[0], 1):
			print "byte 0 is "# + str(ord(self.__raw_data[0])) + " should be 0x01"
			self.__valid = 0
		if self.cmp(self.__raw_data[1], 5):
			print "byte 1 is " #+ str(ord(self.__raw_data[1])) + " should be 0x05"
			self.__valid = 0
		if self.cmp(self.__raw_data[7], 2):
			print "byte 7 is " #+ str(ord(self.__raw_data[7])) + " should be 0x02"
			self.__valid = 0
		# - station id -
		self.__station_id = (ord(self.__raw_data[2]) * 0x10000) + (ord(self.__raw_data[3]) << 8) + ord(self.__raw_data[4])
		#print "Station ID: " + str(self.__station_id)
		# length offset for signature
		self.__len = (ord(self.__raw_data[5]) << 8) | ord(self.__raw_data[6])
		print self.__len
		# - station name -
		self.__station_name = ""
		self.__station_name_len = ord(self.__raw_data[8])
		#print "Station Name Length: " + str(self.__station_name_len)
		for i in range(9, 9 + self.__station_name_len):
			self.__station_name = self.__station_name + self.__raw_data[i]
		#print "Station Name: " + self.__station_name
		p = 9 + self.__station_name_len
		# -- static value --
		if ord(self.__raw_data[p]) != 3:
			print "byte " + str(p) + " is " + str(ord(self.__raw_data[p])) + " should be 3"
			self.__valid = 0
		p = p + 1
		self.__tag_sig_len = ord(self.__raw_data[p])
		p = p + 1
		#print str(len(self.__raw_data) - self.__tag_sig_len)
		#print str(p) + " " + str(self.__tag_sig_len) + " " + str(len(self.__raw_data))
		for i in range(p, p + self.__tag_sig_len):
			self.__tag_sig.append(self.__raw_data[i])
			
	def getNDEFRecord(self):
		if self.__len == 0:
			self.__len = 2 + 3 + 2 + 1 + 1 + len(self.__station_name) + 1 + 1 + 1
			#print "Len: " + str(self.__len)
		payload = []
		# static
		payload.append(0x01)
		payload.append(0x05)
		#print payload
		# station id
		payload.append((self.__station_id / 0x10000) & 0xFF)
		payload.append(((self.__station_id % 0x10000) / 256) & 0xFF)
		payload.append(((self.__station_id % 0x10000) % 256) & 0xFF)
		# length offset
		print self.__len
		self.__len = len(self.__station_name) + 1
		print self.__len
		payload.append((self.__len >> 8) & 0xFF)
		payload.append(self.__len & 0xFF)
		# static
		payload.append(0x02)
		# station name length
		payload.append(self.__station_name_len & 0xFF)
		# station name
		for i in range(0, len(self.__station_name)):
			payload.append(self.__station_name[i])
		# static
		payload.append(0x03)
		# sig len
		payload.append(chr(self.__tag_sig_len & 0xFF))
		# sig
		for i in range(0, len(self.__tag_sig)):
			payload.append(self.__tag_sig[i])
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		rec.setPayload(payload)
		return rec

if __name__ == "__main__":
	import NDEFUri
	
	# Frankfurt am Main - Konstablerwache
	#data = "940A9A726D762E64653A68737401052DC8BE001B020F4B6F6E737461626C6572776163686503800DAA47F6D9B877CD7356FF303BE5F9DE069E6F53BF214C4BFC319C9A0B8D513C62D797C00F258FE4C5EB02998F31E516446314A19B5B581BCBD54BBE75A6D6F061A1761CBECA7A70D71C503598AB79CF4B1409E9DA536F34DF9CA65ED5DB4A0352570671FCF1CD191268161CD8C35ED64C4F9FD256C9B07D2C9D50BA0266AAAD51012B55037761702E726D762E64652F6D6F62696C2F7461672F726571756573742E646F3F69643D33303030353130"

	# FFM HbF
	data = "940A97726D762E64653A68737401052DC6CA000D020C48617570746261686E686F66038018EA317E90DACAAEBD011AE1CF27245CCE82C66CE80A19AA5B691D2A62E7D0D9CB1F7FDF012B9CF8D1BFDCB653086F1DC0D5B022B21CEB75A1C2AE9D7220AD68CD998015B36ED830CF8DDFCC790E7125198D5FB6FCD2EC36E0F6FBD5C466A6CE73AC2C47135D90ED02D5B6ABB026708AED237777A41C8E83B5B630F042D7F21351012B55037761702E726D762E64652F6D6F62696C2F7461672F726571756573742E646F3F69643D33303030303130"

	print "Tag size: " + str(len(data)/2)
	m = NDEFMessage.NDEFMessage()
	m.fromRawData(data, 1)
	print "Message has " + str(m.getNumRecords()) + " Records"
	for i in range(0, m.getNumRecords()):
		r = m.getRecord(i)
		print "Record payload " + str(i) + " is size " + str(len(r.getPayload()))
		print " Type: " + r.getType()
		print " Tnf: 0x" + str(r.getTnf())
		if r.getType() == "U":
			u = NDEFUri.NDEFUri()
			u.fromRawData(r.getHex(), 1)
			ab = NDEFUri.NDEFUriAbbreviation()
			print " " + ab.getName(u.getAbbreviation()) + u.getUri()
		elif r.getType() == "rmv.de:hst":
			p = r.getPayload()
			o = ""
			o2 = ""
			for i in range(0, len(p)):
				if ord(p[i]) > ord("A") and ord(p[i]) < ord("z"):
					o = " " + o + p[i]
					#o2 = o2 + "  "
				else:
					o = o + "  "
				o2 = o2 + Utils.toHex(ord(p[i]))
			r1 = RMVConTag()
			r1.fromRawData(r.getHex(), 1)
			print "Statio ID: " + str(r1.getStationId())
			print "Station Name: " + r1.getStationName()
			r2 = RMVConTag()
			r2.setStationId(r1.getStationId())
			r2.setStationName(r1.getStationName())
			r2.setSignature(r1.getSignature())
			rr2 = r2.getNDEFRecord()
			rr2.setME(0)
			if rr2.getHex() == r.getHex():
				print "Tags equal"
			else:
				print "something went wrong!"

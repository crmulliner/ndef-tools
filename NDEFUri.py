#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NDEFMessage

class NDEFUriAbbreviation:
	def __init__(self):
		self.__ab = []
		self.__ab.append("http://www.")
		self.__ab.append("https://www.")
		self.__ab.append("http://")
		self.__ab.append("https://")
		self.__ab.append("tel:")
		self.__ab.append("mailto:")
		self.__ab.append("ftp://anonymous:anonymous@")
		self.__ab.append("ftp://ftp.")
		self.__ab.append("ftps://")
		self.__ab.append("sftp://")
		self.__ab.append("smb://")
		self.__ab.append("nfs://")
		self.__ab.append("ftp://")
		self.__ab.append("dav://")
		self.__ab.append("news:")
		self.__ab.append("telnet://")
		self.__ab.append("imap:")
		self.__ab.append("rtsp://")
		self.__ab.append("urn:")
		self.__ab.append("pop:")
		self.__ab.append("sip:")
		self.__ab.append("sips:")
		self.__ab.append("tftp:")
		self.__ab.append("btspp://")
		self.__ab.append("btl2cap://")
		self.__ab.append("btgoep://")
		self.__ab.append("tcpobex://")
		self.__ab.append("irdaobex://")
		self.__ab.append("file://")
		self.__ab.append("urn:epc:id:")
		self.__ab.append("urn:epc:tag:")
		self.__ab.append("urn:epc:pat:")
		self.__ab.append("urn:epc:raw:")
		self.__ab.append("urn:epc")
		self.__ab.append("urn:nfc:")
		
		self.Nokia_Gallery = 29;
	
	def getAbbreviation(self, name):
		bigm = -1
		for i in range(0, len(self.__ab)):
			if name.startswith(self.__ab[i]):
				if bigm != -1:
					if len(self.__ab[i]) > len(self.__ab[bigm]):
						#print "+" + self.__ab[i]
						bigm = i
				else:
					#print ": " + self.__ab[i]
					bigm = i
		if bigm != -1:
			return bigm + 1
		else:
			return 0
		
	def getName(self, ab):
		if ab == 29:
			return "Nokia Gallery (protocol identifier unknown)"
		if ab > 0 and ab < len(self.__ab):
			return self.__ab[ab-1]
		else:
			return ""

class NDEFUri:
	def __init__(self):
		self.__uri = None
		self.__abbreviation = 0
		self.__my_type = "U"
		self.__my_tnf = 0x01
	
	def getType(self):
		return self.__my_type
		
	def getTnf(self):
		return self.__my_tnf
	
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayload()
			if len(payload) > 0:
				self.__abbreviation = ord(payload[0])
			self.__uri = ""
			for i in range(1, len(payload)):
				self.__uri = self.__uri + payload[i]
	
	def do(self, uri):
		ab = NDEFUriAbbreviation()
		abn = ab.getAbbreviation(uri)
		self.setAbbreviation(abn)
		if abn == 0:
			self.setUri(uri)
		else:
			self.setUri(uri[len(ab.getName(abn)):])
		return self.getNDEFRecord()
	
	def doFull(self, uri, abbreviation):
		self.setUri(uri)
		self.abbreviation(abbreviation)
		return self.getNDEFRecord()
	
	def getUri(self):
		return self.__uri
		
	def setUri(self, uri):
		self.__uri = uri

	def abbreviate(self):
		ab = NDEFUriAbbreviation()
		abn = ab.getAbbreviation(self.__uri)
		self.setAbbreviation(abn)
		print str(abn)
		if abn != 0:
			self.setUri(self.__uri[len(ab.getName(abn)):])

	def setAbbreviation(self, abbreviation):
		self.__abbreviation = abbreviation
		
	def getAbbreviation(self):
		return self.__abbreviation
		
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		payload = chr(self.__abbreviation)
		payload = payload + str(self.__uri)
		rec.setPayload(payload)
		return rec
		
if __name__ == "__main__":
	ab = NDEFUriAbbreviation()
	print str(ab.getAbbreviation("nfs://"))
	print ab.getName(4)

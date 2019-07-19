#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NDEFMessage

class NDEFTextRecord:
	def __init__(self):
		self.__language_code = "en"
		self.__text = ""
		self.__my_type = "T"
		self.__my_tnf = 0x01
		self.__utf16 = 0;
	
	def doFull(self, text, lang):
		self.setText(text)
		self.setLanguage(lang)
		return self.getNDEFRecord()

	def do(self, text):
		self.setText(text)
		return self.getNDEFRecord()
	
	def isUtf16(self):
		return self.__utf16

	def setUtf16(self, yes = 1):
		self.__utf16 = yes
	
	def getType(self):
		return self.__my_type
		
	def getTnf(self):
		return self.__my_tnf
	
	def setText(self, text):
		self.__text = text
		
	def getText(self):
		return self.__text
		
	def setLanguage(self, lang):
		self.__language_code = lang
		
	def getLanguage(self):
		return self.__language_code
		
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		payload = chr((len(self.__language_code)) | (self.__utf16 << 7))
		payload = payload + self.__language_code
		payload = payload + str(self.__text)
		rec.setPayload(payload)
		return rec

	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayload()
			if (ord(payload[0]) & 0x80):
				self.__utf16 = 1
			llen = ord(payload[0]) & 0x7F
			self.__language_code = ""
			for i in range(1, llen + 1):
				self.__language_code = self.__language_code + payload[i]
			pos = 1 + llen
			self.__text = ""
			for i in range(pos, len(payload)):
				#if ord(payload[i]) < 127 and ord(payload[i]) > 32:
				self.__text = self.__text + payload[i]
				#else:
				#	self.__text = self.__text + "."

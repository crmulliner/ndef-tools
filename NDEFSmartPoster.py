#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NDEFMessage
import NDEFUri
import NDEFTextRecord

class NDEFSpAction:
	def __init__(self):
		self.__action = None
		self.__my_type = "act"
		self.__my_tnf = 0x01

	def getTnf(self):
		return self.__my_tnf

	def getType(self):
		return self.__my_type
		
	def setAction(self, act):
		self.__action = act
		
	def getAction(self):
		return self.__action
		
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayloadRaw()
			if len(payload) == 1:
				self.__action = payload[0]
	
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		rec.setPayload(chr(self.__action))
		return rec

class NDEFSpType:
	def __init__(self):
		self.__type = None
		self.__my_type = "t"
		self.__my_tnf = 0x01

	def getTnf(self):
		return self.__my_tnf

	def getType(self):
		return self.__my_type
		
	def setType(self, sptype):
		self.__type = sptype
		
	def getType(self):
		return self.__type
		
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayloadRaw()
			#print payload
			self.__type = ""
			for i in range(0, len(payload)):
				self.__type = self.__type + chr(payload[i])
	
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		rec.setPayload(self.__type)
		return rec

class NDEFSpSize:
	def __init__(self):
		self.__size = 0
		self.__my_type = "s"
		self.__my_tnf = 0x01

	def getTnf(self):
		return self.__my_tnf

	def getType(self):
		return self.__my_type
		
	def setSize(self, s):
		self.__size = s
		
	def getSize(self):
		return self.__size
		
	def fromRawData(self, raw_data, raw_is_hex):
		rec = NDEFMessage.NDEFRecord()
		rec.fromRawData(raw_data, raw_is_hex)
		if rec.getType() == self.__my_type:
			payload = rec.getPayloadRaw()
			if len(payload) == 4:
				self.__size = payload[0] << 24 | payload[1] << 16 | payload[2] << 8 | payload[3]
			else:
				self.__size = 0
	
	def getNDEFRecord(self):
		rec = NDEFMessage.NDEFRecord()
		rec.setTnf(self.__my_tnf)
		rec.setType(self.__my_type)
		payload = []
		payload.append((self.__size >> 24) & 0xFF)
		payload.append((self.__size >> 16) & 0xFF)
		payload.append((self.__size >> 8) & 0xFF)
		payload.append(self.__size & 0xFF)
		rec.setPayload(payload)
		return rec

class NDEFSmartPoster:
	def __init__(self):
		self.__uri = None
		self.__title = ""
		self.__action = None
		self.__type_info = None
		self.__size_info = None
		self.__uri_rec = None
		self.__title_rec = None
		self.__action_rec = None
		self.__type_rec = None
		self.__size_rec = None
		self.__language_code = "en"
		self.__records = []
		self.__my_type = "Sp"
		self.__my_tnf = 0x01
		
	def getType(self):
		return self.__my_type
		
	def getTnf(self):
		return self.__my_tnf
		
	def setUri(self, uri):
		self.__uri = uri
		
	def getUri(self):
		return self.__uri
	
	def setTitle(self, title):
		self.__title = title
		
	def getTitle(self):
		return self.__title
		
	def setAction(self, action):
		self.__action = action
		
	def getAction(self):
		return self.__action

	def setTypeInfo(self, tinfo):
		self.__type_info = tinfo
		
	def getTypeInfo(self):
		return self.__type_info

	def setTypeInfoRec(self, tinfo):
		self.__type_rec = tinfo
		
	def getTypeInfoRec(self):
		return self.__type_rec

	def setSizeInfo(self, sinfo):
		self.__size_info = sinfo
		
	def getSizeInfo(self):
		return self.__size_info

	def setSizeInfoRec(self, sinfo):
		self.__size_rec = sinfo
		
	def getSizeInfoRec(self):
		return self.__size_rec
	
	def setUriRecord(self, uri):
		self.__uri_rec = uri
		
	def getUriRecord(self):
		return self.__uri_rec
	
	def setTitleRecord(self, title):
		self.__title_rec = title
		
	def getTitleRecord(self):
		return self.__title_rec
		
	def setActionRecord(self, action):
		self.__action_rec = action
		
	def getActionRecord(self):
		return self.__action_rec
	
	def setLanguage(self, lang):
		self.__language_code = lang
		
	def getLanguage(self):
		return self.__language_code
		
	def appendRecord(self, rec):
		self.__records.append(rec)
		
	def getNDEFMessage(self):
		if self.__uri_rec == None and self.__uri != None:
			self.__uri_rec = NDEFUri.NDEFUri()
			self.__uri_rec.setUri(self.__uri)
		
		if self.__uri_rec == None:
			return None
		
		if self.__action_rec == None and self.__action != None:
			self.__action_rec = NDEFSpAction()
			self.__action_rec.setAction(self.__action)
			
		if self.__type_rec == None and self.__type_info != None:
			self.__type_rec = NDEFSpType()
			self.__type_rec.setType(self.__type_info)

		if self.__size_rec == None and self.__size_info != None:
			self.__size_rec = NDEFSpSize()
			self.__size_rec.setSize(self.__size_info)
		
		if self.__title_rec == None and self.__title != None:
			self.__title_rec = NDEFTextRecord.NDEFTextRecord()
			self.__title_rec.doFull(self.__title, self.__language_code)
		
		sp = NDEFMessage.NDEFRecord()
		sp.setTnf(self.__my_tnf)
		sp.setType(self.__my_type)
		payload = self.__uri_rec.getNDEFRecord().getRawBytes()
		if self.__action_rec != None:
			payload = payload + self.__action_rec.getNDEFRecord().getRawBytes()
		if self.__type_rec != None:
			payload = payload + self.__type_rec.getNDEFRecord().getRawBytes()
		if self.__size_rec != None:
			payload = payload + self.__size_rec.getNDEFRecord().getRawBytes()
		payload = payload + self.__title_rec.getNDEFRecord().getRawBytes()
		for i in range(0, len(self.__records)):
			payload = payload + self.__records[i].getRawBytes()
		sp.setPayloadLen(len(payload))
		if len(payload) <= 255:
			sp.setSR(1)
		
		msg = NDEFMessage.NDEFMessage()
		msg.append(sp)
		msg.append(self.__uri_rec.getNDEFRecord())
		if self.__action_rec != None:
			msg.append(self.__action_rec.getNDEFRecord())
		if self.__type_rec != None:
			msg.append(self.__type_rec.getNDEFRecord())
		if self.__size_rec != None:
			msg.append(self.__size_rec.getNDEFRecord())
		msg.append(self.__title_rec.getNDEFRecord())
		
		for i in range(0, len(self.__records)):
			msg.append(self.__records[i])
		
		r = msg.getRecord(0)
		r.setMB(1)
		r.setME(1)
		r = msg.getRecord(1)
		r.setMB(1)
		r.setME(0)
		return msg

	def fromRawData(self, raw_data, raw_is_hex):
		m = NDEFMessage.NDEFMessage()
		m.fromRawData(raw_data, raw_is_hex)
		for i in range(0, m.getNumRecords()):
			r = m.getRecord(i)
			if r.getType() == self.__my_type:
				m1 = NDEFMessage.NDEFMessage()
				m1.fromRawData(r.getPayloadRaw(), 0)
				for j in range(0, m1.getNumRecords()):
					r1 = m1.getRecord(j)
					if r1.getType() == "U":
						self.__uri_rec = NDEFUri.NDEFUri()
						self.__uri_rec.fromRawData(r1.getRawBytes(), 0)
						ab = NDEFUri.NDEFUriAbbreviation()
						self.__uri = ab.getName(self.__uri_rec.getAbbreviation()) + self.__uri_rec.getUri()
					elif r1.getType() == "T":
						self.__title_rec = NDEFTextRecord.NDEFTextRecord()
						self.__title_rec.fromRawData(r1.getRawBytes(), 0)
						self.__title = self.__title_rec.getText()
						self.__language = self.__title_rec.getLanguage()
					elif r1.getType() == "act":
						self.__action_rec = NDEFSpAction()
						self.__action_rec.fromRawData(r1.getRawBytes(), 0)
						self.__action = self.__action_rec.getAction()
					elif r1.getType() == "t":
						self.__type_rec = NDEFSpType()
						self.__type_rec.fromRawData(r1.getRawBytes(), 0)
						self.__type_info = self.__type_rec.getType()
					elif r1.getType() == "s":
						self.__size_rec = NDEFSpSize()
						self.__size_rec.fromRawData(r1.getRawBytes(), 0)
						self.__size_info = self.__size_rec.getSize()
					else:
						self.__records.append(r1)

# for testing
if __name__ == "__main__":
	s1 = NDEFSmartPoster()
	s1.setUri("http://www.mulliner.org/nfc/")
	s1.setTitle("Smart Poster Test")
	s1.setAction(1)
	s1.setSizeInfo(471100815)
	s1.setTypeInfo("image/jpeg")
	s2 = NDEFSmartPoster()
	#print s1.getNDEFMessage().getHex()
	print s1.getUri()
	print s1.getTitle()
	print s1.getAction()
	print s1.getTypeInfo()
	print s1.getSizeInfo()
	s2.fromRawData(s1.getNDEFMessage().getHex(), 1)
	print s2.getUri()
	print s2.getTitle()
	print s2.getAction()
	print s2.getTypeInfo()
	print s2.getSizeInfo()

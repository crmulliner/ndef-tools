#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import Utils
import NDEFSmartPoster
import NDEFUri
import NDEFTextRecord
import NDEFMessage
import Mifare
import NFCTagType1
import SpReader
import os

fi = open(os.sys.argv[1], 'rb')
data = fi.read()
fi.close()

mf = Mifare.Mifare(data, 0)
print "Total Size: " + str(mf.getSize())
#print Utils.bin2hex(mf.getBlock(0))
#print Utils.bin2hex(mf.getBlock(1))
#print Utils.bin2hex(mf.getBlock(2))
#print Utils.bin2hex(mf.getBlock(3))
print "Data:"
print Utils.bin2hex(mf.getData())
for i in range(4, 64):
	print Utils.bin2hex(mf.getBlock(i))

tag = NFCTagType1.NFCTagType1()
tag.fromRawData(mf.getDataHex(), 1)
print len(mf.getData())
n = NDEFMessage.NDEFMessage()
#sp = SpReader.SpReader(tag.getNDEF())
n.fromRawData(tag.getNDEF(), 0)
print "Records: " + str(n.getNumRecords())
for i in range(0, n.getNumRecords()):
	r = n.getRecord(i)
	p = r.getPayload()
	print "PayloadLen: " + str(r.getPayloadLen())
	print "Record Type: " + str(r.getType())
	o = ""
	for j in range(0, len(p)):
		if ord(p[j]) >= 30 and ord(p[j]) <= 127:
			o = o + p[j]
		else:
			o = o + "'" + str(ord(p[j])) + "'"
	print o

#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NDEFSmartPoster
import NDEFUri
import NDEFTextRecord
import NDEFMessage
import CollinsBtNfcAdapter
import os

class SpReader:
	def __init__(self, data, is_hex = 0):
		m = NDEFMessage.NDEFMessage()
		m.fromRawData(data, is_hex)
		if m.getNumRecords() > 0:
			r = m.getRecord(0)
			print "Message has " + str(m.getNumRecords()) + " Records, Type is = " + r.getType()
			if r.getType() == "Sp":
				m1 = NDEFMessage.NDEFMessage()
				m1.fromRawData(r.getPayloadRaw(), 0)
				print "SmartPoster has " + str(m1.getNumRecords()) + " Parts"
				for i in range(0, m1.getNumRecords()):
					r1 = m1.getRecord(i)
					print r1.getType()
					if r1.getType() == "U":
						u = NDEFUri.NDEFUri()
						u.fromRawData(r1.getRawBytes(), 0)
						ab = NDEFUri.NDEFUriAbbreviation()
						print "Plain URI: " + u.getUri()
						print "Abbreviation: " + str(u.getAbbreviation())
						print "Complete URI: " + ab.getName(u.getAbbreviation()) + u.getUri()
					elif r1.getType() == "T":
						u = NDEFTextRecord.NDEFTextRecord()
						u.fromRawData(r1.getRawBytes(), 0)
						print u.getText()
			else:
				print "Message is not a SmartPoster"
		else:
			print "No Records in Message"

if __name__ == "__main__":
	if len(os.sys.argv) < 2:
		print "SpReader.py <BDADDR> <CHANNEL=[22|25]>"
	else:
		test = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
		data = test.quickRead(os.sys.argv[1], int(os.sys.argv[2]))
		sp = SpReader(data, 1)

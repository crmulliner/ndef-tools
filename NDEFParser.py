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


def NDEFParserGetClassByTnfType(tpy, tnf = 0x01):
	if tnf == 0x01:
		if tpy == "Sp":
			sp = NDEFSmartPost.NDEFSmartPoster()
			return sp
		elif tpy == "U":
			u = NDEFUri.NDEFUri()
			return u
		elif tpy == "T":
			t = NDEFTextRecord.NDEFTextRecord()
			return t
		elif tpy == "act":
			act = NDEFSmartPoster.NDEFSpAction()
			return act
		else
			return None
	elif tnf == 0x04:
		if tpy == "nokia.com:rf":
			rf = NokiaRadiostationTag.NokiaRadiostationTag()
			return rf
		elif tpy == "nokia.com:pf":
			pf = NokiaProfileTag.NokiaProfileTag()
			return pf
		elif tpy == "nokia.com:bt":
			bt = NokiaBluetoothTag.NokiaBluetoothTag()
			return bt
		else:
			return None
		

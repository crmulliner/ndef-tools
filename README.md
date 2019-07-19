# Collin's NFC/NDEF Python Library

This library is an implementation of the NFC-Forum's NDEF data types. The 
library can read (parse) and write (generate) most (probably all) defined 
data types as of (April 2008). These are: NDEF Record and Message, URI (U),
TextRecord (T), SmartPoster (Sp) and Action (act). It further supports the
Nokia proprietary Bluetooth-Imaging, Nokia Gallery, Nokia Profile, Nokia
RadioStation record/tag formats.

The library further supports Collin's BtNfcAdapter a simple J2ME/MIDP2.0 
JSR-257 application that acts as a simple NDEF Reader/Writer that is 
accessible via Bluetooth. BtNfcAdapter has been test on the Nokia 6131
NFC and the Nokia 6212 Classic. See [2] for more details on 
CollinsBtNfcAdapter.

References:
 [1] NFC-Forum                        http://www.nfc-forum.org
 [2] NFC tools                        http://www.mulliner.org/nfc/

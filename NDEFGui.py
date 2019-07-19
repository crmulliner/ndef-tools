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
import NokiaBluetoothTag
import os
import signal
import sys
import gobject
import pygtk
pygtk.require('2.0')
import gtk
import time
from threading import Thread
from PIL import Image

class NDEFGui:
	def __init__(self, bdaddr, channel):
		self.cust_file_path = None
		self.cust_file_data = None
		self.cust_file_binary = 0
		self.bdaddr = bdaddr
		self.channel = channel
	
		self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.mainbox = gtk.HBox()
		self.win.add(self.mainbox)
		self.apphbox = gtk.VBox()
		self.apphbox2 = gtk.VBox()
		self.mainbox.add(self.apphbox)
		self.mainbox.add(self.apphbox2)
		
		self.uriframe = gtk.Frame("URI")
		self.apphbox.add(self.uriframe)
		self.urivbox = gtk.VBox()
		self.uriframe.add(self.urivbox)
		self.spframe = gtk.Frame("SmartPoster")
		self.apphbox.add(self.spframe)
		self.spvbox = gtk.VBox()
		self.spframe.add(self.spvbox)
		self.custvbox = gtk.VBox()
		self.custframe = gtk.Frame("Mime-Type")
		self.apphbox2.add(self.custframe)
		self.custframe.add(self.custvbox)
		
		self.uriapp_uri = gtk.TextView()
		self.uriapp_uri.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.urivbox.add(self.uriapp_uri)
		self.uriapp_genbut = gtk.Button("Write")
		self.uriapp_genbut.connect("clicked", self.uri_button)
		self.urivbox.add(self.uriapp_genbut)
		
		self.spvbox.add(gtk.Label("URI"))
		self.spapp_uri = gtk.TextView()
		self.spapp_uri.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.spvbox.add(self.spapp_uri)
		self.spapp_title = gtk.TextView()
		self.spapp_title.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		#self.spapp_title.set_border_window_size(gtk.TEXT_WINDOW_TOP, 5)
		self.spvbox.add(gtk.Label("Title"))
		self.spvbox.add(self.spapp_title)
		self.spapp_genbut = gtk.Button("Write")
		self.spapp_genbut.connect("clicked", self.sp_button)
		self.spvbox.add(self.spapp_genbut)
	
		self.custvbox.add(gtk.Label("Mime-Type"))
		self.custapp_mime_type = gtk.TextView()
		self.custapp_mime_type.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.custvbox.add(self.custapp_mime_type)
		self.custapp_data = gtk.TextView()
		self.custapp_data.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		#self.custapp_data.set_border_window_size(gtk.TEXT_WINDOW_TOP, 5)
		self.custvbox.add(gtk.Label("Data"))
		self.custvbox.add(self.custapp_data)
		self.custapp_loadbut = gtk.FileChooserButton("Load File")
		self.custapp_loadbut.connect("selection-changed", self.file_selected)
		self.custapp_genbut = gtk.Button("Write")
		self.custapp_genbut.connect("clicked", self.mime_button)
		self.custapp_clearbut = gtk.Button("Clear/Reset")
		self.custapp_clearbut.connect("clicked", self.clear_button)
		self.custvbox.add(self.custapp_loadbut)
		self.custvbox.add(self.custapp_clearbut)
		self.custvbox.add(self.custapp_genbut)
		
		self.win.connect("delete-event", self.exit_event)
		
		self.win.resize(800, 480)
		self.win.show_all()
	
	def exit_event(self, bla1, bla2):
		gtk.main_quit()

	def file_selected(self, bla1):
		self.cust_file_path = bla1.get_filename()
		fp = open(self.cust_file_path, 'rb')
		self.cust_file_data = fp.read()
		for i in range(0, len(self.cust_file_data)):
			c = self.cust_file_data[i]
			if ord(c) < 32 or ord(c) > 127:
				if c != '\n' and c != '\r' and c != '\t':
					self.cust_file_binary = 1
					break
		fp.close()
		buf = self.custapp_data.get_buffer()
		if self.cust_file_binary == 0:
			buf.set_text(self.cust_file_data)
		else:
			print "bin"
			buf.set_text(str(len(self.cust_file_data)) +" bytes binary data from: " + bla1.get_filename())

	def get_textfromtextview(self, tv):
		return tv.get_buffer().get_text(tv.get_buffer().get_iter_at_offset(0), tv.get_buffer().get_iter_at_offset(4096))

	def clear_button(self, bla1):
		self.cust_file_binary = 0
		self.cust_file_data = None
		self.custapp_data.get_buffer().set_text("")

	def uri_button(self, bla1):
		self.uri_write(self.get_textfromtextview(self.uriapp_uri))

	def sp_button(self, bla1):
		self.sp_write(self.get_textfromtextview(self.spapp_uri), self.get_textfromtextview(self.spapp_title))
		
	def mime_button(self, bla1):
		if self.cust_file_binary == 0:
			self.mime_write(self.get_textfromtextview(self.custapp_mime_type), self.get_textfromtextview(self.custapp_data))
		else:
			self.mime_write(self.get_textfromtextview(self.custapp_mime_type), self.cust_file_data)

	def sp_write(self, uri, title):
		sp = NDEFSmartPoster.NDEFSmartPoster()
		sp.setUri(uri)
		sp.setTitle(title)
		#title_rec = NDEFTextRecord.NDEFTextRecord()
		#title_rec.setText(title)
		#title_rec.setUtf16(1)
		#sp.setTitleRecord(title_rec)
		
		#print sp.getNDEFMessage().getHex()
		
		w = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
		w.quickWrite(sp.getNDEFMessage().getHex(), self.bdaddr, self.channel)

	def uri_write(self, uri):
		u = NDEFUri.NDEFUri()
		u.setUri(uri)
		
		w = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
		w.quickWrite(u.getNDEFRecord().getHex(), self.bdaddr, self.channel)

	def mime_write(self, mime, data):
		r = NDEFMessage.NDEFRecord()
		r.setPayload(data)
		r.setTnf(0x02)
		r.setType(mime)
		
		w = CollinsBtNfcAdapter.CollinsBtNfcAdapter()
		w.quickWrite(r.getHex(), self.bdaddr, self.channel)

if __name__ == "__main__":
	if len(os.sys.argv) < 2:
		print "NDEFGui Copyright: Collin Mulliner (http://www.mulliner.org/nfc/)"
		print "License: GPLv2"
		print " syntax: " + os.sys.argv[0] + " <BD_ADDR> [channel]"
	else:
		bdaddr = os.sys.argv[1]
		channel = 25
		if len(os.sys.argv) > 2:
			channel = int(os.sys.argv[2])
		main = NDEFGui(bdaddr, channel)
		gtk.main()

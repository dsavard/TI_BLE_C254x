#Main
import serial
from HCIEvents import HCIEvents
from BTDevice import BTDevice,keythread
import struct
from HCI_Codes import *

import os,sys
from threading import Thread

def initserial():
	bt = serial.Serial()
	if os.name == 'posix':
		bt.port = "/dev/ttyACM0"
	else:
		bt.port = "COM3"
	bt.baudrate = 57600
	bt.baudrate = 115200
	bt.stopbits = 1
	bt.parity = 'N'
	bt.bytesize = 8
	bt.xonxoff = 0
	bt.rtscts = 1
	bt.timeout = None
	bt.open()
	return bt

def initdevice(bt):
	'''
		GAP Device Initialization

		Packet is as follow:
			- packet type (1 byte)
			- GAP command (2 bytes)
			- length of data (1 byte)
			- Data:
				i)   GAP Profile Role (1 byte) (Central)
				ii)  Maximum Scan Responses to accept (1 byte) (0x00-0xFF)
				iii) IRK (16 bytes) if all zeros, randomly generated
				iv)  CSRK (16 bytes) if all zeros, randomly generated
				v)   Signature counter initial value (4 bytes)
	'''
	command = PKTTYPES['Command'] + get_gap_cmd('GAP Device Initialization') + struct.pack('B',struct.calcsize('BB16s16sL'))
	command = command + struct.pack('BB16s16sL',struct.unpack('<B',GAPROLES['Central'])[0],3,'\x00','\x00',1)
	
	bt.write(command)
	print "Sent device init command!"

dev = BTDevice()
bt = initserial()
print bt
dev.ser = bt
print("Connected to Dongle")
initdevice(bt)
print ""
print("Starting Read loop")


#useless key thread :)

thr = keythread()
thr.start()
dev.thread=thr
#

while(bt.isOpen()):  # Read a new packet
	packet_type = bt.read()
	
	print("=================================================")
	try:
		print "Found", pkt_types[packet_type], "Packet"
		if packet_type == PKTTYPES['Event']:
			event_code=bt.read()
			try:
				print evt_codes[event_code], "Event Code"
				if event_code == EVTCODES['Low Energy']:
					print "Should not get here. HCI is not supposed to return such events."
					sub_evt_code = bt.read()
					try:
						print sub_evt_codes[sub_evt_code], "Subevent Code"
					except KeyError:
						print "Unknown Subevent Code"

				elif event_code == EVTCODES['Vendor Specific']:
					#event = bt.read(size=3)  # length + event OpCode
					evt_len, evt_opcode = struct.unpack('<BH',bt.read(size=3))
					print "Data length :" + str(evt_len)
					print "Data Code :" + str(evt_opcode)
					HCIEvents().lookup(evt_opcode)(evt_len-2,bt)
				else:
					print "Should not get here. HCI is not supposed to return such events."
					print "Don't know how to handle this Event Code"
					print "Event Code:",hex(struct.unpack('<B',event_code)[0])
					#evt_len = struct.unpack('<B',bt.read())[0]
					#print "Flushing ",str(evt_len)," bytes"
					#bt.read(size=evt_len)

			except KeyError:
				print "Unknown Event Code: ", struct.unpack('<B',event_code)

		else:
			print "Packet type: ", pkt_types[packet_type]
			print struct.unpack('<B',packet_type)
			print "broken!"
	except KeyError:
		print "Not an event. Unknown packet type: ", struct.unpack('<B',packet_type)


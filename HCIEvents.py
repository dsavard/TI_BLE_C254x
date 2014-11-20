import serial
from BTDevice import BTDevice,keythread
import struct
import binascii

from HCI_Codes import *


class HCIEvents:
	'''
		Lookup table to match operation codes to appropriate procedure to
		process the incoming event. Refer to TI_BLE_Vendor_Specific_HCI_Guide.pdf
		for details on opcode and events.
	'''
	opcode_to_procedure = {	0x0600 : 'proc_evt_gap_device_init_done',
				0x0601 : 'proc_evt_gap_discovery',
				0x0605 : 'proc_evt_gap_link_established',
				0x0606 : 'proc_evt_gap_link_terminated',
				0x060D : 'proc_evt_gap_device_information',
				0x067F : 'proc_evt_gap_hci_ext_command_status',
				0x0509 : 'proc_evt_att_read_by_type_response',
				0x0513 : 'proc_evt_att_write_response',
				0x051B : 'proc_evt_att_handle_value_notification'}

	def proc_evt_gap_device_init_done(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		status, deviceAddress, dataPktLen, numDataPkts, IRK, CSRK  = struct.unpack('<B6sHB16s16s',event[0:42])
		if status == 0x00: #success
			print "Device initialized and ready"
			BTDevice.dongleAddress 	= deviceAddress
			print "Device address:", binascii.b2a_hex(BTDevice.dongleAddress)
			BTDevice.IRK		= IRK
			BTDevice.CSRK		= CSRK
			BTDevice.deviceReady	= 1
		else:
			print "Device Initialization failed"
			exit()

	def proc_evt_gap_discovery(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		start_idx = 0
		end_idx = 2
		status, numDevices = struct.unpack('<BB',event[start_idx:end_idx])
		if status == 0:
			if numDevices == 0:
				print "Device discovery done, no device found"
			else:
				print "Device discovery done, found "+str(numDevices)+" device(s)"
				devDictionary={}
				for devIndex in range(numDevices):
					start_idx = end_idx
					end_idx = end_idx + 8
					evttype, addrtype, addr = struct.unpack('<BB6s',event[start_idx:end_idx])
					devDictionary[devIndex] = {'EvType':evttype,'AddrType':addrtype,'Addr':binascii.b2a_hex(addr),'BinAddr':addr}
				print devDictionary
				BTDevice.foundDevices=devDictionary					
		else:
			print "Error during device discovery"
			
	def proc_evt_gap_link_established(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		status, addrtype, addr, handle, interval, latency, timeout, clockaccuracy = struct.unpack('<BB6s2sHHHB',event[0:17])
		BTDevice.connHandle = handle
		print "\tLength connHandle: ", len(BTDevice.connHandle)
		print "\tConnection Handle: 0x"+binascii.b2a_hex(BTDevice.connHandle)
		print "\tStatus: ", hex(status)
		print "\tAddress Type: ", hex(addrtype)
		print "\tAddress: 0x"+binascii.b2a_hex(addr)
		print "\tConnection interval: ", interval*1.25, "msec"
		print "\tConnection latency: ", latency*1.25, "msec"
		print "\tConnection timeout: ", timeout*1.25, "msec"
		print "\tClock accuracy: ", clkaccuracies[clockaccuracy], "ppm"
		print "Established Link connection to keyfob"

	def proc_evt_gap_link_terminated(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		status, handle, reason = struct.unpack('<B2sB',event[0:4])
		if status == 0:
			print "Connection closed"
			if BTDevice.connHandle == handle:
				BTDevice.connHandle=""
				print "Connection to Keyfob closed"
				BTDevice().ser.close()
				print "Terminating App, Please press Enter"

	def proc_evt_gap_device_information(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		start_idx = 0
		end_idx = 11
		status, evttype, addrtype, addr, rssi, datalen = struct.unpack('<BBB6sBB',event[start_idx:end_idx])
		start_idx = end_idx
		end_idx = end_idx + datalen
		print "Device "+binascii.b2a_hex(addr)+" responded to discovery with "+binascii.b2a_hex(event[start_idx:end_idx])+" (reverse)"

	def proc_evt_gap_hci_ext_command_status(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		csgval, opcode, trailer = struct.unpack('<BHB',event[0:4])
		print "opcode:",opcode
		print "csg:",csgval
		print "trailer:",trailer
		if csgval == get_csg('HCI'):
			if opcode == get_gap_cmd10('GAP Device Initialization'):
				print "Dongle received: 'GAP Device Initialization' command"

			elif opcode == get_gap_cmd10('GAP Device Discovery Request'):
				print "Dongle received: 'Device Discovery Request' command and is now searching"

			elif opcode == get_gap_cmd10('GAP Establish Link Request'):
				print "Dongle received: 'GAP Establish Link Request' command"

			elif opcode == get_gap_cmd10('GAP Terminate Link Request'):
				print "Dongle received: 'GAP Terminate Link Request' command"

			elif opcode == get_gatt_cmd10('GATT Discover Characteristics By UUID'):
				print "Dongle received: 'GATT Discover Characteristics By UUID' command"
				print "Keyfob is searching"

			elif opcode == get_att_cmd10('ATT Write Request'):
				print "Dongle received: 'ATT Write Request' command"
				print "Keyfob is writing"

			else:
				print "Unknown OpCode" + hex(opcode)
		else:
			print "Something is wrong. CSG value:", csgval
			print "CSG:", csg[csgval]

	def proc_evt_att_read_by_type_response(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		start_idx = 0
		end_idx = 1
		status = struct.unpack('<B',event[start_idx:end_idx])[0]
		print "\tResponse status:",hex(status)
		if status == 0x1A:
			BTDevice().thread.sendNextPacket()

		elif status == 0x00:
			start_idx = end_idx
			end_idx = end_idx + 4
			chandle, pdulen, datalen = struct.unpack('<HBB',event[start_idx:end_idx])
			start_idx = end_idx
			end_idx = end_idx + 2
			handle = struct.unpack('<H',event[start_idx:end_idx])[0]
			print "Data length: "+str(datalen)
			print "PDU length: "+str(pdulen)
			if datalen == 7:
				print "Sensor handle: "+str(hex(handle))
				address = struct.pack('BB',handle+2,0)
				print "Got Handle for sensor, setting up notification..."
				BTDevice().notificationAttributeAddresses.append(address)
				BTDevice().executionStack.append(BTDevice().setUpNotificationForSensor)
				
	def proc_evt_att_write_response(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		status = struct.unpack('<B',event[0])[0]
		if status == 0x00:
			print "Notification activated"
			BTDevice().thread.sendNextPacket()
		else:
			print "Write failed"
			
	def proc_evt_att_handle_value_notification(self,evt_len,bt):
		print "Data length: ",evt_len
		event = bt.read(size=evt_len)
		start_idx = 0
		end_idx = 4
		P=struct.unpack('<BHB',event[start_idx:end_idx])
		print "--------------------"
		print "Receive HandleValue notification from connhandle: "+str(P[1])
		
		start_idx = end_idx
		end_idx = end_idx + 3
		attr, value = struct.unpack('<HB',event[start_idx:end_idx])
		print "Attribute: "+str(hex(attr))+" Value: "+str(value)

	def proc_evt_no_match(self,evt_len,bt):
		print "no match found"
		print "Data length: ",evt_len
		print "Flushing ",evt_len," bytes"
		bt.read(size=evt_len)

	def lookup(self,opcode):
		print "Got '"+get_event(opcode)+"'"
		try:
			procedure = self.opcode_to_procedure[opcode]
		except KeyError:
			procedure = 'proc_evt_no_match'
			print 'No procedure associated with code: '+hex(opcode)+'\t'+gapevts[opcode]+' Event'

		return getattr(self, procedure, None)


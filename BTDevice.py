import serial,struct
import time

import os,sys
from threading import Thread

from HCI_Codes import *

class keythread(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		while BTDevice().ser.isOpen():
			keyin=raw_input()
			if keyin == "d":
				BTDevice().doDiscovery()
			elif keyin == "e":
				BTDevice().doEstablishLink(0)
			elif keyin == "t":
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactivateAccelerometer)
				BTDevice().executionStack.append(BTDevice().doTerminateLink)
				BTDevice().deactNotificationForSensor()
				
			elif keyin == "1":
				BTDevice().executionStack.append(BTDevice().activateAccelerometer)
				BTDevice().executionStack.append(BTDevice().setUpXAccNotifications)
				BTDevice().executionStack.append(BTDevice().setUpYAccNotifications)
				BTDevice().executionStack.append(BTDevice().setUpZAccNotifications)
				BTDevice().setUpButtNotifications()
			elif keyin == "2":
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactNotificationForSensor)
				BTDevice().executionStack.append(BTDevice().deactivateAccelerometer)
				BTDevice().deactNotificationForSensor()
			elif keyin != "":
				print "Invalid key"

	def sendNextPacket(self):
		print BTDevice().executionStack
		if BTDevice().executionStack != []:
			BTDevice().executionStack.pop(0)()
		else:
			print "No Packets to send"


class BTDevice(object):
    _shared = {}
    def __init__(self):
	self.__dict__ = self._shared
    deviceReady=0
    dongleAddress="\x00\x00\x00\x00\x00\x00\x00\x00"
    IRK="\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    CSRK="\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ser = serial.Serial()
    foundDevices = {}
    connHandle=""
    nextWriteCommand=""
    thread=keythread()
    executionStack=[]

    '''
	Manage connection
    '''
    def doDiscovery(self):
	print "Doing Discovery"
	command = PKTTYPES['Command'] + get_gap_cmd('GAP Device Discovery Request')
	command = command + '\x03' #Data length
	command = command + '\x03' #Mode (all)
	command = command + '\x01' #Enable Name Mode
	command = command + '\x00' #Don't use white list
	self.ser.write(command)

    def doEstablishLink(self,device):
	print "Sending establish link request"
	command = PKTTYPES['Command'] + get_gap_cmd('GAP Establish Link Request')
	command = command + '\x09'							#Data length
	command = command + '\x00'							#Disable highDutyCycle
	command = command + '\x00'							#Don't use white list
	command = command + struct.pack('<B',self.foundDevices[device]['AddrType'])	# 1 octet
	command = command + self.foundDevices[device]['BinAddr']			# 6 octets
	self.ser.write(command)

    def doTerminateLink(self):
	print "Sending terminate link request"
	command = PKTTYPES['Command'] + get_gap_cmd('GAP Terminate Link Request')
	command = command + '\x03' 		#Data length
	command = command + self.connHandle 	#Connection handle
	command = command + '\x13'		#Reason (Remote User Terminated Connection)
	self.ser.write(command)
	
    '''
	Manage notifications
    '''
    def setUpXAccNotifications(self):
	command = PKTTYPES['Command'] + get_gatt_cmd('GATT Discover Characteristics By UUID')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x01\x00'		#Starting handle
	command = command + '\xFF\xFF'		#Ending handle
	command = command + '\xA3\xFF'		#UUID for X-axis
	self.ser.write(command)

    def setUpYAccNotifications(self):
	command = PKTTYPES['Command'] + get_gatt_cmd('GATT Discover Characteristics By UUID')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x01\x00'		#Starting handle
	command = command + '\xFF\xFF'		#Ending handle
	command = command + '\xA4\xFF'		#UUID for Y-axis
	self.ser.write(command)

    def setUpZAccNotifications(self):
	command = PKTTYPES['Command'] + get_gatt_cmd('GATT Discover Characteristics By UUID')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x01\x00'		#Starting handle
	command = command + '\xFF\xFF'		#Ending handle
	command = command + '\xA5\xFF'		#UUID for Z-axis
	self.ser.write(command)

    def setUpButtNotifications(self):
	command = PKTTYPES['Command'] + get_gatt_cmd('GATT Discover Characteristics By UUID')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x01\x00'		#Starting handle
	command = command + '\xFF\xFF'		#Ending handle
	command = command + '\xE1\xFF'		#UUID for Buttons
	self.ser.write(command)

    def activateAccelerometer(self):
	command = PKTTYPES['Command'] + get_att_cmd('ATT Write Request')
	command = command + '\x07'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x00' 		#Signature off
	command = command + '\x00' 		#Command off
	command = command + '\x34\x00'		#Attribute address
	command = command + '\x01'		#Attribute value
	self.ser.write(command)

    def deactivateAccelerometer(self):
	command = PKTTYPES['Command'] + get_att_cmd('ATT Write Request')
	command = command + '\x07'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x00'		#Signature off
	command = command + '\x00'		#Command off
	command = command + '\x34\x00'		#Attribute address
	command = command + '\x00'		#Attribute value
	self.ser.write(command)

    notificationAttributeAddresses=[]
    def setUpNotificationForSensor(self):
	command = PKTTYPES['Command'] + get_att_cmd('ATT Write Request')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x00'		#Signature off
	command = command + '\x00'		#Command off
	x=self.notificationAttributeAddresses.pop()
	self.notificationAttributeAddressesAct.append(x)
	print "setUpNotificationForSensor(): x=",x
	command = command + x 			#Attribute address
	command = command + '\x01\x00'		#Attribute value
	self.ser.write(command)


    notificationAttributeAddressesAct=[]
    def deactNotificationForSensor(self):
	print self.notificationAttributeAddressesAct
	if self.notificationAttributeAddressesAct == []:
		BTDevice().thread.sendNextPacket()
		return
	command = PKTTYPES['Command'] + get_att_cmd('ATT Write Request')
	command = command + '\x08'		#Data length
	command = command + self.connHandle	#Connection handle (2 octets)
	command = command + '\x00'		#Signature off
	command = command + '\x00'		#Command off
	x=self.notificationAttributeAddressesAct.pop()
	print "deactNotificationForSensor(): x=",x
	command = command + x			#Attribute address
	command = command + '\x00\x00'		#Attribute value
	self.ser.write(command)

import struct

PKTTYPES = {'Command'           : '\x01',
            'Asynchronous Data' : '\x02',
            'Synchronous Data'  : '\x03',
            'Event'             : '\x04'}

EVTCODES = {'Vendor Specific'                             : '\xFF',
            'Low Energy'                                  : '\x3E',
            'Disconnection Complete BT'                   : '\x05',
            'Encryption Change BT'                        : '\x08',
            'Read Remote Version Information Complete BT' : '\x0C',
            'Command Complete BT'                         : '\x0E',
            'Command Status BT'                           : '\x0F',
            'Hardware Error BT'                           : '\x10',
            'Number of Completed Packets BT'              : '\x13',
            'Data Buffer Overflow'                        : '\x1A',
            'Encryption Key Refresh Complete BT'          : '\x30'}

SUBEVTCODES = {'LE Connection Complete'                : '\x01',
               'LE Advertising Report'                 : '\x02',
               'LE Connection Update Complete'         : '\x03',
               'LE Read Remote Used Features Complete' : '\x04',
               'LE Long Term Key Requested'            : '\x05'}

EOGF = {'Embedded Opcode'  : '\x00',
        'Core Opcode'      : '\x01',
        'Profile Request'  : '\x02',
        'Profile Response' : '\x03'}

GAPEVTS = {'GAP Device Init Done'         : '\x00',
           'GAP Device Discovery'         : '\x01',
           'GAP Advert Data Update Done'  : '\x02',
           'GAP Make Discoverable Done'   : '\x03',
           'GAP End Discoverable Done'    : '\x04',
           'GAP Link Established'         : '\x05',
           'GAP Link Terminated'          : '\x06',
           'GAP Link Parameter Update'    : '\x07',
           'GAP Random Address Changed'   : '\x08',
           'GAP Signature Updated'        : '\x09',
           'GAP Authentication Complete'  : '\x0A',
           'GAP Passkey Needed'           : '\x0B',
           'GAP Slave Requested Security' : '\x0C',
           'GAP Device Information'       : '\x0D',
           'GAP Bond Complete'            : '\x0E',
           'GAP Pairing Requested'        : '\x0F',
           'GAP Command Status'           : '\x7F'}

OGF = {'Link Control Commands'            : '\x01',
       'Link Policy Commands'             : '\x02',
       'Controller and Baseband Commands' : '\x03',
       'Informational Parameters'         : '\x04',
       'Status Parameters'                : '\x05',
       'Testing Commands'                 : '\x06',
       'LE Only Commands'                 : '\x08',
       'Vendor Specific Commands'         : '\xFF'}

CSG = {'HCI'          : '\x00',
       'L2CAP'        : '\x01',
       'ATT'          : '\x02',
       'GATT'         : '\x03',
       'GAP'          : '\x04',
       'UTIL'         : '\x05',
       'Reserved'     : '\x06',
       'User Profile' : '\x07'}

L2CAPCMDS = {'L2CAP Connection Parameter Update Request' : '\x92'}

ATTCMDS = {'ATT Error Response'              : '\x01',
           'ATT Exchange MTU Request'        : '\x02',
           'ATT Exchange MTU Response'       : '\x03',
           'ATT Find Information Request'    : '\x04',
           'ATT Find Information Response'   : '\x05',
           'ATT Find By Type Value Request'  : '\x06',
           'ATT Find By Type Value Response' : '\x07',
           'ATT Read By Type Request'        : '\x08',
           'ATT Read By Type Response'       : '\x09',
           'ATT Read Request'                : '\x0A',
           'ATT Read Response'               : '\x0B',
           'ATT Read Blob Request'           : '\x0C',
           'ATT Read Blob Response'          : '\x0D',
           'ATT Read Multiple Request'       : '\x0E',
           'ATT Read Multiple Response'      : '\x0F',
           'ATT Read By Group Type Request'  : '\x10',
           'ATT Read By Group Type Response' : '\x11',
           'ATT Write Request'               : '\x12',
           'ATT Write Response'              : '\x13',
           'ATT Prepare Write Request'       : '\x16',
           'ATT Prepare Write Response'      : '\x17',
           'ATT Execute Write Request'       : '\x18',
           'ATT Execute Write Response'      : '\x19',
           'ATT Handle Value Notification'   : '\x1B',
           'ATT Handle Value Indication'     : '\x1D',
           'ATT Handle Value Confirmation'   : '\x1E'}


GATTCMDS = {'GATT Discover Characteristics By UUID' : '\x88',
            'GATT Write Long'                       : '\x96'}

GAPCMDS = {'GAP Device Initialization'         : '\x00',
           'GAP Configure Device Address'      : '\x03',
           'GAP Device Discovery Request'      : '\x04',
           'GAP Device Discovery Cancel'       : '\x05',
           'GAP Make Discoverable'             : '\x06',
           'GAP Update Advertising Data'       : '\x07',
           'GAP End Discoverable'              : '\x08',
           'GAP Establish Link Request'        : '\x09',
           'GAP Terminate Link Request'        : '\x0A',
           'GAP Authenticate'                  : '\x0B',
           'GAP Passkey Update'                : '\x0C',
           'GAP Slave Security Request'        : '\x0D',
           'GAP Signable'                      : '\x0E',
           'GAP Bond'                          : '\x0F',
           'GAP Terminate Auth'                : '\x10',
           'GAP Update Link Parameter Request' : '\x11',
           'GAP Set Parameter'                 : '\x30',
           'GAP Get Parameter'                 : '\x31',
           'GAP Resolve Private Address'       : '\x32',
           'GAP Set Advertisement Token'       : '\x33',
           'GAP Remove Advertisement Token'    : '\x34',
           'GAP Update Advertisement Tokens'   : '\x35',
           'GAP Bond Set Parameter'            : '\x36',
           'GAP Bond Get Parameter'            : '\x37'}

GAPROLES = {'Broadcaster' : '\x01',
            'Observer'    : '\x02',
            'Peripheral'  : '\x04',
            'Central'     : '\x08'}

pkt_types = {'\x01' : 'Command',
             '\x02' : 'Asynchronous Data',
             '\x03' : 'Synchronous Data',
             '\x04' : 'Event'}

evt_codes = {'\xFF' : 'Vendor Specific',
             '\x3E' : 'Low Energy',
             '\x05' : 'Disconnection Complete BT',
             '\x08' : 'Encryption Change BT',
             '\x0C' : 'Read Remote Version Information Complete BT',
             '\x0E' : 'Command Complete BT',
             '\x0F' : 'Command Status BT',
             '\x10' : 'Hardware Error BT',
             '\x13' : 'Number of Completed Packets BT',
             '\x1A' : 'Data Buffer Overflow',
             '\x30' : 'Encryption Key Refresh Complete BT'}

sub_evt_codes = {'\x01' : 'LE Connection Complete',
                 '\x02' : 'LE Advertising Report',
                 '\x03' : 'LE Connection Update Complete',
                 '\x04' : 'LE Read Remote Used Features Complete',
                 '\x05' : 'LE Long Term Key Requested'}

ogf = {'\x01' : 'Link Control Commands',
       '\x02' : 'Link Policy Commands',
       '\x03' : 'Controller and Baseband Commands',
       '\x04' : 'Informational Parameters',
       '\x05' : 'Status Parameters',
       '\x06' : 'Testing Commands',
       '\x08' : 'LE Only Commands',
       '\xFF' : 'Vendor Specific Commands'}

csg = {'\x00' : 'HCI',
       '\x01' : 'L2CAP',
       '\x02' : 'ATT',
       '\x03' : 'GATT',
       '\x04' : 'GAP',
       '\x05' : 'UTIL',
       '\x06' : 'Reserved',
       '\x07' : 'User Profile'}

gapevts = {0x0600 : 'GAP Device Init Done',
           0x0601 : 'GAP Device Discovery',
           0x0602 : 'GAP Advert Data Update Done',
           0x0603 : 'GAP Make Discoverable Done',
           0x0604 : 'GAP End Discoverable Done',
           0x0605 : 'GAP Link Established',
           0x0606 : 'GAP Link Terminated',
           0x0607 : 'GAP Link Parameter Update',
           0x0608 : 'GAP Random Address Changed',
           0x0609 : 'GAP Signature Updated',
           0x060A : 'GAP Authentication Complete',
           0x060B : 'GAP Passkey Needed',
           0x060C : 'GAP Slave Requested Security',
           0x060D : 'GAP Device Information',
           0x060E : 'GAP Bond Complete',
           0x060F : 'GAP Pairing Requested',
           0x067F : 'GAP Command Status'}

attevts = {0x0501 : 'ATT Error Response',
           0x0502 : 'ATT Exchange MTU Request',
           0x0503 : 'ATT Exchange MTU Response',
           0x0504 : 'ATT Find Information Request',
           0x0505 : 'ATT Find Information Response',
           0x0506 : 'ATT Find By Type Value Request',
           0x0507 : 'ATT Find By Type Value Response',
           0x0508 : 'ATT Read By Type Request',
           0x0509 : 'ATT Read By Type Response',
           0x050A : 'ATT Read Request',
           0x050B : 'ATT Read Response',
           0x050C : 'ATT Read Blob Request',
           0x050D : 'ATT Read Blob Response',
           0x050E : 'ATT Read Multiple Request',
           0x050F : 'ATT Read Multiple Response',
           0x0510 : 'ATT Read By Group Type Request',
           0x0511 : 'ATT Read By Group Type Response',
           0x0512 : 'ATT Write Request',
           0x0513 : 'ATT Write Response',
           0x0516 : 'ATT Prepare Write Request',
           0x0517 : 'ATT Prepare Write Response',
           0x0518 : 'ATT Execute Write Request',
           0x0519 : 'ATT Execute Write Response',
           0x051B : 'ATT Handle Value Notification',
           0x051D : 'ATT Handle Value Indication',
           0x051E : 'ATT Handle Value Confirmation'}

clkaccuracies = [500, 250, 150, 100, 75, 50, 30, 20]

def get_gap_cmd(cmd):
	try:
		output = GAPCMDS[cmd]+'\xFE'
	except KeyError:
		output = '\x00\x00'
	return output

def get_gap_cmd10(cmd):
	try:
		output = GAPCMDS[cmd]+'\xFE'
	except KeyError:
		output = '\x00\x00'
	return struct.unpack('<H',output)[0]

def get_gatt_cmd(cmd):
	try:
		output = GATTCMDS[cmd]+'\xFD'
	except KeyError:
		output = '\x00\x00'
	return output

def get_gatt_cmd10(cmd):
	try:
		output = GATTCMDS[cmd]+'\xFD'
	except KeyError:
		output = '\x00\x00'
	return struct.unpack('<H',output)[0]

def get_att_cmd(cmd):
	try:
		output = ATTCMDS[cmd]+'\xFD'
	except KeyError:
		output = '\x00\x00'
	return output

def get_att_cmd10(cmd):
	try:
		output = ATTCMDS[cmd]+'\xFD'
	except KeyError:
		output = '\x00\x00'
	return struct.unpack('<H',output)[0]

def get_l2cap_cmd(cmd):
	try:
		output = L2CAPCMDS[cmd]+'\xFC'
	except KeyError:
		output = '\x00\x00'
	return output

def get_gap_evt(evt):
	try:
		output = GAPEVTS[evt]+'\x06'
	except KeyError:
		output = '\x00\x00'
	return struct.unpack('<H',output)[0]

def get_att_evt(evt):
	try:
		output = ATTCMDS[evt]+'\x05'
	except KeyError:
		output = '\x00\x00'
	return struct.unpack('<H',output)[0]

def get_csg(code):
	try:
		output = CSG[code]
	except KeyError:
		output = '\xFF'
	return struct.unpack('<B',output)[0]

def get_event(code):
	''' Search for a GAP event '''
	try:
		output = gapevts[code]
	except KeyError:
		''' Search for a ATT event '''
		try:
			output = attevts[code]
		except KeyError:
			output = 'Unknown event (not found)'
	return output

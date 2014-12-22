#!/usr/bin/python

import platform
import Queue
import serial
import sys
import thread
import time

if platform.system() == 'Windows':
    import serial.tools.list_ports
    #print list(serial.tools.list_ports.comports())
    port = "COM37"
else:
    # Linux:
    port = '/dev/ttyUSB0'


baudrate = 115200

def hex_dump(data):
    for i in range(0, len(data), 16):
        s = "rx data: "
        #s = "%04x: " % i
        for j in range(16):
            if (i + j) < len(data):
                s += "%02x " % ord(data[i+j])
            else:
                s += "   "
        for j in range(16):
            if (i + j) < len(data):
                c = ord(data[i+j])
                if (c >= 32) and (c < 95):
                    s += "%c" % c
                else:
                    s += "."
        print s

ser = serial.Serial(port,
                    baudrate,
                    bytesize=8, parity='N', stopbits=1,
                    xonxoff=0, rtscts=0,
                    timeout=0.1)

def rx_thread():
    while True:
        data = ser.read(64)
        if len(data) > 0:
            hex_dump(data)

rx_queue = Queue.Queue()
rx_thread = thread.start_new_thread(rx_thread, ())

while True:
    sys.stdout.write('> ')
    data = sys.stdin.readline()
    try:
        bytes = ''.join([chr(int(x, 16) & 0xff) for x in data.split()])
    except Exception as e:
        print "error parsing data: %s" % str(e)
    ser.write(bytes)

    

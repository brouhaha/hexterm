#!/usr/bin/python
# -*- coding: utf-8 -*-

# hexterm.py - serial terminal program with hexadecimal input from
# keyboard and hexadecimal dump w/ ASCII output.
copyright_msg = 'hexterm Copyright © 2014 Eric Smith <spacewar@gmail.com>'

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import platform
import Queue
import serial
import sys
import thread
import time

if platform.system() == 'Windows':
    import serial.tools.list_ports
    #print list(serial.tools.list_ports.comports())
    default_port = "COM1"
else:
    # Linux:
    default_port = '/dev/ttyUSB0'

default_rate = 115200

parser = argparse.ArgumentParser(epilog = copyright_msg)
parser.add_argument("-p", "--port", type=str, help="serial port (default: %(default)s)", default = default_port)
parser.add_argument("-r", "--rate", type=int, help="serial bits/s (default: %(default)s)", default = default_rate)
parser.add_argument("-q", "--quiet", help="suppress sign-on message", action="store_true")

args = parser.parse_args()

port = args.port
rate = args.rate

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
                    rate,
                    bytesize=8, parity='N', stopbits=1,
                    xonxoff=0, rtscts=0,
                    timeout=0.1)

def rx_thread():
    while True:
        data = ser.read(64)
        if len(data) > 0:
            hex_dump(data)


if not args.quiet:
    print copyright_msg
    print "use --help command line option for help and license information"
    print "port = %s, rate = %d" % (port, rate)
    print

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

    

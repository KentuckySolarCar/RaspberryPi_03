#python 2.7

import serial, time, io, thread, cStringIO
from datetime import datetime as dt
from ThreadedSerialIO import ThreadedSerialIO

#the file to be written to
engine_file = open("engine.txt","a") #engine data written to
data_file = open("data.txt","a") #both batteries and gps data written to

#engine=>  t...8
#battery=> V[
#GPS=> 

#all of the ports
ports=["/dev/ttyACM0","/dev/ttyUSB1","/dev/pts/1"]
port_refresh_rate=[9600,9600,9600]
port_delay_timer=[10,10,10]
serial_ports=[None,None,None]

def write_to_file(a,b,c):
	while True:
		for temp_serial_port in serial_ports:
			if temp_serial_port != None:
				temp_serial_port.saveDataToFile(c)
		c.flush()
		time.sleep(b)

def close_program():
	file.close()

#all of the serial
i = 0
for port in ports:
	try:
		serial_ports[i] = ThreadedSerialIO(port, port_refresh_rate[i], port_delay_timer[i])
		i = i+1
	except:
		print "Could not connect to "+port

for serial in serial_ports:
	if serial != None:
		serial.start()

try:
	thread.start_new_thread( write_to_file, ("Thread-4", 1, data_file))
except:
	print "Could not start the writing thread"

while 1:
	pass

#!python 3

import serial, time, io, threading, datetime, subprocess, os
from datetime import datetime as dt
from ThreadedSerialIO import ThreadedSerialIO
from SerialIdentifier import SerialIdentifier
from MotorSerialIO import MotorSerialIO
from BatterySerialIO import BatterySerialIO
from datetime import datetime

#the file to be written to
motor_file = open("motor.txt","a") #motor data written to
data_file = open("data.txt","a") #both batteries and gps data written to

engine_file.write("-------------------------------\r\n")
engine_file.write("Starting Logging:"+str(datetime.now().time())+"\r\n")
engine_file.write("Data Format...\r\n")
engine_file.write("hour:min:sec.milli:bus_current,bus_voltage,vehicle_velocity,motor_velocity,phase_a_current,phase_b_current,dc_bus_amphours,odometer\r\n")
engine_file.write("-------------------------------\r\n")
engine_file.flush()

data_file.write("---------------------------------\r\n")
data_file.write("Starting Logging:"+str(datetime.now().time())+"\r\n")
data_file.write("---------------------------------\r\n")
data_file.flush()

#lock to serialize console output
lock = threading.Lock()

#all of the ports
ports=[]
port_refresh_rate=[19200,152900]
port_delay_timer=10
serial_ports=[]

def write_to_file(a,b):
	while True:
		with lock:
			i = 0
			p_time = str(datetime.now().time())
			#for each element in serial_ports
			for temp_serial_port in serial_ports:

				#check to make sure it was actually created
				if temp_serial_port != None:

					#check to see if it has read from the port
					if temp_serial_port.hasReadData():

						#check to see if it is a SerialIdentifier and has not been given a type yet
						if isinstance(temp_serial_port, SerialIdentifier):
							input_data = temp_serial_port.getData()

							#check if it is an engine input
							if MotorSerialIO.determineType(MotorSerialIO, input_data):
								print(str(temp_serial_port.port)+" identified as motor with baud rate of "+str(port_refresh_rate[temp_serial_port.baud_rate_id])+" and data of \""+input_data+"\"")
								temp_serial_port.stop()
								serial_ports[i] = MotorSerialIO(temp_serial_port.port, port_refresh_rate, temp_serial_port.baud_rate_id, temp_serial_port.fps_delay, input_data)
								serial_ports[i].start()

							#check if it is a battery input
							elif BatterySerialIO.determineType(BatterySerialIO, input_data):
								print(str(temp_serial_port.port)+"identified as battery with baud rate of "+str(port_refresh_rate[temp_serial_port.baud_rate_id])+" and data of \""+input_data+"\"")
								temp_serial_port.stop()
								serial_ports[i] = BatterySerialIO(temp_serial_port.port, port_refresh_rate, temp_serial_port.baud_rate_id, temp_serial_port.fps_delay, input_data)
								serial_ports[i].start()

							#check to see if it is a GPS input
							#elif GPSSerialIO.determineType(input_data):

						#if its type has already been determined and it was determined to be an motor controll input
						elif isinstance(temp_serial_port, MotorSerialIO):
							temp_serial_port.saveDataToFile(motor_file,p_time)

						#if it is a battery input
						elif isinstance(temp_serial_port, BatterySerialIO):
							temp_serial_port.saveDataToFile(data_file,p_time)

						#should never happen
						#else:

				i = i+1
			motor_file.flush()
			data_file.flush()
			time.sleep(b)

#Not implemented
def close_program():
	file.close()

#all of the serial
return_text = os.popen("ls /dev/ttyUSB*").read()

for port in return_text.split("\n"):
	try:
		serial_ports.append(SerialIdentifier(port, port_refresh_rate, 0, port_delay_timer, ""))
	except:
		pass

for serial in serial_ports:
	if serial != None:
		serial.start()

# Create the queue and thread pool.
thread = threading.Thread( target=write_to_file, args=("Thread-4", 1))
thread.start()

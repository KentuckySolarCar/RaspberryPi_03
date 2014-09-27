#Class for handling serial communications overhead
#JM 9/14


import serial 
import io

class SerialComm:
	def __init__(self, port, baud):
		ser = serial.Serial(port, baud)
		sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1)
		

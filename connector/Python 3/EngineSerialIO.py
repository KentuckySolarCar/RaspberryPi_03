from ThreadedSerialIO import ThreadedSerialIO
import re, time, struct

#Author: Ethan Toney and Kristina Gessel

class MotorSerialIO(ThreadedSerialIO):

	#In/out current (bus:input Phase:output)
	#phase a and b (seperate)
	#Enery odometer (?) amp hours
	motorPattern = re.compile('(t([0-9]|[A-F])*)')

	base_motor_controller_id = int("0x400",0)

	bus_measurement_id = base_motor_controller_id+2
	velocity_measurement = base_motor_controller_id+3
	phase_measurement_id = base_motor_controller_id+4
	odometer_and_bus_amphours_measurement = base_motor_controller_id+14

	

	def determineType(cls,text):
		m1 = MotorSerialIO.motorPattern.search(text)
		return m1 != None

	def __init__(self, t_port, t_rates, t_rate_id, t_fps_delay, t_data):
		super(MotorSerialIO, self).__init__( t_port, t_rates, t_rate_id, t_fps_delay, t_data)

		self.bus_current = 0
		self.bus_voltage = 0
		self.vehicle_velocity = 0
		self.motor_velocity = 0
		self.phase_a_current = 0
		self.phase_b_current = 0
		self.dc_bus_amphours = 0
		self.odometer = 0

	#saves the current data in the data_buffer to 'p_file'
	def saveDataToFile(self,p_file,p_time):
		data_format = p_time + ":" +  str(self.bus_current) + "," + str(self.bus_voltage) + "," + str(self.vehicle_velocity) + "," + str(self.motor_velocity) 
		data_format = str(data_format) + "," + str(self.phase_a_current) + "," + str(self.phase_b_current) + "," + str(self.dc_bus_amphours) + "," + str(self.odometer) + "\r\n"
		p_file.write(data_format)
		p_file.flush()

	def interpretData(self):
		while self.running:
			self.temp_data = self.temp_data + self.getData()
			m1 = MotorSerialIO.motorPattern.search(self.temp_data) #True

			while m1 != None:
				code = m1.group()
				if len(code) == 21:
					#FIXME this might be wrong depending on if the endline characters are still in the strings, which I think they are not
					self.temp_data = self.temp_data[self.temp_data.index(m1.group())+len(m1.group())+4 : len(self.temp_data)]
					codeArray = list(code)

					#print("data="+code + " length=" + str(len(code)) + " [0]="+ codeArray[0])

					id_numb = int("0x" + codeArray[1] + codeArray[2] + codeArray[3], 0)     

		#first number

#hex1 = "0x" + codeArray[5] + codeArray[6]
#					hex2 = "0x" + codeArray[7] + codeArray[8]
#					hex3 = "0x" + codeArray[9] + codeArray[10]
#					hex4 = "0x" + codeArray[11] + codeArray[12]
#					first_number = int(hex1,0)+int(hex2,0)+int(hex3,0)+int(hex4,0)
					first_number_hexstr = codeArray[5] + codeArray[6] + codeArray[7] + codeArray[8] + codeArray[9] + codeArray[10] + codeArray[11] + codeArray[12]
					#first_number = struct.unpack('f',struct.pack("i", int(first_number_hexstr, 16)))
					first_number = first_number_hexstr

		#second number
#					hex5 = "0x" + codeArray[13] + codeArray[14]
#					hex6 = "0x" + codeArray[15] + codeArray[16]
#					hex7 = "0x" + codeArray[17] + codeArray[18]
#					hex8 = "0x" + codeArray[19] + codeArray[20]
#					second_number = int(hex5,0)+int(hex6,0)+int(hex7,0)+int(hex8,0)
					second_number_hexstr = codeArray[13] + codeArray[14] + codeArray[15] + codeArray[16] + codeArray[17] + codeArray[18] + codeArray[19] + codeArray[20]
					#second_number = struct.unpack('f',struct.pack("i", int(second_number_hexstr, 16)))
					second_number = second_number_hexstr

					if( id_numb==EngineSerialIO.bus_measurement_id ):
						self.bus_current = first_number
						self.bus_voltage = second_number

					elif( id_numb==EngineSerialIO.velocity_measurement ):
						self.vehicle_velocity = first_number
						self.motor_velocity = second_number

					elif( id_numb==EngineSerialIO.phase_measurement_id ):
						self.phase_a_current = first_number
						self.phase_b_current = second_number

					elif( id_numb==EngineSerialIO.odometer_and_bus_amphours_measurement ):
						self.dc_bus_amphours = first_number
						self.odometer = second_number

					m1 = EngineSerialIO.enginePattern.search(self.temp_data)
				else:
					#print("pausing waiting on input")
					m1 = None
			time.sleep(1)

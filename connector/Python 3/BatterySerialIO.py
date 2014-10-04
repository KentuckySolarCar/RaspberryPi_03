from ThreadedSerialIO import ThreadedSerialIO
import re

class BatterySerialIO(ThreadedSerialIO):

	NUMB_OF_CELLS = 20

	#two of these will exsist BATMAN and ROBIN

	#Message Format Error
	#Message Corruption Error
	#Slave Timeout Error

	#20 numb of batteries
	#V[]
	#T[]
	#BC[]

	#A 'V' or a 'T' followed by a '[' with any number of 0-9s with a ']' after
	#or 'BC=' followed by any number of 0-9s
	batteryPattern = re.compile('([V|T]\\[[0-9]*\\]=[0-9]*|BC=[0-9]*)|BATMAN|ROBIN')

	dataRecognitionPattern = re.compile('([V|T]\\[[0-9]*\\]=[0-9]*|BC=[0-9]*)')
	batmanRecognitionPattern = re.compile('BATMAN')
	robinRecognitionPattern = re.compile('ROBIN')

	def determineType(cls, text):
		m1 = BatterySerialIO.batteryPattern.search(text)
		return m1 != None

	def __init__(self, t_port, t_rates, t_rate_id, t_fps_delay, t_data):
		super(BatterySerialIO, self).__init__( t_port, t_rates, t_rate_id, t_fps_delay, t_data)

		self.V = [0]*BatterySerialIO.NUMB_OF_CELLS
		self.T = [0]*BatterySerialIO.NUMB_OF_CELLS
		self.BC = 0

		# 0 - doesn't know
		# 1 - Batman
		# 2 - Robin
		self.identified_battery = 0

	#saves the current data in the data_buffer to 'p_file'
	def saveDataToFile(self,p_file,p_time):
		data_format = p_time + ":"
		i=0
		while i<BatterySerialIO.NUMB_OF_CELLS:
			data_format = data_format + str(self.V[i]) + "," + str(self.T[i]) + ";"
			i = i+1
		data_format = data_format + str(self.BC) + "\r\n"
		p_file.write(data_format)
		p_file.flush()

	def interpretData(self):
		while self.running:
			temp_data = self.getData()

			if(self.identified_battery == 0):
				if(BatterySerialIO.batmanRecognitionPattern.match(temp_data) != None):
					self.identified_battery = 1
				elif(BatterySerialIO.robinRecognitionPattern.match(temp_data) != None):
					self.identified_battery = 2
		
			m1 = BatterySerialIO.dataRecognitionPattern.match(temp_data) #True
			while m1 != None:
				temp_data = temp_data[temp_data.index(m1.group())+len(m1.group())+4 : len(temp_data)]

				print("data "+temp_data)
				self.storeData(m1.group())

				m1 = BatterySerialIO.dataRecognitionPattern.search(temp_data)

	def storeData(self, s_data):
		start_index = 0
		end_index = 0

		print("data2 "+s_data)

		if "V[" in  s_data:
			start_index = s_data.index("[")
			end_index = s_data.index("]",start_index)

			index = int(s_data[start_index+1 : end_index])

			start_index = s_data.index("=")

			value = int(s_data[start_index+1 : len(s_data)])

			self.V[index] = value

		elif "T[" in s_data:
			start_index = s_data.index("[")
			end_index = s_data.index("]",start_index)

			index = int(s_data[start_index+1 : end_index])

			start_index = s_data.index("=")

			value = int(s_data[start_index+1 : len(s_data)])

			self.T[index] = value
			
		elif "BC" in s_data:
			start_index = s_data.index("BC=")

			value = int(s_data[start_index+3 : len()])

			self.BC = value

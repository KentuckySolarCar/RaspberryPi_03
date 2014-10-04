from ThreadedSerialIO import ThreadedSerialIO

#this class is a placeholder class
class SerialIdentifier(ThreadedSerialIO):

	def determineType(cls,text):
		return False

	def __init__(self, t_port, t_rates, t_rate_id, t_fps_delay, t_data):
		super(SerialIdentifier, self).__init__( t_port, t_rates, t_rate_id, t_fps_delay, t_data)

	def interpretData(self):
		print("")

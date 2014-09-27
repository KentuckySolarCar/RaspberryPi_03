from ThreadedSerialIO import ThreadedSerialIO

class SerialIdentifier(ThreadedSerialIO):

	def __init__(self, t_port, t_rate, t_fps_delay):
		super(self, t_port, t_rate, t_fps_delay)

	def interpretData(self,p_file):
		if EngineSerialIO.determineType(): 
			pass
# ***added colon to if and pass

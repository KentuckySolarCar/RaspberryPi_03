import serial, time, io
from threading import Thread

class ThreadedSerialIO(object):
    
    def __init__(self, t_port, t_rates, t_rate_id, t_fps_delay, t_data):
        #the string port id
        self.port = t_port

        #the delay in loop() in ms
        self.fps_delay = t_fps_delay

        #the output rate of the port
        self.baud_rates = t_rates
        self.baud_rate_id = t_rate_id

        #the serial port
        self.ser = serial.Serial(self.port, baudrate=self.baud_rates[self.baud_rate_id], timeout=3, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

        #controlls the loop() method
        self.running = False

        #the name of the decoding type
        self.decode_identifier = 'ascii'

        #the string of information to be written to the file
        self.data_buffer = io.StringIO()
        self.data_buffer.write(t_data)

        #the main thread
        self.data_thread = None

        #the reader thread
        self.interprate_thread = None
        self.temp_data = ""

        #self explanitory
        self.readData = False;

        #temporary should become obsolite in python3
        #self.data_reader = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser,1), encoding = self.decode_identifier)

    def tryAnotherBaudRate(self):
        #self.stop()
        self.baud_rate_id = self.baud_rate_id + 1
        print(self.baud_rate_id)
        self.ser = serial.Serial(self.port, baudrate=self.baud_rates[self.baud_rate_id], timeout=3, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
        #self.start()

    def loop(self):
        while self.running:
            if(self.ser.isOpen()):
                try:
                    line = self.ser.read(26).decode(self.decode_identifier)
                    #print("read:",line)
                    if line: #check if the line is blank
                        self.data_buffer.write(line.replace("\r",""))
                        self.readData = True
                        #time.sleep(self.fps_delay/1000.0)
                    #no need to stop the whole thread
                    #else:
                    #self.stop()
                except UnicodeDecodeError:
                    self.tryAnotherBaudRate()

    #interprets data... this must be implemented by any subclass
    def interpretData(self):
        raise NotImplementedError( "Should have implemented this" )
                            
    def start(self):
        self.ser.close()
        self.ser.open()
        self.ser.write("S8\r".encode())
        self.ser.flush()
        self.ser.write("O\r".encode())
        self.ser.flush()
        self.running = True
        if self.data_thread == None:
            self.data_thread = Thread(target = self.loop)
        self.data_thread.start()
        print("Started Reading Port "+str(self.port)+" with baudrate of "+str(self.baud_rates[self.baud_rate_id]))
        if self.interprate_thread == None:
            self.interprate_thread = Thread(target = self.interpretData)
        self.interprate_thread.start()

    def stop(self):
        self.running = False
        self.data_thread.join()
        self.interprate_thread.join()
        print("Stopped Reading Port:"+str(self.port)+" with baudrate of "+str(self.baud_rates[self.baud_rate_id]))
    
    def setDecoder(self,decoder_id):
        if self.running:
            print("please call .stop() before calling this method")
        else:
            self.decode_identifier = decoder_id
            self.data_reader = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser,1), encoding = self.decode_identifier)

    def setUpdateRate(self,p_rate):
        self.update_rate = p_rate

    #removes the inforectly decoded text at the beginning of the dad_buffer
    def cleanUpData(self):
        self.data = self.data_value.getvalue()
        self.data_value.truncate(0)
        self.data.replace('^'+'@','')
        self.data_value.write(self.data)

    #saves the current data in the data_buffer to 'p_file'
    def saveDataToFile(self,p_file,p_time):
        raise NotImplementedError( "Should have implemented this" )

    def getData(self):
        self.readData = False
        s_text = self.data_buffer.getvalue()
        self.data_buffer = io.StringIO()
        return s_text

    def determineType(self,f_data):
        raise NotImplementedError( "Should have implemented this" )

    def hasReadData(self):
        return self.readData

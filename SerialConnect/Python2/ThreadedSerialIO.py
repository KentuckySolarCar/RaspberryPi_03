import serial, time, io, cStringIO
from threading import Thread

class ThreadedSerialIO():
    
    def __init__(self, t_port, t_rate, t_fps_delay):
        #the string port id
        self.port = t_port

        #the delay in loop() in ms
        self.fps_delay = t_fps_delay

        #the output rate of the port
        self.update_rate = t_rate

        #the serial port
        self.ser = serial.Serial(self.port, self.update_rate)
        print ser.name

        #controlls the loop() method
        self.running = False

        #the name of the decoding type
        self.decode_identifier = 'ascii'

        #the string of information to be written to the file
        self.data_buffer = cStringIO.StringIO()

        #the main thread
        self.data_thread = None

        #temporary should become obsolite in python3
        self.data_reader = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser,1), encoding = self.decode_identifier)

    def loop(self):
        while self.running:
            if(self.ser.isOpen()):
                print "waiting on input"
                #python3 line = self.ser.readline().decode(self.decode_identifier)[:-2]
                #python2
                line = self.data_reader.readline()
                print line
                if line: #check if the line is blank
                    self.data_buffer.write(line)
                    time.sleep(self.fps_delay/1000.0)
                else:
                    self.stop()
                            
    def start(self):
        self.running = True
        if self.data_thread == None:
            self.data_thread = Thread(target = self.loop)
        self.data_thread.start()
        print "Started Reading Port:"+str(self.port)

    def stop(self):
        self.running = False
        self.data_thread.join()
        print "Stopped Reading Port:"+str(self.port)
    
    def setDecoder(self,decoder_id):
        if self.running:
            print "please call .stop() before calling this method"
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
    def saveDataToFile(self,p_file):
        p_file.write(self.data_buffer.getvalue())
        self.data_buffer.truncate(0)
        p_file.flush()

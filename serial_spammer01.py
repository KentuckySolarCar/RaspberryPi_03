import serial, time, io
from datetime import datetime as dt
port = "/dev/pts/2"
ser = serial.Serial(port, 115200)
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), encoding = 'ascii')

time.sleep(.5)

for i in range (0, 25):
    sio.write(unicode("t5008ABD43CFE2D23DF3"))
    sio.write(unicode(str(i)))
    sio.write(unicode("\r"))
    sio.flush()
    time.sleep(0.01)




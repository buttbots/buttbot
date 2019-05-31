import serial
import time


ser = serial.Serial(port='COM9', baudrate = 9600)

#For sending :

time.sleep(1)
ser.write(b"m,10,33;")
print("test")
        
while time.process_time() < 5:
	read_serial=ser.readline()            
	print(read_serial)
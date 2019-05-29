import serial
import time


ser = serial.Serial(port='COM9', baudrate = 9600)
# Test serial connection


#For sending :

time.sleep(2)
ser.write(b"m,10,33;")
print("test")
        
while time.process_time() < 5:
	read_serial=ser.readline()            
	print(read_serial)
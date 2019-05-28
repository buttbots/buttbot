from __future__ import print_function
import tkinter as tk
import serial
import PIL
from PIL import Image,ImageTk
import threading
import datetime
import pytesseract
import imutils
import cv2
import os


"""
------------------------------------------
SERIELLE COMMUNICATION
------------------------------------------
"""
"""
# Connection
ser = serial.Serial(port='/dev/ttyACM0', baudrate = 9600)
# Test serial connection
s = [0]
while True:
	read_serial=ser.readline()            
	s[0] = str(int (ser.readline(),16))
	print(s[0])
	print(read_serial)
"""
"""
#For sending :
while True:
        ser.write(xCord.get(), yCord.get())
        time.sleep(1)
"""


"""
------------------------------------------
BUTTBOT GUI
------------------------------------------
"""
root = tk.Tk()
root.resizable(height = False, width = False)

HEIGHT = 800
WIDTH = 1600

# get cam frames
camheight = 800
camwidth = 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camwidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camheight)


# background
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

# orange background
background = tk.Frame(root, bg = "#e67300" )
background.place(relheight = 1, relwidth = 1)

# BUTTBOT Label
label = tk.Label(root, text = "BUTTBOT", bg = "#994d00", font =("IBM Plex",18))
label.place(anchor = "n", height = 50, width = 200, relx = 0.5, rely = 0.01)

# grey frame
greyframeheight = HEIGHT*0.8
greyframewidth = WIDTH*0.8

cordframe = tk.Frame(root, bg = "#994d00")
cordframe.place(height = int(greyframeheight), width = int(greyframewidth), relx = 0.1, rely = 0.1)

# X-coordinate
xCordLabel = tk.Label(cordframe, text = "X-Wert", bg = "#994d00")
xCordLabel.place(anchor = "n", relx = 0.2, y = 5)

X = tk.StringVar()
xCord = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = X)
xCord.place(anchor = "n", relx = 0.2, y = 25)

# Y-coordinate
yCordLabel = tk.Label(cordframe, text = "Y-Wert", bg = "#994d00")
yCordLabel.place(anchor = "n", relx = 0.2, y = 55)

Y = tk.StringVar()
yCord = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = Y)
yCord.place(anchor = "n", relx = 0.2, y = 75)

# "GO!" Button
def getxy():
    print(xCord.get(),yCord.get())

button = tk.Button(cordframe, command = getxy, height = 1, width = 16, bg = "#995c00", activebackground = "#b36b00", activeforeground = "#ffffff", text = "Go!", cursor = "target")
button.place(anchor = "n", relx = 0.2, y = 115)

# CAMSTREAM
camlabel = tk.Label(cordframe)
camlabel.place(anchor = "nw", height = greyframeheight, width = greyframewidth/2, x = greyframewidth/2)

def showframe():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img = PIL.Image.fromarray(cv2image)
	cam = ImageTk.PhotoImage(image=img)
	camlabel.cam = cam
	camlabel.configure(image=cam)
	camlabel.after(10, showframe)
	root.update

showframe()

root.mainloop()
"""
---------------------------------------------------------------------------
BUTTBOT GUI ENDE
----------------------------------------------------------------------------
"""
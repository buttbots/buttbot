from __future__ import print_function
import tkinter as tk
import serial
import numpy as np
import PIL
from PIL import Image,ImageTk
import threading
import time
import datetime
import pytesseract
import imutils
import cv2
import os
import subprocess

"""
--------------------------------------------------------------------------------
FUNCTIONS AND DATA
--------------------------------------------------------------------------------
"""
#Numpy array for polygon shape
shape = np.array([[0, 212.02022],[-0.830975, 211.70305],[-2.3010259, 211.12807],[-4.3209591, 210.3087],[-6.8084583, 209.25218],[-9.6883364, 207.96208],
[-12.892286, 206.43996],[-16.358395, 204.68677],[-20.030579, 202.70375],[-23.858021, 200.49301],[-27.794651, 198.05798],[-31.798706, 195.40367],[-35.83234, 192.53674],[-39.861324, 189.46568],
[-43.85479, 186.20068],[-47.78503, 182.75365],[-51.627327, 179.13806],[-55.359848, 175.36893],[-58.963524, 171.46259],[-62.421974, 167.43657],[-65.721428, 163.30939],
[-68.85067, 159.10039],[-71.800934, 154.82953],[-74.565872, 150.51717],[-77.141426, 146.18381],[-79.525757, 141.8499],[-81.719124, 137.53563],[-78.186401, 135.67329],
[-74.433983, 133.56046],[-70.499527, 131.18874],[-66.419914, 128.5508],[-62.23111, 125.64066],[-53.66478, 118.98743],[-49.354034, 115.24037],[-45.067535, 111.2133],
[-40.835785, 106.90871],[-36.688034, 102.33089],[-32.652237, 97.485954],[-28.755009, 92.381775],[-25.021545, 87.027946],[-18.139372, 75.618088],[-15.033542, 69.589417],
[-12.177121, 63.365719],[-9.5874548, 56.964531],[-7.2801471, 50.404999],[-3.5660315, 36.897682],[-1.1226108, 23.059383],[-0.39553642, 16.141909],[0, 9.4772148],[0.39553642, 16.141909],
[1.1226108, 23.059383],[2.1812406, 30.001831],[3.5660315, 36.897682],[7.2801471, 50.404999],[9.5874548, 56.964531],[12.177121, 63.365719],[15.033542, 69.589417],
[18.139372, 75.618088],[21.475592, 81.435753],[25.021545, 87.027946],[28.755009, 92.381775],[32.652237, 97.485954],[36.688034, 102.33089],[40.835785, 106.90871],[45.067535, 111.2133],
[49.354034, 115.24037],[53.66478, 118.98743],[57.968086, 122.45382],[62.23111, 125.64066],[66.419914, 128.5508],[70.499527, 131.18874],[74.433983, 133.56046],[81.719124, 137.53563],[79.525757, 141.8499],
[77.141426, 146.18381],[74.565872, 150.51717],[71.800934, 154.82953],[68.85067, 159.10039],[65.721428, 163.30939],[62.421974, 167.43657],[58.963524, 171.46259],[55.359848, 175.36893],
[51.627327, 179.13806],[47.78503, 182.75365],[43.85479, 186.20068],[39.861324, 189.46568],[35.83234, 192.53674],[31.798706, 195.40367],[27.794651, 198.05798],
[23.858021, 200.49301],[20.030579, 202.70375],[16.358395, 204.68677],[12.892286, 206.43996],[9.6883364, 207.96208],[6.8084583, 209.25218],[4.3209591, 210.3087],
[2.3010259, 211.12807],[0.830975, 211.70305],[0, 212.02022]])


"""
-------------------------------------------------------------------------------
SERIELLE COMMUNICATION AND CAMDRIVER
-------------------------------------------------------------------------------
"""
ser = serial.Serial(port='/dev/ttyACM0', baudrate = 9600)

subprocess.call(["sudo","modprobe","bcm2835-v4l2"]) 
"""
-------------------------------------------------------------------------------
BUTTBOT GUI
-------------------------------------------------------------------------------
"""




root = tk.Tk()
root.resizable(height = False, width = False)


HEIGHT = 720
WIDTH = 1280

XVar = tk.StringVar()
YVar = tk.StringVar()

XVar.set(0)
YVar.set(0)

# get cam frames
camheight = 480
camwidth = 640
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
#logoimage = Image.open("Buttbotlogo.png")
#buttbotimage = ImageTk.PhotoImage(logoimage)
label = tk.Label(root, text = "BUTTBOT", bg = "#994d00", font =("IBM Plex",18))
label.place(anchor = "n", height = 50, width = 200, relx = 0.5, rely = 0.01)

# grey frame
greyframeheight = HEIGHT*0.8
greyframewidth = WIDTH*0.8

cordframe = tk.Frame(root, bg = "#994d00")
cordframe.place(height = int(greyframeheight), width = int(greyframewidth), relx = 0.1, rely = 0.1)

# X-coordinate
xCordEntryLabel = tk.Label(cordframe, text = "X-Wert", bg = "#994d00")
xCordEntryLabel.place(anchor = "n", relx = 0.1, y = 5)

xCordEntry = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = XVar)
xCordEntry.place(anchor = "n", relx = 0.1, y = 25)

# Y-coordinate
yCordEntryLabel = tk.Label(cordframe, text = "Y-Wert", bg = "#994d00")
yCordEntryLabel.place(anchor = "n", relx = 0.1, y = 55)

yCordEntry = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = YVar)
yCordEntry.place(anchor = "n", relx = 0.1, y = 75)

# the "GO!" BUTTON sends the x and y-coordinates serial to the arduino
def send_coords():
	print("Sending (%s,%s)!" % (XVar.get(), YVar.get()))
	time.sleep(1)
	ser.write(b"m,%d,%d;" % (int(XVar.get()),int(YVar.get())))


button = tk.Button(cordframe, command = send_coords, height = 1, width = 16, bg = "#995c00", activebackground = "#b36b00", activeforeground = "#ffffff", text = "Go!", cursor = "target")
button.place(anchor = "n", relx = 0.1, y = 115)

# CAMSTREAM
# camlabel where the stream is shown
camlabel = tk.Label(cordframe, bg = "black")
camlabel.place(anchor = "nw", height = camheight, width = camwidth, x = greyframewidth/3 + 44)

# scaling functions for the coordinate systems : 
# take the new scale : 166x212 and devide by the old scale 640x480: 166/640= 0.2594 and 212/480= 0.4417
# the addition and subtraction is for the right positioning 
def scale_xcoord(x):
	newx = x * 0.2594 - 83
	return int(newx)

def scale_ycoord(y):
	newy = -y * 0.4417 + 212
	return int(newy)

def descale_xcoord(x):
	oldx = x + 83 
	oldx = oldx * 3.8554
	return int(oldx)

def descale_ycoord(y):
	oldy = y - 212
	oldy = oldy * -2.2642
	return int(oldy)

# Videostream
def showframe():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1,)
	# frame perspective tranformation to the trapez-points (result)
	pts1 = np.float32([[128,127],[517,116], [55,443],[617,430]])		#dst points
	pts2 = np.float32([[0,0],[640,0],[0,480],[640,480]])		#src points
	matrix = cv2.getPerspectiveTransform(pts1, pts2)			# calculates the tranformation matrix
	result = cv2.warpPerspective(frame, matrix, (camwidth,camheight))
	# scaling for polygon
	#descaleshape = shape + np.array([83,-212])
	#descaleshape = descaleshape * np.array([3.8553,-2.2642])
	# polygon
	#cv2.polylines(result, descaleshape, True, (0,0,255), thickness = 3)
	# implement the stream in tkinter and the camlabel
	result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
	img = PIL.Image.fromarray(result)
	cam = ImageTk.PhotoImage(image=img)
	camlabel.cam = cam
	camlabel.configure(image=cam)
	camlabel.after(10, showframe)

showframe()



# mouseclick
def click_coords(event):
	XVar.set(scale_xcoord(event.x))
	YVar.set(scale_ycoord(event.y))
	print("clicked at", XVar.get(), YVar.get())

camlabel.bind("<Button-1>", click_coords)



root.mainloop()
"""
---------------------------------------------------------------------------
BUTTBOT GUI ENDE
----------------------------------------------------------------------------
"""
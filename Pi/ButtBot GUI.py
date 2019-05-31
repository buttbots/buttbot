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
SERIELLE COMMUNICATION
-------------------------------------------------------------------------------
"""
#ser = serial.Serial(port='COM9', baudrate = 9600)

"""
-------------------------------------------------------------------------------
BUTTBOT GUI
-------------------------------------------------------------------------------
"""
root = tk.Tk()
root.resizable(height = False, width = False)

HEIGHT = 720
WIDTH = 1280

# get cam frames
camheight = 640
camwidth = 480
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

# "GO!" Button should send the x and y-coordinates serial to the arduino

def send_coords():
	time.sleep(1)
	ser.write(b"m,%d,%d;" % (xCord.get(),yCord.get()))

button = tk.Button(cordframe, command = send_coords, height = 1, width = 16, bg = "#995c00", activebackground = "#b36b00", activeforeground = "#ffffff", text = "Go!", cursor = "target")
button.place(anchor = "n", relx = 0.2, y = 115)



# CAMSTREAM
# camlabel where the stream is shown
camlabel = tk.Label(cordframe, bg = "black")
camlabel.place(anchor = "nw", height = camheight, width = camwidth, x = greyframewidth/2 + 32)


def showframe():
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	# frame perspective tranformation to the trapez-points (result)
	pts1 = np.float32([[225,160],[390,160],[210,350],[430,350]])
	pts2 = np.float32([[0,0],[402,0], [0,500],[402,500]])
	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	result = cv2.warpPerspective(frame, matrix, (402,500))
	# scaling for polygon
	scalingfactor = (212 - 9.447)/500
	scaleshape = shape / (scalingfactor) + np.array([[201,0]])
	# polygon
	cv2.polylines(result, np.int32([scaleshape]), True, (0,0,255), thickness = 3)
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
	clickedx = event.x
	clickedy = event.y
	print("clicked at", clickedx, clickedy)
camlabel.bind("<Button-1>", click_coords)






root.mainloop()
"""
---------------------------------------------------------------------------
BUTTBOT GUI ENDE
----------------------------------------------------------------------------
"""
import tkinter as tk
import serial

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

HEIGHT = 600
WIDTH = 800


# Hintergrund 
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

# oranger Hintergrund
background = tk.Frame(root, bg = "#e67300" )
background.place(relheight = 1, relwidth = 1)

# BUTTBOT Überschrift
label = tk.Label(root, text = "BUTTBOT", bg = "#994d00", font =("IBM Plex",18))
label.place(anchor = "n", height = 50, width = 200, relx = 0.5, rely = 0.01)

# grauer Frame
cordframe = tk.Frame(root, bg = "#994d00")
cordframe.place(relheight = 0.8, relwidth = 0.8, relx = 0.1, rely = 0.1)

# X-Koordinate
xCordLabel = tk.Label(cordframe, text = "X-Wert", bg = "#994d00")
xCordLabel.place(anchor = "n", relx = 0.2, y = 5)

X = tk.StringVar()
xCord = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = X)
xCord.place(anchor = "n", relx = 0.2, y = 25)

# Y-Koordinate
yCordLabel = tk.Label(cordframe, text = "Y-Wert", bg = "#994d00")
yCordLabel.place(anchor = "n", relx = 0.2, y = 55)

Y = tk.StringVar()
yCord = tk.Entry(cordframe, bd = 1, bg = "gray", textvariable = Y)
yCord.place(anchor = "n", relx = 0.2, y = 75)

# Knopf
def getxy():
    print(xCord.get(),yCord.get())

button = tk.Button(cordframe, command = getxy, height = 1, width = 16, bg = "#995c00", activebackground = "#b36b00", activeforeground = "#ffffff", text = "Go!", cursor = "target")
button.place(anchor = "n", relx = 0.2, y = 115)


root.mainloop()
"""
BUTTBOT GUI ENDE
"""
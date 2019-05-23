import tkinter as tk

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
label = tk.Label(root, text = "BUTTBOT", bg = "#994d00")
label.place(anchor = "n", height = 50, width = 200, relx = 0.5, rely = 0.01 )

# grauer Frame
cordframe = tk.Frame(root, bg = "#994d00")
cordframe.place(relheight = 0.8, relwidth = 0.5, relx = 0.05, rely = 0.1)

# X-Koordinate
xCord = tk.Entry(cordframe, bd = 1, bg = "gray")
xCord.grid(row = 4, column = 4)

xCordLabel = tk.Label(cordframe, text = "X-Wert", bg = "#994d00")
xCordLabel.grid(row = 3, column = 4)

# Y-Koordinate
yCord = tk.Entry(cordframe, bd = 1, bg = "gray")
yCord.grid(row = 7, column = 4)

yCordLabel = tk.Label(cordframe, text = "Y-Wert", bg = "#994d00")
yCordLabel.grid(row = 6, column = 4)

# Knopf
buttonLabel = tk.Label(cordframe, text = "(%s) ansteuern." % (xCord.get()), bg = "#994d00")
buttonLabel.grid(row = 8, column = 4)


button = tk.Button(cordframe, height = 1, width = 16, bg = "#995c00", text = "Go!")
button.grid(row = 12, column = 4)






root.mainloop()


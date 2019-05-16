
from tkinter import *
from PIL import ImageTk, Image



def test():
    print("test")
root = Tk()
root.geometry("1024x600")

################# TOP FRAME ##################
topFrame = Frame(root,bg = "red",width = 600,height = 200)
topFrame.pack(side = TOP,fill = X)


loadButton = Button(topFrame,text = 'LOAD GCODE', width = 10 ,height = 1)
loadButton.place(x = 20,y = 20 )

gcodeDirLabel = Label(topFrame,text = 'Gcode Directory',width = 80, height = 1 )
gcodeDirLabel.place(x = 150,y = 22)

connectBotton = Button(topFrame,text = 'CONNECT',width = 30 ,height = 1)
connectBotton.place(x = 20,y = 90)

printButton = Button(topFrame,text = 'PRINT',width = 30 ,height = 1)
printButton.place(x = 300 ,y = 90)

pauseButton = Button(topFrame,text = 'PAUSE',width = 30 ,height = 1)
pauseButton.place(x = 580,y = 90)


################# MID FRAME ##################
midFrame = Frame(root,bg = "blue",width = 600,height = 200)
midFrame.pack(side = TOP, fill = X)

#Input Box for both
inputBoxForBoth = Entry(midFrame,width = 50)
inputBoxForBoth.place(x = 350,y = 20)
################ BOTTOM FRAME ################
bottomFrame = Frame(root,bg = "green",width = 600,height = 200)
bottomFrame.pack(side = TOP, fill = X)

mainloop() 

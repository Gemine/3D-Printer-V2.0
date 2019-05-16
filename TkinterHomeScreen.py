
from tkinter import *
from PIL import ImageTk, Image



def test():
    print("test")
root = Tk()
root.geometry("1024x600")

################# TOP FRAME ##################
topFrame = Frame(root,bg = "red",width = 600,height = 200)
topFrame.pack(side = TOP,fill = X)

##loadButton.pack(side = LEFT, padx = 10, pady = 10)
#loadButton.place(x = 10,y = 10 )

gcodeDirLabel = Label(topFrame,text = 'Gcode Directory',width = 80, height = 1 )
#gcodeDirLabel.pack(side = LEFT)

connectBotton = Button(topFrame,text = 'CONNECT',width = 10 ,height = 1)
#connectBotton.pack(side = LEFT, anchor = SW)
connectBotton.place(x = 10,y = 90)


################# MID FRAME ##################
midFrame = Frame(root,bg = "blue",width = 600,height = 200)
midFrame.pack(side = TOP, fill = X)
################ BOTTOM FRAME ################
bottomFrame = Frame(root,bg = "green",width = 600,height = 200)
bottomFrame.pack(side = TOP, fill = X)

mainloop() 

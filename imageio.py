from Tkinter import *
from tkFileDialog   import askopenfilenames

def OpenFile():
    name = askopenfilenames()
    print name

def Circumsize():
    options_window = Tk()
    options_window.mainloop()

class AppUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New")
        menu.add_command(label="Open...", command=OpenFile)

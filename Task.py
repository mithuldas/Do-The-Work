from tkinter import *
from PIL import ImageTk,Image

class Task:

    description=0
    weight=0
    position=0
    
    def printDetails(self):
        print (self.description)
        print (self.weight)

    def getDetails(self):
        return "TD " + self.description + "\n" + "TW " + str(self.weight)

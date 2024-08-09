from tkinter import *

class ChildWindow:
    def __init__(self, parent, width, height, title = "New child Window", resizable=(False, False)):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(resizable[0], resizable[1])

        self.root.bind("Escape", self._close)
   
    def run(self):
        pass

    def _close(self, event):
        self.root.quit()
    
    def drawMenu(self):
        pass

    def drawWigets(self):
        pass
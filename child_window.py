from tkinter import *

class ChildWindow:
    def __init__(self, parent, width, height, title = "New child Window", resizable=(False, False)):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(resizable[0], resizable[1])

        self.root.bind("<Escape>", self._close)

        self.grabFocus()
   
    def run(self):
        pass

    def grabFocus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def _close(self, event="None"):
        self.root.destroy()
    
    def drawMenu(self):
        pass

    def drawWigets(self):
        pass
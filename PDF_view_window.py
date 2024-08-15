from tkinter import *
from tkinter.ttk import Notebook

class ChildWindow():
    def __init__(self, parent, width, height, title = "New child Window", resizable=(False, False)):
        self.root = Toplevel(parent)
        self.root.title(title)
        x, y = self.find_screen_center(width, height)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.root.resizable(resizable[0], resizable[1])

        self.root.bind("<Escape>", self._close)

        self.grabFocus()
    
    def find_screen_center(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return x, y
   
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
        self.img_tabs = Notebook(self.root)
        self.img_tabs.enable_traversal()
        self.img_tabs.pack(fill="none", expand=1, anchor="center")
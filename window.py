from tkinter import *
from child_window import ChildWindow

class Window:
    def __init__(self, width, height, resizable=(False, False)):
        self.root = Tk()
        self.root.title("Photo Editor")
        #self.root.iconbitmap("icons/icon.img")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(resizable[0], resizable[1])

        self.root.bind("<Escape>", self._close)
   
    def run(self):
        self.drawMenu()
        self.drawWigets()

        self.root.mainloop()

    def _close(self, event):
        self.root.quit()
    
    def drawMenu(self):
        pass

    def drawWigets(self):
        pass

    def createChildWindow(self, width, height, title = "New child Window", resizable=(False, False)):
        ChildWindow(self.root, width, height, title, resizable)

if __name__ == "__main__":
    window = Window (500, 200)
    window.run()
    window.createChildWindow(500, 400)
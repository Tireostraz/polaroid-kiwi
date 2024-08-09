from tkinter import *

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Photo Editor")
        #self.root.iconbitmap("icons/icon.img")

        self.root.bind("Escape", self._close)
   
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

if __name__ == "__main__":
    Window.run()
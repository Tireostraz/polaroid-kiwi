from tkinter import *
from tkinter import filedialog as fd
from child_window import ChildWindow
from PIL import Image, ImageTk


class Window:
    def __init__(self, width, height, resizable=(False, False)):        
        self.root = Tk()
        self.root.title("Photo Editor")
        self.root.iconbitmap("resources/icon.ico")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(resizable[0], resizable[1])

        img = Image.open(r"resources\cat.jpg")
        img = img.resize((50, 50))
        self.image = ImageTk.PhotoImage(img)

        self.root.bind("<Escape>", self._close)
   
    def run(self):
        self.drawMenu()
        self.drawWigets()
        self.root.mainloop()

    def _close(self, event):
        self.root.destroy()
    
    def drawMenu(self):
        menu_bar = Menu(self.root)
        file_bar = Menu(menu_bar, tearoff=0)        
        menu_bar.add_cascade(label="File", menu=file_bar)

        file_bar.add_command(label="Open", command=self.openImage)
        file_bar.add_command(label="Save")
        file_bar.add_command(label="Save as...")
        self.root.configure(menu=menu_bar)

    def openImage(self):
        image_path = fd.askopenfilename(filetypes=(("Images", "*.jpg; *.png; *.jpeg"), ))
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((200, 200))
        image = ImageTk.PhotoImage(pil_image)
        image_panel = Label(self.root, image=image)
        image_panel.image = image
        image_panel.pack()

    def drawWigets(self):
        pass


if __name__ == "__main__":
    window = Window (500, 500)  
    window.run()
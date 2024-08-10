from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from child_window import ChildWindow
from PIL import Image, ImageTk
import os


class Window:
    def __init__(self, width, height, resizable=(True, True)):        
        self.root = Tk()
        x, y = self.find_screen_center(width, height)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.root.resizable(resizable[0], resizable[1])
        self.init()
    
    def init(self):
        self.root.title("Photo Editor")
        self.root.iconbitmap("resources/icon.ico")
        self.opened_images = []
        self.radio_choice = IntVar(value=0)        

    def find_screen_center(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return x, y    

    def run(self):
        self.drawMenu()
        self.drawWigets()
        self.binds()
        self.root.mainloop()
    
    def binds(self):
        self.root.bind("<Escape>", self._close)
        #self.root.bind("<r>", lambda: self.rotate_image(90))

    def _close(self, event=None):
        choice = mb.askyesno("Exit", "Do you really want to exit?")
        if choice:
            self.root.destroy()
        else:
            return
    
    def drawMenu(self):
        menu_bar = Menu(self.root)      

        #File менюбар
        file_bar = Menu(menu_bar, tearoff=0)   
        menu_bar.add_cascade(label="File", menu=file_bar)
        file_bar.add_command(label="Open", command=self.open_image)
        file_bar.add_command(label="Save", command=self.save_current_image)
        file_bar.add_command(label="Save as...", command=self.save_image_as)
        file_bar.add_separator()
        file_bar.add_command(label="Exit", command=self._close)

        #Edit менюбар        
        edit_bar = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_bar)
        rotate_bar = Menu(edit_bar, tearoff=0)
        edit_bar.add_cascade(label="Rotate", menu=rotate_bar)
        rotate_bar.add_command(label="Rotate left 90", command=lambda: self.rotate_image(90))

        self.root.configure(menu=menu_bar)

    def drawWigets(self):
        top_frame = Frame(self.root)
        top_frame.pack()
        bottom_frame = Frame(self.root)
        bottom_frame.pack()
        self.img_tabs = Notebook(top_frame)
        self.img_tabs.enable_traversal()
        self.img_tabs.pack(fill="both", expand=1)
        Radiobutton(bottom_frame, variable=self.radio_choice, value=0, text="Standard").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=1, text="Mini").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=2, text="Square").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=3, text="Max").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=4, text="10x15").pack(side="left")
    
    def drawRadiobuttons(self):
        pass

    def get_current_working_data(self):
        #returns current_tab, path, image
        current_tab = self.img_tabs.select()
        if not current_tab:
            return None, None, None
        tab_index = self.img_tabs.index(current_tab)
        path, image = self.opened_images[tab_index]
        return current_tab, path, image
        
    def open_image(self):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpg; *.png; *.jpeg"), ))
        for image_path in image_paths:
            self.add_new_image(image_path)

    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((300, 300))
        self.opened_images.append([image_path, image])
        image_tk = ImageTk.PhotoImage(image)
        self.img_tab = Frame(self.img_tabs)
        self.img_tabs.add(self.img_tab, text=f"{image_path.split("/")[-1]}")
        # self.image_panel = Label(self.img_tab, text="Hello", image=image_tk)
        # self.image_panel.image = image_tk
        # self.image_panel.pack()
        image_panel = Canvas(self.img_tab, width=300, height=300)
        image_panel.image = image_tk
        image_panel.create_image(0, 0, image=image_tk, anchor="nw")
        image_panel.pack(expand="yes")

    def update_image(self, current_tab, image):
        current_frame = self.img_tabs.children[current_tab[current_tab.rfind("!"):]] #поиск дочернего виджета текущей Frame в Tabs
        canvas = current_frame.children["!canvas"] #поиск дочернего элемента Label в виджете frame
        image_tk = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.image = image_tk
        canvas.create_image(0, 0, image=image_tk, anchor="nw")

        
        tab_index = self.img_tabs.index(current_tab)
        self.opened_images[tab_index][1] = image

        #добавить * при изменении картинки
        image_path = self.opened_images[tab_index][0]
        if image_path[-1] == "*":
            return
        image_path += "*"
        self.opened_images[tab_index][0] = image_path
        self.img_tabs.tab(current_tab, text=f"{image_path.split("/")[-1]}")

    def rotate_image(self, degree):
        current_tab, image_path, image = self.get_current_working_data()
        if not current_tab:
            return

        image = image.rotate(degree, expand=True)
        self.update_image(current_tab, image)
        
    def save_image_as(self):
        current_tab, image_path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_index = self.img_tabs.index(current_tab)

        old_path, old_ext = os.path.splitext(image_path)
        if old_path[-1] == "*":
            old_ext = old_ext[:-1]        
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpg; *.png; *.jpeg"), ))
        if not new_path:
            return
        new_path, new_ext = os.path.splitext(new_path)
        if not new_ext:
            new_ext = old_ext
        elif old_ext != new_ext:
            mb.showerror("Error", f"Новое расширение картинки не равно старому, {old_ext} != {new_ext}")
            return
        image.save(new_path + new_ext)
        image.close()

        del self.opened_images[tab_index]
        self.img_tabs.forget(tab_index)

        self.add_new_image(new_path + new_ext)
    
    def save_current_image(self):
        current_tab, image_path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_index = self.img_tabs.index(current_tab)
        if image_path[-1] == "*":
            image_path = image_path[:-1]
            self.opened_images[tab_index][0] = image_path
            image.save(image_path)
            self.img_tabs.add(current_tab, text=image_path.split("/")[-1])


if __name__ == "__main__":
    window = Window (500, 500)  
    window.run()
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from child_window import ChildWindow
from PIL import Image, ImageTk
import os

from image_info import ImageInfo
from sheetA4 import SheetA4

class Editor:
    def __init__(self, width, height, resizable=(True, True)):     
        self.sheet = SheetA4()
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
        self.working_rectangle = None
        self.thumbnail_rectangle = None
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
        file_bar.add_command(label="Export all as PDF", command=self.save_image_as)
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
        top_frame.pack(expand=1, anchor="center")
        Label(top_frame, text="Scale factor")
        bottom_frame = Frame(self.root)
        bottom_frame.pack(expand=1, anchor="center")
        self.img_tabs = Notebook(top_frame)
        self.img_tabs.enable_traversal()
        self.img_tabs.pack(fill="none", expand=1, anchor="center")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=0, text="Standard").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=1, text="Mini").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=2, text="Square").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=3, text="Max").pack(side="left")
        Radiobutton(bottom_frame, variable=self.radio_choice, value=4, text="10x15").pack(side="left")
        Button(bottom_frame, text="Draw frame", command=self.draw_frame).pack(side="left")
        Button(bottom_frame, text="Crop image", command=self.crop_image).pack(side="left")
        Button(bottom_frame, text="Create polaroid", command=self.create_polaroid).pack(side="left")

    def get_format(self):
        if self.radio_choice.get() == 0: #Standard polaroid
            ratio = 5/6
            format = "Standard"
            return [ratio, format]
        elif self.radio_choice.get() == 1: #Mini
            ratio = 2/3
            format = "Mini"
            return [ratio, format]
        elif self.radio_choice.get() == 2: #Square
            ratio = 1
            format = "Square"
            return [ratio, format]
        elif self.radio_choice.get() == 3: #Max
            ratio = 20/21
            format = "Max"
            return [ratio, format]
        elif self.radio_choice.get() == 4: #10x15
            ratio = 2/3
            format = "10x15"
            return [ratio, format]
        
    def draw_frame(self):
        image_info = self.current_image()
        if not image_info:
            return
        
        x0, y0, x1, y1 = self.frame_size(image_info.thumbnail)

        canvas = image_info.canvas
        canvas.delete(self.working_rectangle)
        self.working_rectangle = canvas.create_rectangle(x0, y0, x1, y1, dash=(10, 10), fill='cyan', width=1, stipple="gray25")        
        canvas.focus_set()
        canvas.bind("<Left>", self.move_left)
        canvas.bind("<Right>", self.move_right)
        canvas.bind("<Up>", self.move_up)
        canvas.bind("<Down>", self.move_down)
    
    def move_left(self, event):
        image = self.current_image()
        image.canvas.move(self.working_rectangle, -5, 0)

    def move_right(self, event):
        image = self.current_image()
        image.canvas.move(self.working_rectangle, 5, 0)

    def move_up(self, event):
        image = self.current_image()
        image.canvas.move(self.working_rectangle, 0, -5)

    def move_down(self, event):
        image = self.current_image()
        image.canvas.move(self.working_rectangle, 0, 5)
        
     
    def frame_size(self, image):
        img_width, img_height = image.size
        ratio = self.get_format()
        if img_width/img_height < ratio[0]:
            frame_width = img_width
            frame_height = img_width/ratio[0]
        elif img_width/img_height >= ratio[0]:
            frame_height = img_height
            frame_width = img_height * ratio[0]
        x_start = img_width/2 - frame_width/2
        y_start = img_height/2 - frame_height/2
        x_end = img_width/2 + frame_width/2
        y_end = img_height/2 + frame_height/2
        return x_start, y_start, x_end, y_end
    
    def create_polaroid(self):
        image = self.current_image()
        # format = self.get_format()
        image.resize_to_format()
        self.update_image(image)
        # self.sheet.concat_image(image, format[1])
        
    def current_image(self):
        current_tab = self.img_tabs.select()
        if not current_tab:
            return None
        tab_index = self.img_tabs.index(current_tab)        
        return self.opened_images[tab_index]
        
    def open_image(self):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpg; *.png; *.jpeg"), ))
        for image_path in image_paths:
            self.add_new_image(image_path)

    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image_tab = Frame(self.img_tabs)
        image_info = ImageInfo(image, image_path, image_tab)
        self.opened_images.append(image_info)

        image_tk = image_info.image_tk
               
        image_panel = Canvas(image_tab, width=500, height=500, bd=0, highlightthickness=0)
        image_panel.image = image_tk
        image_panel.create_image(0, 0, image=image_tk, anchor="nw")
        image_panel.pack(expand="no", anchor="center")
        image_info.canvas = image_panel

        self.img_tabs.add(image_tab, text=image_info.image_name())
        self.img_tabs.select(image_tab)

    def update_image(self, image_info):
        image_info.update_image_on_canvas()
        self.img_tabs.tab(image_info.tab, text=image_info.image_name())

    def rotate_image(self, degrees):
        image = self.current_image()
        if not image:
            return
        
        image.rotate(degrees)
        image.unsaved = True
        self.update_image(image)

    def crop_image(self):
        image = self.current_image()
        if not image:
            return
        image.crop(*image.canvas.coords(self.working_rectangle))
        format = self.get_format()
        format = format[1]
        image.set_format(format)
        image.unsaved = True
        self.update_image(image)
        
    def save_image_as(self):
        current_tab, image_path, image = self.current_image()
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
        image = self.current_image()
        if not image.tab:
            return
        if image.unsaved:
            image.unsaved = False
            image.image.save(image.path)
            self.img_tabs.add(image.tab, text=image.path)


if __name__ == "__main__":
    window = Editor (800, 800)  
    window.run()
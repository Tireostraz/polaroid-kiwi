from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from PDF_view_window import ChildWindow
from PIL import Image, ImageTk
import os
import customtkinter

from image_info import ImageInfo
from sheetA4 import SheetA4

class Editor:
    def __init__(self, width, height, resizable=(True, True)):
        self.root = customtkinter.CTk()
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")
        x, y = self.find_screen_center(width, height)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.root.resizable(resizable[0], resizable[1])
        self.init()
    
    def init(self):
        self.root.title("Photo Editor")
        self.root.iconbitmap("resources/icons/icon.ico")
        self.opened_images = []
        self.opened_sheets = []
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
        self.root.bind("<Return>", self.create_polaroid)

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
        file_bar.add_command(label="Export all as PDF", command=self.export_all)
        file_bar.add_separator()
        file_bar.add_command(label="Close", command=self.close_image)
        file_bar.add_command(label="Exit", command=self._close)

        #Edit менюбар        
        edit_bar = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_bar)
        rotate_bar = Menu(edit_bar, tearoff=0)
        edit_bar.add_cascade(label="Rotate", menu=rotate_bar)
        rotate_bar.add_command(label="Rotate left 90", command=lambda: self.rotate_image(90))

        self.root.configure(menu=menu_bar)

    def drawWigets(self):
        top_frame = customtkinter.CTkFrame(self.root, width=600, height=600)
        top_frame.pack(expand=True)
        # top_frame.grid(row=0, column=0, sticky="n")
        bottom_frame = customtkinter.CTkFrame(self.root)
        bottom_frame.pack()
        # bottom_frame.grid(row=1, column=0, sticky="esw")
        self.img_tabs = Notebook(top_frame)
        self.img_tabs.enable_traversal()
        self.img_tabs.pack(fill="none", expand=1, anchor="center")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=0, text="Standard").grid(row=0, column=0)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=1, text="Mini").grid(row=0, column=1)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=2, text="Square").grid(row=0, column=2)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=3, text="Max").grid(row=0, column=3)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=4, text="10x15").grid(row=0, column=4)
        customtkinter.CTkButton(bottom_frame, text="Draw frame", command=self.draw_frame).grid(row=1, column=1)
        customtkinter.CTkButton(bottom_frame, text="Crop image", command=self.crop_image).grid(row=1, column=2)
        customtkinter.CTkButton(bottom_frame, text="Create polaroid", command=self.create_polaroid).grid(row=1, column=3)
        rotate_left_img = ImageTk.PhotoImage(Image.open(r".\resources\icons\rotate_left.png"))
        rotate_right_img = ImageTk.PhotoImage(Image.open(r".\resources\icons\rotate_right.png"))
        # rotate_left_img = PhotoImage(file=r'resources\icons\rotate-left.jpg')
        customtkinter.CTkButton(bottom_frame, text="Rotate left", image=rotate_left_img, compound="left", command=lambda: self.rotate_image(90)).grid(row=2, column=1)
        customtkinter.CTkButton(bottom_frame, text="Rotate right", image=rotate_right_img, command=lambda: self.rotate_image(-90)).grid(row=2, column=3)

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
    
    def create_polaroid(self, event=None):
        image = self.current_image()
        if not image:
            return
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

    def close_image(self):
        image_info = self.current_image()
        tab_index = self.img_tabs.index(image_info.tab)
        image_info.image.close()
        del self.opened_images[tab_index]
        self.img_tabs.forget(image_info.tab)

    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image_tab = Frame(self.img_tabs)
        image_info = ImageInfo(image, image_path, image_tab)
        self.opened_images.append(image_info)
        
        image_tk = image_info.image_tk

        image_panel = Canvas(image_tab, width=image_info.thumbnail.width, height=image_info.thumbnail.height, bd=0, background="cyan", highlightthickness=0)
        image_panel.pack()
        image_panel.image = image_tk

        image_panel.create_image(0, 0, image=image_tk, anchor="nw")        
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
        
    def export_all(self):
        formats = []
        for image in self.opened_images:
            if image.format not in formats:
                formats.append(image.format)
        print(formats)
        for format in formats:
            sheet = SheetA4(format)
            self.opened_sheets.append(sheet)
            for image in self.opened_images:
                if format == image.format and sheet.occupied == False:
                    sheet.add_image_on_sheet(image.image, format)
                elif format == image.format and sheet.occupied:
                    sheet = SheetA4(format)
                    self.opened_sheets.append(sheet)
                    sheet.add_image_on_sheet(image.image, format)
        
        self.save_sheets_as_pdf()

    def save_sheets_as_pdf(self):
        i = 0
        image = self.current_image()
        old_path = image.full_path(True)
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Portable Document Format", "*.pdf"), ))
        if not new_path:
            return
        new_path, new_ext = os.path.splitext(new_path)
        print(f"New path: {new_path}, New ext: {new_ext}")
        for sheet in self.opened_sheets:
            print(new_path + f"_{i}" + new_ext)
            sheet.sheet.save(new_path + f"_{i}" + new_ext)
            sheet.sheet.close()
            del sheet.sheet
            i +=1

if __name__ == "__main__":
    window = Editor (700, 700, (False, False))  
    window.run()
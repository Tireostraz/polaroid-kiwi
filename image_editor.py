from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from tkinter import colorchooser
from PDF_view_window import ChildWindow
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener #for heic images
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
        register_heif_opener() #for heic images
        self.init()
    
    def init(self):
        self.root.title("Photo Editor")
        # self.root.iconbitmap("resources/icons/icon.ico")
        self.opened_images = []
        self.opened_sheets = []
        self.radio_choice = IntVar(value=0)
        self.checkbox_autoframe = customtkinter.StringVar(value="on")
        self.working_rectangle = None
        self.thumbnail_rectangle = None
        self.DPI = 300
        self.polaroid_bg_color = (255, 255, 255)
        self.polaroid_border_color = (225, 225, 225)
        self.AdobeRGB = r".\resources\icc\AdobeRGB1998.icc"

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
        file_bar.add_command(label="Convert ICC to AdobeRGB", command=self.convert_icc)
        file_bar.add_separator()
        file_bar.add_command(label="Close", command=self.close_image)
        file_bar.add_command(label="Close all", command=self.close_images)
        file_bar.add_command(label="Exit", command=self._close)

        #Edit менюбар        
        edit_bar = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_bar)
        rotate_bar = Menu(edit_bar, tearoff=0)
        edit_bar.add_cascade(label="Rotate", menu=rotate_bar)
        rotate_bar.add_command(label="Rotate left 90", command=lambda: self.rotate_image(90))

        #Options menubar
        options_bar = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_bar)
        pick_color = Menu(options_bar, tearoff=0)
        options_bar.add_cascade(label="Pick color of...", menu=pick_color)
        pick_color.add_command(label="Pick color of polaroid background", command=lambda: self.pick_color_of("polaroid_bg_color"))
        pick_color.add_command(label="Pick color of border", command=lambda: self.pick_color_of("border_color"))

        self.root.configure(menu=menu_bar)

    def drawWigets(self):
        top_frame = customtkinter.CTkFrame(self.root, width=600, height=600)
        top_frame.pack(expand=True)
        bottom_frame = customtkinter.CTkFrame(self.root)
        bottom_frame.pack()
        self.img_tabs = Notebook(top_frame)
        self.img_tabs.enable_traversal()
        self.img_tabs.pack(fill="none", expand=1, anchor="center")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=0, text="Standard").grid(row=0, column=0, padx=2, pady=2)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=1, text="Mini").grid(row=0, column=1)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=2, text="Square").grid(row=0, column=2)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=3, text="Max").grid(row=0, column=3)
        self.border_var = customtkinter.StringVar(value="off")
        self.frame_var = customtkinter.StringVar(value="off")
        customtkinter.CTkCheckBox(bottom_frame, text="4mm border", onvalue="on", offvalue="off", variable=self.border_var).grid(row=0, column=4)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=4, text="Standard H").grid(row=1, column=0)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=5, text="Mini instax").grid(row=1, column=1)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=6, text="10 x 15").grid(row=1, column=2)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=7, text="Photo garland").grid(row=1, column=3)
        customtkinter.CTkRadioButton(bottom_frame, variable=self.radio_choice, value=8, text="A4").grid(row=1, column=4)
        customtkinter.CTkCheckBox(bottom_frame, text="No frame", onvalue="on", offvalue="off", variable=self.frame_var).grid(row=2, column=0)
        customtkinter.CTkButton(bottom_frame, text="Draw frame", command=self.draw_frame).grid(row=2, column=1, padx=2, pady=2)
        # customtkinter.CTkButton(bottom_frame, text="Crop image", command=self.crop_image).grid(row=1, column=2)
        customtkinter.CTkButton(bottom_frame, text="Create polaroid", command=self.create_polaroid).grid(row=2, column=3)
        # rotate_left_img = ImageTk.PhotoImage(Image.open(r".\resources\icons\rotate_left.png"))
        # rotate_right_img = ImageTk.PhotoImage(Image.open(r".\resources\icons\rotate_right.png"))
        # customtkinter.CTkButton(bottom_frame, text="Rotate left", image=rotate_left_img, compound="left", command=lambda: self.rotate_image(90)).grid(row=3, column=1, padx=2, pady=2)
        customtkinter.CTkButton(bottom_frame, text="Rotate left", compound="left", command=lambda: self.rotate_image(90)).grid(row=3, column=1, padx=2, pady=2)
        # customtkinter.CTkButton(bottom_frame, text="Rotate right", image=rotate_right_img, command=lambda: self.rotate_image(-90)).grid(row=3, column=3, padx=2, pady=2)
        customtkinter.CTkButton(bottom_frame, text="Rotate right", command=lambda: self.rotate_image(-90)).grid(row=3, column=3, padx=2, pady=2)        
        customtkinter.CTkButton(bottom_frame, text="Add space", command=self.add_space).grid(row=3, column=4)
    def get_format(self):
        if self.border_var.get() == "on":
            border = 4
            if self.radio_choice.get() == 0: #Standard polaroid 4mm border
                ratio = (75-border*2)/(100-border*2)
                format = "Standard bordered"
                return [ratio, format]
            elif self.radio_choice.get() == 1: #Mini 4mm border
                ratio = (55-border*2)/(90-border*2)
                format = "Mini bordered"
                return [ratio, format]
            elif self.radio_choice.get() == 2: #Square 4mm border
                ratio = 1
                format = "Square"
                return [ratio, format]
            elif self.radio_choice.get() == 3: #Max 4mm border
                ratio = (90-border*2)/(100-border*2)
                format = "Max bordered"
                return [ratio, format]            
            elif self.radio_choice.get() == 4: #Standard Horizontal 4mm border
                ratio = (100-border*2)/(75-border*2)
                format = "Standard H bordered"
                return [ratio, format]            
        elif self.frame_var.get == "on":
            border = 0
            if self.radio_choice.get() == 0: #Standard polaroid 4mm border
                ratio = (75-border*2)/(100-border*2)
                format = "Standard unbordered"
                return [ratio, format]
            elif self.radio_choice.get() == 1: #Mini 4mm border
                ratio = (55-border*2)/(90-border*2)
                format = "Mini unbordered"
                return [ratio, format]
            elif self.radio_choice.get() == 2: #Square 4mm border
                ratio = 1
                format = "Square unbordered"
                return [ratio, format]
            elif self.radio_choice.get() == 3: #Max 4mm border
                ratio = (90-border*2)/(100-border*2)
                format = "Max unbordered"
                return [ratio, format]            
            elif self.radio_choice.get() == 4: #Standard Horizontal 4mm border
                ratio = (100-border*2)/(75-border*2)
                format = "Standard H unbordered"
                return [ratio, format]
        else:
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
                ratio = 1
                format = "Max"
                return [ratio, format]            
            elif self.radio_choice.get() == 4: #Standard Horizontal
                ratio = 18/11
                format = "Standard H"
                return [ratio, format]
            elif self.radio_choice.get() == 5: #Mini instax
                ratio = 46/61
                format = "Mini instax"
                return [ratio, format]
            elif self.radio_choice.get() == 6: #10 x 15 horizontal
                ratio = 15/10
                format = "15 x 10"
                return [ratio, format]
            elif self.radio_choice.get() == 7: #Photo garland
                ratio = 65/73
                format = "Photo garland"
                return [ratio, format]
            elif self.radio_choice.get() == 8: #A4
                ratio = 297/210
                format = "A4"
                return [ratio, format]
        
    def draw_frame(self):
        image_info = self.current_image()
        if not image_info:
            return
        x0, y0, x1, y1 = self.frame_size(image_info.thumbnail)
        canvas = image_info.canvas
        canvas.delete(self.working_rectangle)
        self.working_rectangle = canvas.create_rectangle(x0, y0, x1 - 1, y1 - 1, dash=(10, 10), width=1, stipple="gray25", fill="#CCFFFF") # added -1 to draw inside canvas   
        canvas.focus_set()
        canvas.bind("<Left>", self.move_left)
        canvas.bind("<Right>", self.move_right)
        canvas.bind("<Up>", self.move_up)
        canvas.bind("<Down>", self.move_down)
    
    def move_left(self, event):
        image = self.current_image()
        coords = image.canvas.coords(self.working_rectangle)
        x0 = coords[0]
        moveDelta = -5
        if x0 + moveDelta >= 0:
            image.canvas.move(self.working_rectangle, moveDelta, 0)
        else:
            moveDelta = 0 - x0
            image.canvas.move(self.working_rectangle, moveDelta, 0)


    def move_right(self, event):
        image = self.current_image()
        coords = image.canvas.coords(self.working_rectangle)
        x1 = coords[2]
        moveDelta = 5
        if x1 + moveDelta <= image.thumbnail.width:
            image.canvas.move(self.working_rectangle, moveDelta, 0)
        else:
            moveDelta = image.thumbnail.width - x1
            image.canvas.move(self.working_rectangle, moveDelta, 0)

    def move_up(self, event):
        image = self.current_image()
        coords = image.canvas.coords(self.working_rectangle)
        y0 = coords[1]
        moveDelta = -5
        if y0 + moveDelta >= 0:
            image.canvas.move(self.working_rectangle, 0, moveDelta)
        else:
            moveDelta = 0 - y0
            image.canvas.move(self.working_rectangle, 0, moveDelta)

    def move_down(self, event):
        image = self.current_image()
        coords = image.canvas.coords(self.working_rectangle)
        y0 = coords[3]
        moveDelta = 5
        if y0 + moveDelta <= image.thumbnail.height:
            image.canvas.move(self.working_rectangle, 0, moveDelta)
        else:
            moveDelta = image.thumbnail.height - y0
            image.canvas.move(self.working_rectangle, 0, moveDelta)
        
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
        self.crop_image()
        image.resize_to_format(self.polaroid_bg_color, self.polaroid_border_color)
        self.update_image(image)
        self.img_tabs.focus_set()
        
    def current_image(self):
        current_tab = self.img_tabs.select()
        if not current_tab:
            return None
        tab_index = self.img_tabs.index(current_tab)        
        return self.opened_images[tab_index]
        
    def open_image(self):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpg *.png *.jpeg *.heic *.webp"), ))
        for image_path in image_paths:
            self.add_new_image(image_path)

    def close_image(self):
        image_info = self.current_image()
        tab_index = self.img_tabs.index(image_info.tab)
        image_info.image.close()
        del self.opened_images[tab_index]
        self.img_tabs.forget(image_info.tab)

    def close_images(self):
        for image_info in self.opened_images:
            image_info.image.close()
            self.img_tabs.forget(image_info.tab)
        self.opened_images.clear()
    
    def convert_icc(self):
        image_info = self.current_image()
        tab_index = self.img_tabs.index(image_info.tab)
        image_info.convert_icc(self.AdobeRGB)

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
        x0, y0, x1, y1 = image.canvas.coords(self.working_rectangle)
        print(f"x0: {x0}, y0: {y0}, x1: {x1}, y1: {y1}")
        image.crop(x0 + 1, y0 + 1, x1 - 1, y1 - 1) # x0 + 1, y0 + 1, x1 - 1, y1 - 1 reduces the frame on 1 px
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
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpg; *.png; *.jpeg *.heic"), ))
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
        self.save_sheets_as_pdf(formats)

    def save_sheets_as_pdf(self, formats):
        image = self.current_image()
        old_path = image.full_path(True)
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Portable Document Format", "*.pdf"), ))
        if not new_path:
            return
        new_path, new_ext = os.path.splitext(new_path)
        if not new_ext:
            new_ext = ".pdf"
        print(f"New path: {new_path}, New ext: {new_ext}")
        for format in formats:
            sheets_of_this_format = []
            for sheet in self.opened_sheets:
                if format == sheet.format:
                    sheets_of_this_format.append(sheet.sheet)
            sheets_of_this_format[0].save(f"{new_path} of {format}.pdf", save_all=True, append_images=sheets_of_this_format[1:], resolution=self.DPI)
        for sheet in self.opened_sheets:
            sheet.sheet.close()
            del sheet
        self.opened_sheets.clear()

    def add_space(self):
        image = self.current_image()
        format = self.get_format()
        ratio = format[0]
        image.add_space(ratio, self.polaroid_bg_color)
        self.update_image(image)

    def pick_color_of(self, instance):
        color_code = colorchooser.askcolor(title="Choose color")
        if instance == "polaroid_bg_color":
            self.polaroid_bg_color = color_code[0]
        elif instance == "border_color":
            self.polaroid_border_color = color_code[0]

if __name__ == "__main__":
    window = Editor (700, 700, (False, False))  
    window.run()
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from child_window import ChildWindow
from PIL import Image, ImageTk
import os

from image_info import ImageInfo


class Editor:
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
        self.frame_width = 0
        self.frame_height = 0
        self.working_canvas = None
        self.working_rectangle = None


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
        Button(bottom_frame, text="Draw frame", command=self.draw_frame).pack()
    
    def get_ratio(self):
        if self.radio_choice.get() == 0: #Standard polaroid
            ratio = 2/3
            return ratio
        elif self.radio_choice.get() == 1: #Mini
            ratio = 2/3
            return ratio
        elif self.radio_choice.get() == 2: #Square
            ratio = 1
            return ratio
        elif self.radio_choice.get() == 3: #Max
            ratio = 2/3
            return ratio
        elif self.radio_choice.get() == 4: #10x15
            ratio = 2/3
            return ratio
        
    # def start_crop_image(self):
    #     current_tab, image_path, image = self.get_current_working_data()
    #     if not current_tab:
    #         return
    #     tab_index = self.img_tabs.index(current_tab)
    #     current_frame = self.img_tabs.children[current_tab[current_tab.rfind("!"):]] #поиск дочернего виджета текущей Frame в Tabs
    #     canvas = current_frame.children["!canvas"] #поиск дочернего элемента Label в виджете frame
        

    def draw_frame(self):
        current_tab, image_path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_index = self.img_tabs.index(current_tab)
        current_frame = self.img_tabs.children[current_tab[current_tab.rfind("!"):]] #поиск дочернего виджета текущей Frame в Tabs
        canvas = current_frame.children["!canvas"] #поиск дочернего элемента Label в виджете frame

        x0, y0, x1, y1 = self.frame_size(image)

        self.working_canvas = canvas
        self.working_rectangle = canvas.create_rectangle(x0, y0, x1, y1, dash=(1, 5), fill='', width=2)
        self.working_canvas.bind("<Left>", self.move_left)
        self.working_canvas.bind("<Right>", self.move_right)
        self.working_canvas.bind("<Up>", self.move_up)
        self.working_canvas.bind("<Down>", self.move_down)
        print(self.working_canvas.children)
    
    def move_left(self, event):
        self.working_canvas.move(image)
        pass

    def move_right(self, event):
        pass

    def move_up(self, event):
        pass

    def move_down(self, event):
        pass
    #     self.working_canvas.move(image_panel)
        
     
    def frame_size(self, image):
        img_width, img_height = image.size
        ratio = self.get_ratio()
        if img_width/img_height < ratio:
            frame_width = img_width
            frame_height = img_width/ratio
        elif img_width/img_height >= ratio:
            frame_height = img_height
            frame_width = img_height * ratio
        x_start = img_width/2 - frame_width/2
        y_start = img_height/2 - frame_height/2
        x_end = img_width/2 + frame_width/2
        y_end = img_height/2 + frame_height/2
        return x_start, y_start, x_end, y_end


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
        image_tab = Frame(self.img_tabs)
        image_info = ImageInfo(image, image_path, image_tab)
        #image.thumbnail((600, 600))
        self.opened_images.append(image_info)

        image_tk = image_info.image_tk

        
        #img_width, img_height = image.size
        #image_panel = Canvas(self.img_tab, width=img_width, height=img_height)
        image_panel = Canvas(image_tab, width=image.width, height=image.height)
        image_panel.image = image_tk
        image_panel.create_image(0, 0, image=image_tk, anchor="nw")
        image_panel.pack(expand="yes")

        self.img_tabs.add(image_tab, text=f"{image_path.split("/")[-1]}")
        self.img_tabs.select(image_tab)

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
    window = Editor (800, 800)  
    window.run()
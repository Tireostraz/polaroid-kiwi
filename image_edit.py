from PIL import Image, ImageTk

class ImageEdit:
    def __init__(self, image):
        self.original_image = image
        self.image = image.copy()
        self.thumbnail = image.copy()
        self.thumbnail_size = (500, 500)
        self.thumbnail.thumbnail(self.thumbnail_size)
        self.image_tk = ImageTk.PhotoImage(self.thumbnail)
        self.canvas = None
        self.format = None
        self.DPI = 300  # pixels in inch
        self.DPM = self.DPI/25.4 # pixels in mm
        self.border_size = 1
        self.border_color = (235, 235, 235)
        # self.bg_color = (255, 255, 255)

        self.scale_factor = 500 / max(self.image.width, self.image.height)
    
    def set_format (self, format):
        self.format = format
    
    def resize_to_format(self, bg_color): # dimensions in mm -> pixels (5 mm * self.DPM) = pixels
        top = left = right = int(5 * self.DPM)
        if self.format == "Standard":
            bottom = int(17 * self.DPM)            
            image_width = int(65 * self.DPM)
            image_heigth = int(78 * self.DPM)
        elif self.format == "Mini":
            bottom = int(17.5 * self.DPM)
            image_width = int(45 * self.DPM)
            image_heigth = int(67.5 * self.DPM)
        elif self.format == "Max":
            bottom = int(16 * self.DPM)
            image_width = int(80 * self.DPM)
            image_heigth = int(84 * self.DPM)
        self.image = self.image.resize((image_width, image_heigth))
        self.add_padding(top, left, bottom, right, bg_color)
        self.add_border(self.border_size, self.border_color)
    
    def add_padding(self, top, left, bottom, right, bg_color):
        new_image = Image.new("RGB", (self.image.width + left + right, self.image.height + top + bottom), bg_color)
        new_image.paste(self.image, (left, top))
        self.image = new_image.copy()
        self.thumbnail = new_image.copy()
        self.thumbnail.thumbnail(self.thumbnail_size)

    def add_border(self, border_size, border_color):
        border = Image.new("RGB",  (self.image.width + border_size * 2, self.image.height + border_size * 2), border_color)
        border.paste(self.image, (border_size, border_size))
        self.image = border.copy()

    def image_tk(self):
        return ImageTk.PhotoImage(self.image)

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees, expand=True)
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail(self.thumbnail_size)

    def update_image_on_canvas(self):
        if self.canvas is None:
            raise RuntimeError("Canvas of image not given")
        
        self.image_tk = ImageTk.PhotoImage(self.thumbnail) 
        image_tk = self.image_tk
        self.canvas.delete("all")
        self.canvas.configure(width=self.thumbnail.width, height=self.thumbnail.height)        
        self.canvas.create_image(0, 0, image=image_tk, anchor="nw")
        self.canvas.image = image_tk
    
    def crop(self, x0, y0, x1, y1):
        original_image_rectangle = []
        thumbnail_rectangle = [x0, y0, x1, y1]
        for x in thumbnail_rectangle:
            original_image_rectangle.append(x/self.scale_factor)
        # print(original_image_rectangle)
        # print(thumbnail_rectangle)
        self.image = self.image.crop(original_image_rectangle)
        self.thumbnail = self.thumbnail.crop(thumbnail_rectangle)

from PIL import Image, ImageTk, ImageCms
from io import BytesIO

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
        # self.border_color = (215, 215, 215)
        # self.bg_color = (255, 255, 255)

        # self.scale_factor = 500 / max(self.image.width, self.image.height)
    
    def set_format (self, format):
        self.format = format
    
    def resize_to_format(self, bg_color, border_color): # dimensions in mm -> pixels (5 mm * self.DPM) = pixels
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
            bottom = int(15 * self.DPM) #16
            image_width = int(80 * self.DPM) #80
            image_heigth = int(80 * self.DPM) #84
        elif self.format == "Square":
            bottom = int(5 * self.DPM)
            image_width = int(80 * self.DPM)
            image_heigth = int(80 * self.DPM)
        elif self.format == "Standard H":
            bottom = int(15 * self.DPM)
            image_width = int(90 * self.DPM)
            image_heigth = int(55 * self.DPM)
        elif self.format == "Mini instax":
            top = int(7 * self.DPM)
            left = right = int(4 * self.DPM)
            bottom = int(17 * self.DPM)
            image_width = int(46 * self.DPM)
            image_heigth = int(62 * self.DPM)
        elif self.format == "15 x 10":
            top = bottom = left = right = 0
            image_width = int(150 * self.DPM)
            image_heigth = int(100 * self.DPM)

        #5mm border:
        if self.format == "Standard bordered":
            top = left = right = bottom = int(4 * self.DPM)
            image_width = int(75 * self.DPM) - (right+left)
            image_heigth = int(100 * self.DPM) - (top+bottom)
            self.format = "Standard"
        elif self.format == "Mini bordered":
            top = left = right = bottom = int(4 * self.DPM)
            image_width = int(55 * self.DPM) - (right+left)
            image_heigth = int(90 * self.DPM) - (top+bottom)
            self.format = "Mini"       
        elif self.format == "Max bordered":
            top = left = right = bottom = int(4 * self.DPM)
            image_width = int(90 * self.DPM) - (right+left)
            image_heigth = int(100 * self.DPM) - (top+bottom)
            self.format = "Max"
        elif self.format == "Standard H bordered":
            top = left = right = bottom = int(4 * self.DPM)
            image_width = int(100 * self.DPM) - (right+left)
            image_heigth = int(75 * self.DPM) - (top+bottom)
            self.format = "Standard H"
        self.image = self.image.resize((image_width, image_heigth))
        self.add_padding(top, left, bottom, right, bg_color)
        self.add_border(self.border_size, border_color)
    
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
    
    def convert_icc(self, icc):
        print(self.image.info)
        current_icc_bytes = self.image.info.get("icc_profile")
        if not current_icc_bytes:
            return            
        current_icc = ImageCms.getOpenProfile(BytesIO(current_icc_bytes)).profile
        if current_icc != icc:
            self.image = ImageCms.profileToProfile(self.image, current_icc, icc)
            print(self.image.info)
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
        scale_factor = 500 / max(self.image.width, self.image.height)
        for x in thumbnail_rectangle:
            original_image_rectangle.append(x/scale_factor)
        # print(original_image_rectangle)
        # print(thumbnail_rectangle)
        self.image = self.image.crop(original_image_rectangle)
        self.thumbnail = self.thumbnail.crop(thumbnail_rectangle)
    
    def add_space(self, ratio, bg_color):
        if self.image.width/self.image.height > ratio:
            newImageWidth = int(self.image.width)
            newImageHeight = int(self.image.width/ratio)
        elif self.image.width/self.image.height <= ratio:
            newImageWidth = int(self.image.height * ratio)
            newImageHeight = int(self.image.height)
        newImage = Image.new("RGB", (newImageWidth, newImageHeight), bg_color)
        newImage.paste(self.image, (int(newImageWidth/2-self.image.width/2), int(newImageHeight/2-self.image.height/2)))
        self.image = newImage.copy()
        print(f"image width:{self.image.width}, new image width: {newImageWidth}")
        print(f"image height:{self.image.height}, new image height: {newImageHeight}")
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail(self.thumbnail_size)
        


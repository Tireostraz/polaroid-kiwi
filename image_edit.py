from PIL import Image, ImageTk

class ImageEdit:
    def __init__(self, image):
        self.original_image = image
        self.image = image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas = None
        self.croped_image = None

    def image_tk(self):
        return ImageTk.PhotoImage(self.image)

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees)
        self.image_tk = ImageTk.PhotoImage(self.image)

    def update_image_on_canvas(self):
        if self.canvas is None:
            raise RuntimeError("Canvas of image not given")        
        
        image_tk = self.image_tk
        self.canvas.delete("all")
        self.canvas.configure(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, image=image_tk, anchor="nw")
        self.canvas.image = image_tk
    
    def crop(self, x0, y0, x1, y1):
        self.image = self.image.crop([x0, y0, x1, y1])
        self.image_tk = ImageTk.PhotoImage(self.image)
        # self.image = self.image.crop((250, 250, 750, 750))

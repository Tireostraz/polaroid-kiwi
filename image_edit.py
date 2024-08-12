from PIL import Image, ImageTk

class ImageEdit:
    def __init__(self, image):
        self.original_image = image
        self.image = image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas = None

    def image_tk(self):
        return ImageTk.PhotoImage(self.image)

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees)
        self.image_tk = ImageTk.PhotoImage(self.image)

    def update_image_on_canvas(self):
        if self.canvas == None:
            raise RuntimeError("Canvas of image not given")        
        
        image_tk = self.image_tk
        self.canvas.delete("all")
        self.canvas.configure(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, image=image_tk, anchor="nw")        
        self.canvas.image = image_tk
from PIL import Image, ImageTk

class ImageEdit:
    def __init__(self, image):
        self.original_image = image
        self.image = image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)

    def image_tk(self):
        return ImageTk.PhotoImage(self.image)

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees)
        self.image_tk = ImageTk.PhotoImage(self.image)
from image_edit import ImageEdit

class ImageInfo(ImageEdit):
    def __init__(self, image, path, tab):
        super().__init__(image)
        
        self.path = path
        self.tab = tab

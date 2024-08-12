from image_edit import ImageEdit
import os

class ImageInfo(ImageEdit):
    def __init__(self, image, path, tab):
        super().__init__(image)
        
        self.path = path
        self.tab = tab

    def unsaved(self): #Возвращает true если картинка изменена (добавилась "*") и не сохранена
        return self.path[-1] == "*"
    
    def image_name(self, no_star=False):
        name = os.path.split(self.path)[1]
        return name[:-1] if no_star and name[-1] == "*" else name
    
    def image_extantion(self, no_star=False):
        extantion = os.path.splitext(self.path)[1]
        return extantion[:-1] if no_star and extantion[-1] == "*" else extantion

    def directory(self, no_star=False):
        directory=os.path.split(self.path)[0]
        return directory[:-1] if no_star and directory[-1] == "*" else directory
    
    def full_path(self, no_star=False):
        return self.path[:-1] if no_star and self.path[-1] == "*" else self.path


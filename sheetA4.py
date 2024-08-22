from PIL import Image, ImageTk

class SheetA4:
    def __init__(self, format, DPI=200):
        self.DPI = DPI  # pixels in inch
        self.DPM = self.DPI/25.4 # pixels in mm
        self.format = format
        self.sheet = Image.new("RGB", (int(297 * self.DPM), int(210 * self.DPM)), (255, 255, 255))
        sheet_thumbnail = self.sheet.copy()
        self.MAX_SIZE = (500, 500)
        sheet_thumbnail.thumbnail(self.MAX_SIZE)
        sheet_thumbnail = ImageTk.PhotoImage(sheet_thumbnail)

        self.occupied = False
        self.left_padding = 5 * self.DPM
        self.top_padding = 5 * self.DPM
        self.width_occupied = self.left_padding
        self.height_occupied = self.top_padding

    def add_image_on_sheet(self, image, format):
        if format == "Max":
            self.top_padding = 2
            self.height_occupied = self.top_padding     
        print("Paste pos: ")
        print(int(self.width_occupied), int(self.height_occupied))
        self.sheet.paste(image, (int(self.width_occupied), int(self.height_occupied)))
        self.width_occupied += image.width
        # self.height_occupied += image.height
        width_left = self.sheet.width - self.width_occupied
        height_left = self.sheet.height - self.height_occupied #- image.height   
        if width_left < image.width + 10 * self.DPM and height_left < image.height + 5 * self.DPM:
            self.occupied = True
            return
        elif width_left < image.width + 10 * self.DPM:
            self.height_occupied += image.height
            self.width_occupied = self.left_padding
        



    


from PIL import Image, ImageTk

class SheetA4:
    def __init__(self, DPI=200):
        self.DPI = DPI  # pixels in inch
        self.DPM = self.DPI/25,4 # pixels in mm
        self.sheets = []
        self.left_padding = 10 * self.DPM
        self.top_padding = 10 * self.DPM
        self.width_occupied = self.left_padding
        self.height_occupied = self.top_padding
        self.MAX_SIZE = (500, 500)

    def concat_image(self, image, format):
        width_left = sheet.a4.width - self.width_occupied
        height_left = sheet.a4.height - self.height_occupied
        if self.sheets == [] or width_left < image.width + 10 * self.DPM and height_left < image.height + 10 * self.DPM:
            sheet = self.create_sheet(format)
            sheet = sheet[0]
            self.width_occupied = self.left_padding
            self.height_occupied = self.top_padding

        if width_left < image.width + 10 * self.DPM:
            self.height_occupied += image.height
            self.width_occupied = self.left_padding
                   
        sheet.a4.paste(image, (self.width_occupied, self.height_occupied))
        self.width_occupied += image.width
        self.update_sheet(sheet, format)
            
    def create_sheet(self, format):        
        sheet = Image.new("RGB", (297 * self.DPM, 210 * self.DPM), (255, 255, 255)) # a4 sheet with white background
        sheet_thumbnail = sheet.copy()
        sheet_thumbnail.thumbnail(self.MAX_SIZE)
        sheet_thumbnail = ImageTk.PhotoImage(sheet_thumbnail)
        self.sheets.append([sheet, sheet_thumbnail, format])
        return [sheet, sheet_thumbnail, format]
    
    def update_sheet(self, sheet, format):
        self.sheets.pop(-1)
        sheet_thumbnail = sheet.copy()
        sheet_thumbnail.thumbnail(self.MAX_SIZE)
        sheet_thumbnail = ImageTk.PhotoImage(sheet_thumbnail)
        self.sheets.append([sheet, sheet_thumbnail, format])
        return [sheet, sheet_thumbnail, format]




    


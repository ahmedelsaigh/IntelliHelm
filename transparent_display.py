from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1309
import time
from PIL import ImageFont, Image, ImageDraw

class Transparent_Display:
    def __init__(self):
        serial = spi(port=0, address=0x3C)
        self.device = ssd1309(serial)
        self.output = Image.new("1", (128,64))
        self.image = ImageDraw.Draw(self.output)

    def write_street_name(self, string):
        street_name_start = (0,0)
        street_name_zone = [street_name_start, (127,10)]
        self.image.rectangle(street_name_zone, outline="black", fill="black")
        self.image.text(street_name_start, str(string), fill="white")
        self.device.display(self.output)

    def clear_street_name(self):
        street_name_start = (0,0)
        street_name_zone = [street_name_start, (127,10)]
        self.image.rectangle(street_name_zone, outline="black", fill="black")
        self.device.display(self.output)

    def write_distance(self, string):
        distance_start = (0,11)
        distance_zone = [distance_start, (127,21)]
        self.image.rectangle(distance_zone, outline="black", fill="black")
        self.image.text(distance_start, str(string), fill="white")
        self.device.display(self.output)

    def clear_distance(self):
        distance_start = (0,11)
        distance_zone = [distance_start, (127,21)]
        self.image.rectangle(distance_zone, outline="black", fill="black")
        self.device.display(self.output)


    def write_direction(self, string):
        direction_start = (0,22)
        direction_zone = [direction_start, (127,32)]
        self.image.rectangle(direction_zone, outline="black", fill="black")
        self.image.text(direction_start, str(string), fill="white")
        self.device.display(self.output)

    def clear_direction(self):
        direction_start = (0,22)
        direction_zone = [direction_start, (127,32)]
        self.image.rectangle(direction_zone, outline="black", fill="black")
        self.device.display(self.output)

    def write_incoming(self, string):
        incoming_start = (0,42)
        incoming_zone = [incoming_start, (127,52)]
        self.image.rectangle(incoming_zone, outline="black", fill="black")
        self.image.text(incoming_start, str(string), fill="white")
        self.device.display(self.output)

    def clear_incoming(self):
        incoming_start = (0,42)
        incoming_zone = [incoming_start, (127,52)]
        self.image.rectangle(incoming_zone, outline="black", fill="black")
        self.device.display(self.output)

    def write_name(self, string):
        name_start = (0,53)
        name_zone = [name_start, (127,63)]
        self.image.rectangle(name_zone, outline="black", fill="black")
        self.image.text(name_start, str(string), fill="white")
        self.device.display(self.output)
        
    def clear_name(self):
        name_start = (0,53)
        name_zone = [name_start, (127,63)]
        self.image.rectangle(name_zone, outline="black", fill="black")
        self.device.display(self.output)

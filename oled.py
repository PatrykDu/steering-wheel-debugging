from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=64, height=48, rotate=0)

device.clear()

image = Image.new("1", (64, 48), 0)
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 63, 47), outline=255)
draw.text((4, 4), "HELLO", fill=255)
draw.text((4, 20), "OLED OK", fill=255)

device.display(image)
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=64, height=48)

image = Image.new("1", (64, 48))
draw = ImageDraw.Draw(image)

draw.text((0, 0), "Hello")
draw.text((0, 16), "Patryk")
draw.text((0, 32), "RPi 5 OK")

device.display(image)
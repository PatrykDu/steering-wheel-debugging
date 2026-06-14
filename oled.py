import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(64, 48, i2c, addr=0x3C)

oled.fill(0)
oled.show()

image = Image.new("1", (64, 48))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 63, 47), outline=255)
draw.text((2, 2), "HELLO", fill=255)
draw.text((2, 18), "SSD1306", fill=255)
draw.text((2, 34), "OK", fill=255)

oled.image(image)
oled.show()
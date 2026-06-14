import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(64, 48, i2c)

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    52
)

def display(n):
    image = Image.new("1", (64, 48))
    draw = ImageDraw.Draw(image)

    text = str(n)
    bbox = draw.textbbox((0, 0), text, font=font)

    x = (64 - (bbox[2] - bbox[0])) // 2
    y = (48 - (bbox[3] - bbox[1])) // 2

    draw.text((x, y), text, font=font, fill=255)

    oled.image(image)
    oled.show()


display(8)
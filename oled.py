import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(64, 48, i2c)

def display(n):
    text = str(n)

    for size in range(200, 5, -1):
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            size
        )

        image = Image.new("1", (64, 48))
        draw = ImageDraw.Draw(image)

        bbox = draw.textbbox((0, 0), text, font=font)

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w <= 64 and h <= 48:
            break

    image = Image.new("1", (64, 48))
    draw = ImageDraw.Draw(image)

    x = (64 - w) // 2 - bbox[0]
    y = (48 - h) // 2 - bbox[1]

    draw.text((x, y), text, font=font, fill=255)

    oled.image(image)
    oled.show()


display(8)
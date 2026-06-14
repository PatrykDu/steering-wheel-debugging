import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 64
HEIGHT = 48

VISIBLE_Y = 10
VISIBLE_H = HEIGHT - VISIBLE_Y

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

def display(value):
    text = str(value)

    for size in range(200, 5, -1):
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            size
        )

        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w <= WIDTH and h <= VISIBLE_H:
            break

    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    x = (WIDTH - w) // 2 - bbox[0]
    y = VISIBLE_Y + (VISIBLE_H - h) // 2 - bbox[1]

    draw.text((x, y), text, font=font, fill=255)

    oled.image(image)
    oled.show()


display("8")
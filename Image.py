# SPDX-FileCopyrightText: Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

# Imports the necessary libraries...
import socket
import fcntl
import struct
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import binance


def price(symbol):
    # Create blank image for drawing.
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    price_text = binance.get_usd_price(symbol)
    price_text = str(int(float(price_text)))
    # draw price
    text_width = font.getsize(price_text)
    width = int((128 - text_width[0]) / 2)
    draw.text((width, 30), price_text, font=font, fill=255)

    # draw symbol

    text_width = font2.getsize(symbol)
    width = int((128 - text_width[0]) / 2)
    draw.text((width, 0), symbol, font=font2, fill=255)
    return image

def main():
    pass


if __name__ == '__main__':
    main()

from PIL import Image, ImageDraw, ImageFont
import binance

def price(symbol):
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


def position(number, symbol):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    position_text = str(number) + " / " + str(5)
    # draw position
    text_width = font.getsize(position_text)
    width = int((128 - text_width[0]) / 2)
    draw.text((width, 0), position_text, font=font, fill=255)

    # draw symbol

    text_width = font2.getsize(symbol)
    width = int((128 - text_width[0]) / 2)
    draw.text((width, 30), symbol, font=font2, fill=255)
    return image


def main():
    pass


if __name__ == '__main__':
    main()

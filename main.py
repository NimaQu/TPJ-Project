import Image
import binance
import screen
from time import sleep


def main():
    try:
        while True:
            sleep(1)
            image = Image.price("BTC")
            screen.display(image)
    except KeyboardInterrupt:
        screen.reset()
        print('\nExiting...')


if __name__ == '__main__':
    main()

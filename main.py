from time import sleep
import binance


def main():
    try:
        while True:
            print(binance.get_usd_price('BTC'))
            sleep(1)
    except KeyboardInterrupt:
        print('\nExiting...')


if __name__ == "__main__":
    main()

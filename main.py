import Image
import binance
import screen
import threading
import logging
import var
from time import sleep
from configparser import ConfigParser
from waitress import serve

cf = ConfigParser()
cf.read('config.ini', encoding='utf-8')
logging.basicConfig(level=logging.INFO)


def start_web():
    import webapi
    port = cf.getint('web', 'flask_port')
    host = cf.get('web', 'flask_host')
    webapi.app.secret_key = cf.get('web', 'flask_secret_key')
    webapi.cf = cf
    if cf.getboolean('web', 'development'):
        webapi.app.env = 'development '
        webapi.app.run(host=host, port=port)
    else:
        serve(webapi.app, host=host, port=port)


def start_monitor():
    while True:
        symbol = cf.get('config', 'symbol' + str(var.symbol_index))
        sleep(1)
        image = Image.price(symbol)
        screen.display(image)


def main():
    # start web
    tt = threading.Thread(
        target=start_web, name="WebThread")
    tt.daemon = True
    logging.info('Starting webapi ....')
    tt.start()

    try:
        start_monitor()
    except KeyboardInterrupt:
        screen.reset()
        print('\nExited')


if __name__ == '__main__':
    main()

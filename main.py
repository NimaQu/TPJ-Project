import Image
import binance
import screen
import threading
import logging
import var
import sound
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


def display_price():
    while True:
        sleep(1)
        symbol = cf.get('config', 'symbol' + str(var.symbol_index))
        image = Image.price(symbol)
        screen.display(image)


def monitor_fluctuations():
    while True:
        sleep(5)
        symbol = cf.get('config', 'symbol' + str(var.symbol_index))
        price_before = float(binance.get_usd_price_before(symbol, var.monitor_time))
        price_now = float(binance.get_usd_price(symbol))
        fluctuation = abs(price_now - price_before) / price_before * 100
        print(fluctuation)
        print(abs(price_now - price_before))
        if fluctuation > cf.getfloat('monitor', 'fluctuation_threshold_percent') or abs(price_now - price_before) > cf.getfloat('monitor', 'fluctuation_threshold'):
            sound.play()
            sleep(cf.getint('monitor', 'alert_interval'))


def main():
    # start web
    webt = threading.Thread(
        target=start_web, name="WebThread", daemon=True)
    logging.info('Starting webapi ....')
    fluctuationt = threading.Thread(target=monitor_fluctuations, name="FluctuationThread", daemon=True)
    try:
        webt.start()
        logging.info('Webapi started')
        fluctuationt.start()
        logging.info('Fluctuation thread started')
        display_price()
    except KeyboardInterrupt:
        screen.reset()
        print('\nExited')


if __name__ == '__main__':
    main()

import Image
import binance
import screen
import threading
import logging
import sound
import Global
from time import sleep
from configparser import ConfigParser
from waitress import serve
from encoder import Encoder
import RPi.GPIO as GPIO

cf = ConfigParser()
cf.read('config.ini', encoding='utf-8')
logging.basicConfig(level=logging.INFO)
Global.init(cf)
tt_lock = threading.Lock()
Global.var['pause'] = False


def valueChanged(value, direction):
    Global.var['pause'] = True
    symbol_index = int(Global.var['symbol_index'])
    if direction == 'L':
        if symbol_index > 0:
            Global.var['symbol_index'] = symbol_index = symbol_index - 1
    elif direction == 'R':
        if symbol_index < 4:
            Global.var['symbol_index'] = symbol_index = symbol_index + 1
    else:
        return
    image = Image.position(symbol_index + 1, cf.get('config', 'symbol' + str(symbol_index)))
    screen.display(image)


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
        if Global.var['pause']:
            value_now = Global.var['symbol_index']
            sleep(1)
            if value_now != Global.var['symbol_index']:
                sleep(1)
                continue
            else:
                Global.var['pause'] = False
        symbol = cf.get('config', 'symbol' + str(Global.var['symbol_index']))
        image = Image.price(symbol)
        screen.display(image)
        sleep(1)


def monitor_fluctuations():
    while True:
        if Global.var['pause']:
            value_now = Global.var['symbol_index']
            sleep(1)
            if value_now != Global.var['symbol_index']:
                sleep(1)
                continue
            else:
                Global.var['pause'] = False

        symbol = cf.get('config', 'symbol' + str(Global.var['symbol_index']))
        try:
            price_before = float(binance.get_usd_price_before(symbol, Global.var['monitor_time']))
            price_now = float(binance.get_usd_price(symbol))
            fluctuation = abs(price_now - price_before) / price_before * 100
        except TypeError:
            continue
        if fluctuation > cf.getfloat('monitor', 'fluctuation_threshold_percent') or abs(price_now - price_before) > cf.getfloat('monitor', 'fluctuation_threshold'):
            sound.play()
            sleep(cf.getint('monitor', 'alert_interval'))
        sleep(5)


def main():
    GPIO.setmode(GPIO.BCM)
    # start web
    webt = threading.Thread(
        target=start_web, name="WebThread", daemon=True)
    logging.info('Starting webapi ....')
    fluctuationt = threading.Thread(target=monitor_fluctuations, name="FluctuationThread", daemon=True)
    e1 = Encoder(17, 18, valueChanged)
    try:
        webt.start()
        logging.info('Webapi started')
        fluctuationt.start()
        logging.info('Fluctuation thread started')
        display_price()
    except KeyboardInterrupt:
        screen.reset()
        GPIO.cleanup()
        Global.var.save()
        logging.info('Exiting')
        print('\nExited')


if __name__ == '__main__':
    main()

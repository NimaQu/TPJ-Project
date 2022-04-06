import requests
import time
import logging
baseurl = 'https://api.binance.com'


def get_usd_price(symbol):
    url = baseurl + '/api/v3/ticker/price'
    params = {'symbol': symbol + 'USDT'}
    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.ConnectionError:
        logging.error('ConnectionError')
        return None
    except requests.exceptions.Timeout:
        logging.error('Request Timeout')
        return None
    try:
        price = response.json()['price']
    except KeyError:
        return None
    try:
        round(float(price), 2)
    except ValueError:
        return None
    return price


def get_usd_price_before(symbol, _time):
    url = baseurl + '/api/v3/aggTrades'
    start_time = int((time.time() - float(_time)) * 1000)
    end_time = start_time + 10000
    params = {'symbol': symbol + 'USDT', 'startTime': start_time, 'endTime': end_time, 'limit': 1}
    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.ConnectionError:
        logging.error('Connection Error')
        return None
    except requests.exceptions.Timeout:
        logging.error('Request Timeout')
        return None
    try:
        price = response.json()[0]['p']
    except KeyError as e:
        logging.error(e)
        return None
    except IndexError as e:
        logging.error(e)
        return None
    try:
        round(float(price), 2)
    except ValueError as e:
        logging.error(e)
        return None
    return price


if __name__ == "__main__":
    print(get_usd_price('BTC'))
    print(get_usd_price_before('BTC', 300))

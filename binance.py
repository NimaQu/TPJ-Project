import requests

baseurl = 'https://api.binance.com'


def get_usd_price(symbol):
    url = baseurl + '/api/v3/ticker/price'
    params = {'symbol': symbol + 'USDT'}
    response = requests.get(url, params=params)
    price = response.json()['price']
    try:
        round(float(price), 2)
    except ValueError:
        return None
    return price


if __name__ == "__main__":
    pass
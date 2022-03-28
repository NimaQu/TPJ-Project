from flask import Flask, request, render_template
from configparser import ConfigParser
import Global
import Image
import screen
import binance

app = Flask(__name__)
cf = ConfigParser()


@app.route("/")
def root():
    return render_template("config.html")


@app.route("/setconfig", methods=["POST", "GET"])
def set_config():
    if request.method == "POST":
        for key in request.form:
            if binance.get_usd_price(request.form[key]) is None:
                return "Invalid currency: " + request.form[key]
            Global.var[key] = request.form[key]
    Global.var.save()
    return "OK"


@app.route("/setindex", methods=["POST"])
def set_index():
    try:
        int(request.form["currencies"])
    except ValueError:
        return "Invalid number of currencies"
    Global.var['symbol_index'] = symbol_index = request.form["currencies"]
    symbol_index = int(symbol_index)
    image = Image.position(symbol_index + 1, cf.get('config', 'symbol' + str(symbol_index)))
    screen.display(image)
    return "OK"


if __name__ == "__main__":
    app.secret_key = 'dsflkasjfsskk123211'
    app.env = 'debug '
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

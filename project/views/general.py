import adafruit_dht
import board
from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
import hashlib
import tempfile

mod = Blueprint('general', __name__)

dhtDevice = adafruit_dht.DHT11(board.D14)

@mod.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        global temperature_c
        global humidity
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
        except RuntimeError as error:
            print(error.args[0]) # A full buffer was not returned. Try again.
            temperature_c = -999
            humidity = -999

        return render_template('index.html', temp = temperature_c, humidity = humidity)

    elif request.method == 'POST':
        return render_template('index.html', post=False)

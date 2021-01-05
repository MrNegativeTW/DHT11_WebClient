# import adafruit_dht
# import board
from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
import pymysql.cursors

import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay

mod = Blueprint('general', __name__)

# dhtDevice = adafruit_dht.DHT11(board.D14)

# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

@mod.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        global result
        global temperature_c
        global humidity
        global dirtHum

        try:
            # Connect to the database
            connection = pymysql.connect(host='localhost',
                             user='dht22',
                             password='password',
                             db='dht22',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

            # Print latest record
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `history` ORDER BY `id` DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result[0])

            # Direct get value from sensor
            # temperature_c = dhtDevice.temperature
            # humidity = dhtDevice.humidity

            # Start SPI connection
            spi = spidev.SpiDev() # Created an object
            spi.open(0,0)
            dirtHum = analogInput(0) # Reading from CH0
            dirtHum = interp(dirtHum, [0, 1023], [100, 0])
            dirtHum = int(dirtHum)

        except RuntimeError as error:
            # Error handle for Database fetch error
            result = [{"dirtHum": -999, "hum": -999,"temp": -999,}]

            print(error.args[0]) # A full buffer was not returned. Try again.
            temperature_c = -999
            humidity = -999

        finally:
            connection.close()

        return render_template('index.html', result=result, dirtHum = dirtHum)
        

# import adafruit_dht
# import board
from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
import pymysql.cursors

mod = Blueprint('general', __name__)

# dhtDevice = adafruit_dht.DHT11(board.D14)

@mod.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        global result
        global temperature_c
        global humidity
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

        except RuntimeError as error:
            # Error handle for Database fetch error
            result = [{"dirtHum": -999, "hum": -999,"temp": -999,}]

            print(error.args[0]) # A full buffer was not returned. Try again.
            temperature_c = -999
            humidity = -999

        finally:
            connection.close()

        return render_template('index.html', result=result)

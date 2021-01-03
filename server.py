import board
import adafruit_dht
from flask import Flask, jsonify

app = Flask(__name__)
last_measurement_time = None

# Modify this GPIO pin to match your device's pin.
dhtDevice = adafruit_dht.DHT11(board.D14)

@app.route('/api/v1/temp+hum', methods=['GET'])
def get_temperature_and_humidity():
    global temperature_c
    global humidity
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return jsonify({
            'temperature': temperature_c, 
            'humidity': humidity
        })
 
    except RuntimeError as error:
        return jsonify({
            'temperature': 0, 
            'humidity': 0
        })

if __name__ == '__main__':
    # Modify host address and port. 
    app.run(host='192.168.1.138', port=5001)
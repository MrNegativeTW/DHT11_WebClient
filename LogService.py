import asyncio
import board
import adafruit_dht
import pymysql.cursors

dhtDevice = adafruit_dht.DHT11(board.D14)

async def getValueThenStoreToDatabase():
    global temperature_c
    global humidity

    while True:
        # Get sensor value
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
        except RuntimeError as error:
            print(error.args[0]) # A full buffer was not returned. Try again.
            temperature_c = -999
            humidity = -999

        try:
            # Connect to the database
            connection = pymysql.connect(host='localhost',
                             user='dht22',
                             password='password',
                             db='dht22',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

            # Write into database
            with connection.cursor() as cursor:
                sql = "INSERT INTO `history` ( `temp`, `hum`, `dirtHum`) VALUES ( %s, %s, %s)"
                cursor.execute(sql, (temperature_c, humidity, -999))
                connection.commit()

            # Print latest record
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `history` ORDER BY `id` DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result[0])
        finally:
            connection.close()

        await asyncio.sleep(1800) # 30 Minutes
        # await asyncio.sleep(5) # 10 Second, for debug

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(getValueThenStoreToDatabase())
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
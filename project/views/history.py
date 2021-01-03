from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
import hashlib
import tempfile
import pymysql.cursors

mod = Blueprint('history', __name__)

@mod.route('/history', methods=['GET'])
def index():
    if request.method == 'GET':
        global result
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='dht22',
                                     password='password',
                                     db='dht22',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `history`"
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return render_template('history.html', title='歷史紀錄', result=result)
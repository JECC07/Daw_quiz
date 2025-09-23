from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

def obtenerconexion():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    port=3339,
                                    user='root',
                                    password='',
                                    database='dawa_bd',
                                    cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        return None
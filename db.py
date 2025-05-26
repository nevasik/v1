import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="var1",
        cursorclass=pymysql.cursors.Cursor
    )

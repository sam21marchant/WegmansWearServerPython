import mysql.connector
import json
import os


def put_checked(entry_id, checked):
    DB_HOST="35.245.85.231"
    DB_USER="Database-Admin"
    DB_USER_READ="Database-Admin-Read"
    DB_PW="admin9125"
    DB_UNIX_SOCKET="/cloudsql/wegman-watch:us-east4:database"

    use_unix = 'USE_UNIX_SOCKET' in os.environ

    kwargs = {
        "user": DB_USER,
        "passwd":  DB_PW
    }
    if use_unix:
        kwargs["unix_socket"]=DB_UNIX_SOCKET
    else:
        kwargs["host"]=DB_HOST


    db = mysql.connector.connect(**kwargs)
    db_cursor = db.cursor(prepared=True)
    db_cursor.execute("UPDATE wegamns_watch.product p SET p.checked = %s WHERE p.entry_id = %s", (checked, entry_id))
    db.commit()
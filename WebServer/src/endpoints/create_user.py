import mysql.connector
import json
import os


def insertUser(google_id, name):
    ret_payload = []
    ret_code = 200

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
    db_cursor.execute("SELECT user_id FROM wegamns_watch.user WHERE google_id = %s LIMIT 1;", google_id)
    res = cur.fetchone()
    rc = cur.rowcount
    if rc == 0:
        db_cursor.execute("INSERT INTO wegamns_watch.user (name, google_id)VALUES(%s,%s) LIMIT 1;", (name, google_id))
        user_id = db.insert_id()
    else:
        user_id = res[0]

    
    return user_id, ret_code
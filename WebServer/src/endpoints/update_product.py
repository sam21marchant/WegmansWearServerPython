import mysql.connector
import json
import os


def put_checked(user_id, list_id, sku, checked):
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
    db_cursor.execute("UPDATE wegamns_watch.product p INNER JOIN wegamns_watch.list l ON p.list_id = l.list_id AND p.list_id = %s INNER JOIN wegamns_watch.user u ON u.user_id = l.user_id AND l.user_id = %s SET p.checked = %s WHERE sku = %s", (list_id, user_id, checked, sku))
    db.commit()
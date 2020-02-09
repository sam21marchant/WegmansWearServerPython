import mysql.connector
import json
import os


def getLists(user_id):
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
    db_cursor.execute("SELECT * FROM wegamns_watch.list WHERE user_id = %s;", user_id)
    myresult = db_cursor.fetchall()
    field_names = [i[0] for i in db_cursor.description]
    for res in myresult:
        print(res)
        x={}
        for i in range(len(db_cursor.description)):
            try:
                val = res[i].decode()
            except (AttributeError):
                val = res[i]
            x[db_cursor.description[i][0]] = val
        ret_payload.append(x)
    print(ret_payload)
    return json.dumps(ret_payload), ret_code
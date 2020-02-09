import mysql.connector
import json
import os

def getListDetails(list_id):
    ret_payload = {}
    ret_payload['data'] = []
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
    db_cursor.execute("SELECT p.list_id, l.name, p.entry_id, sku, p.name, p.description, qty, location, checked  FROM wegamns_watch.product p INNER JOIN wegamns_watch.list l ON p.list_id = l.list_id WHERE p.list_id = %s;", list_id)
    myresult = db_cursor.fetchall()
    field_names = [i[0] for i in db_cursor.description]
    for res in myresult:
        x={}
        ret_payload['id'] = res[0]
        ret_payload['name'] = res[1].decode()
        for i in range(2,len(field_names)):
            try:
                val = res[i].decode()
            except (AttributeError):
                if i == len(field_names)-1:
                    val = res[i] == 1
                else:
                    val = res[i]
            x[db_cursor.description[i][0]] = val
        ret_payload['data'].append(x)
    return json.dumps(ret_payload), ret_code
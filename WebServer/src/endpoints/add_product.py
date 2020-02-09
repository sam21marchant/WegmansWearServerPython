import mysql.connector
import json
import os


def add_produce(list_id, skus, names):
    ret_payload = []
    ret_code = 200
    for sku, name in zip(skus, names):

        url = "https://api.wegmans.io/products/"+ str(sku) +"/locations/13"

        headers = {
            "Cache-Control":"no-cache"
        }

        params = urllib.parse.urlencode({
            'subscription-key': 'bafe992034b244e688209673ebd2876b',
            "api-version":"2018-10-18"
        })
        try:
            r = requests.get(url, headers=headers, params=params)
            json_dump = r.json()
            loc = json_dump['locations'][0]['name']
        except Exception as e:
            print(e)

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
        db_cursor.execute("INSERT INTO wegamns_watch.product (sku, list_id, name, location, checked) VALUES(%s,%s,%s,%s,False);", (sku, list_id, name, loc))
        
    
    return "", ret_code
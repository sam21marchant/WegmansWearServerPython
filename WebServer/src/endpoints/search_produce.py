import mysql.connector
import json
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests


def search_produce(search_string):
    ret_payload = []
    ret_code = 200

    url = "https://api.wegmans.io/products/search"

    headers = {
        "Cache-Control":"no-cache"
    }

    params = urllib.parse.urlencode({
        'subscription-key': 'bafe992034b244e688209673ebd2876b',
        "query":"kabob",
        "api-version":"2018-10-18"
    })
    try:
        r = requests.get(url, headers=headers, params=params)
        json_dump = r.json()
        for j in json_dump['results']:
            x = {}
            x["sku"] = j["sku"]
            x["name"] = j["name"]
            ret_payload.append(x) 
    except Exception as e:
        print(e)

    return json.dumps(ret_payload), ret_code
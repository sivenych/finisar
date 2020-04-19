#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_list = [
    'https://xn--80aesfpebagmfblc0a.xn--p1ai/'
]

conn = psycopg2.connect(dbname='covid19', user='postgres',
                        password='postgres', host='localhost')
cursor = conn.cursor()

all_input = b''

for url in url_list:
    fp = None
    while fp is None:
        try:
            fp = urllib.request.urlopen(url, context=ctx)
        except:
            pass

    mybytes = fp.read()
    fp.close()
    all_input += mybytes

mystr = all_input.decode("utf8")

soup = BeautifulSoup(mystr, "html.parser")

div = soup.find('div', class_='d-map__list')
table = div.find('table')

for row in table.find_all('tr'):
    state = row.find('th').string
    data = []
    for column in row.find_all('td'):
        data.append(column.text)
    cursor.execute("INSERT INTO russia (date, ill, recovered, died, region) VALUES (current_date, %s, %s, %s, %s)",
                   (data[0], data[1], data[2], state))

conn.commit()
cursor.close()
conn.close()
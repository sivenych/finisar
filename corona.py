#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import postgresql

url_list = [
    'https://xn--80aesfpebagmfblc0a.xn--p1ai/'
]

connect_string = 'pq://postgres:postgres@localhost:5432/covid19'

all_input = b''

for url in url_list:
    fp = None
    while fp is None:
        try:
            fp = urllib.request.urlopen(url)
        except:
            pass

    mybytes = fp.read()
    fp.close()
    all_input += mybytes

mystr = all_input.decode("utf8")

soup = BeautifulSoup(mystr, "html.parser")

div = soup.find('div', class_='d-map__list')
table = div.find('table')

with postgresql.open(connect_string) as db:
    insert = db.prepare("INSERT INTO russia (date, ill, recovered, died, region) VALUES (current_date, $2, $3, $4, $1)")
    for row in table.find_all('tr'):
        state = row.find('th').string
        data = []
        for column in row.find_all('td'):
            data.append(column.text)
        insert(state, int(data[0]), int(data[1]), int(data[2]))
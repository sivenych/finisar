import urllib.request
from bs4 import BeautifulSoup

url_list = [
    'https://www.finisar.com/optical-transceivers?f%5B0%5D=field_protocol_general%3AEthernet',
    'https://www.finisar.com/optical-transceivers?f%5B0%5D=field_protocol_general%3AEthernet&page=1',
    'https://www.finisar.com/optical-transceivers?f%5B0%5D=field_protocol_general%3AEthernet&page=2'
]

all_input = b''

for url in url_list:
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    fp.close()
    all_input += mybytes

mystr = all_input.decode("utf8")

soup = BeautifulSoup(mystr, "html.parser")

total_items = 0

for article in soup.find_all('article'):
    title = article.find('div', {'class': 'field-title-field'})
    subtitle = article.find('div', {'class': 'field-subtitle'})
    ff = article.find('div', {'class': 'field-form-factor'})
    dist = article.find('div', {'class': 'field-reach'})
    max_speed = article.find('div', {'class': 'field-data-rate'})
    wl = article.find('div', {'class': 'field-components-wavelength'})
    proto = article.find_all('div', {'class': 'field-speeds'})
    protocols = []
    for p in proto:
        protocols.append(p.string)
    print(title.find('a').string+';;;', end='')
    print(ff.string+';', end='')
    print(dist.string+';', end='')
    print(max_speed.string+';;', end='')
    if wl != None:
        print(wl.string+';', end='')
    else:
        print("Unknown"+';', end='')
    print(', '.join(protocols)+';', end='')
    print(subtitle.find('a').string+';', end='')
    print('https://finisar.com/'+subtitle.find('a').get('href'), end='')
    total_items += 1
    print()

#print()
#print("Total items:")
#print(total_items)
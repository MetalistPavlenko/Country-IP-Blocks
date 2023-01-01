from math import log
from re import findall
from urllib.request import Request, urlopen

data = []

url = ['https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
       'https://ftp.ripe.net/ripe/stats/delegated-ripencc-latest',
       'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
       'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
       'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest']

for i in range(len(url)): data += urlopen(Request(url[i])).read().decode('utf-8')

blocks = {
    'ipv4':{
        'countries': {},
        'data': findall('\w+\|(\w+)\|ipv4\|(.+)\|(\d+)\|\d+', ''.join(data))
    },
    'ipv6':{
        'countries': {},
        'data': findall('\w+\|(\w+)\|ipv6\|(.+)\|(\d+)\|\d+', ''.join(data))
    },
}

for ip_type in blocks:
    for line in blocks[ip_type]['data']:
        if ip_type == 'ipv4':
            ip = line[1] + '/' + str(int(32-log(int(line[2]))/log(2)))
        else:
            ip = line[1] + '/' + str(line[2])

        if line[0] not in blocks[ip_type]['countries']:
            blocks[ip_type]['countries'][line[0]] = []

        blocks[ip_type]['countries'][line[0]].append(ip)

    for country in blocks[ip_type]['countries']:
        open(country + '_IPv' + ip_type[-1] + '.txt', 'w', encoding = 'utf-8').write(
            '\n'.join(blocks[ip_type]['countries'][country])
        )

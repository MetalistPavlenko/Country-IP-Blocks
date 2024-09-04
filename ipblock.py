import math, re, urllib.request

data = []

urls = ['https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
        'https://ftp.ripe.net/ripe/stats/delegated-ripencc-latest',
        'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
        'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
        'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest']

for url in urls: data += urllib.request.urlopen(urllib.request.Request(url, headers = {'User-Agent': 'curl/7.88.1'})).read().decode()

blocks = {
    'ipv4':{
        'countries': {},
        'data': re.findall('\w+\|(\w+)\|ipv4\|(.+)\|(\d+)\|\d+', ''.join(data))
    },
    'ipv6':{
        'countries': {},
        'data': re.findall('\w+\|(\w+)\|ipv6\|(.+)\|(\d+)\|\d+', ''.join(data))
    },
}

for sort in blocks:
    for line in blocks[sort]['data']:
        if sort == 'ipv4':
            ip = line[1]+'/'+str(int(32-math.log(int(line[2]))/math.log(2)))
        else:
            ip = line[1]+'/'+str(line[2])

        if line[0] not in blocks[sort]['countries']:
            blocks[sort]['countries'][line[0]] = []

        blocks[sort]['countries'][line[0]].append(ip)

    for country in blocks[sort]['countries']:
        open(country + '_IPv' + sort[-1] + '.txt', 'w', encoding = 'utf-8').write(
            '\n'.join(blocks[sort]['countries'][country])
        )

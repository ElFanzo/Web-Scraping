from bs4 import BeautifulSoup
from requests import get
from random import choice
import os
import time
import re


# main process
def getData():
    print('Parsing...Please, wait...')

    try:
        os.mkdir('Yahoo Finance Parsed Data')
    except FileExistsError:
        pass
    os.chdir('Yahoo Finance Parsed Data')
    file = open('stocks_info.csv', 'w')

    # List of your stocks. If necessary you can add new stock to this list.
    stocks = ['TSLA', 'DRIP', 'TVIX', 'RUN', 'RIOT', 'KNDI', 'MRO', 'GBTC', 'INGN', 'FAZ']

    # Parsing info for each stock
    for stock in stocks:
        time.sleep(2)
        getInfo(stock, file, proxy(), userAgent())
        getOptions(stock, proxy(), userAgent())

    print('%s\nDone! All output data is in folder "Yahoo Finance Parsed Data".\nCommon info is in the file called %s'
          '\nOptions for each stock are in the folder Options.\nIf the options do not exist for any stock, then perhaps'
          '\n   this info does not exist on the site.' % ('_' * 63, file.name))
    file.close()


# List of User Agents to prevent blocking due to scraping.
def userAgent():
    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90'
        ' Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
        ' Safari/537.36',
        # Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152;'
        ' .NET CLR 3.5.30729)'
    ]
    return choice(user_agent_list)


# List of Proxies to prevent blocking due to scraping. If necessary you can add new work proxy to this list.
def proxy():
    proxies = ['http://138.68.240.218:8080', 'http://138.68.24.145:8080', 'http://138.68.232.41:8080',
               'http://138.68.240.218:3128', 'http://138.68.24.145:3128', 'http://138.68.161.14:8080',
               'http://138.68.169.8:8080']
    return choice(proxies)


# Getting stock's base information.
def getInfo(stock, file, proxy, agent):
    req = get('https://finance.yahoo.com/quote/%s' % stock, proxies={'http': proxy}, headers={'User-Agent': agent})
    soup = BeautifulSoup(req.content, 'html5lib')

    table = soup.find('table', class_='W(100%)')
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    rows = [row.find_all('td')[1].text for row in rows]

    last_price = soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text

    change, perc_change = soup.find('div', class_='D(ib) Mend(20px)').find_all('span')[1].text.split()

    cur = soup.find('div', class_='C($c-fuji-grey-j) Fz(12px)')
    cur = cur.find('span').text[-3:]

    mark_time = soup.find('div', id='quote-market-notice')  #
    mark_time = mark_time.find('span').text
    mark_time = re.findall(r'\d+:\d+\w\w \w{3}', mark_time).pop()

    vol = rows[6].replace(',', '.')
    avg_vol = rows[7].replace(',', '.')
    day_range = rows[4]
    weeks_range = rows[5]

    mark_cup = soup.find('table', class_='W(100%) M(0) Bdcl(c)')
    if mark_cup.find('td').text == 'Market Cap':
        mark_cup = mark_cup.find('td', class_='Ta(end) Fw(b) Lh(14px)').text
    else:
        mark_cup = '-'

    file.write(stock + ',')
    file.write(','.join(i for i in [last_price, change, perc_change, cur, mark_time, vol, avg_vol, day_range,
                                    weeks_range, mark_cup]))
    file.write('\n')


# Getting stock's options information.
def getOptions(stock, proxy, agent):
    req = get('https://finance.yahoo.com/quote/{0}/options?p={0}'.format(stock), headers={'User-Agent': agent},
              proxies={'http': proxy})

    soup = BeautifulSoup(req.content, 'html5lib')

    try:
        section_calls = soup.find('section', attrs={'class': 'Mt(20px) qsp-2col-options'})
        section_puts = section_calls.next_sibling
        tbody_calls = section_calls.find('tbody')
        tbody_puts = section_puts.find('tbody')
        trows_calls = tbody_calls.find_all('tr')
        trows_puts = tbody_puts.find_all('tr')
    except AttributeError:
        return

    try:
        os.mkdir('Options')
    except FileExistsError:
        pass
    file = open('Options/stock_%s.csv' % stock, 'w')

    writeOptions('Calls', trows_calls, file)
    writeOptions('Puts', trows_puts, file)

    file.close()


# Writing options to file
def writeOptions(name, options, file):
    file.write('%s\n' % name)
    for row in options:
        cells = row.find_all('td')

        res = ','.join([cells[i].text for i in range(11)])

        file.write(res + '\n')


if __name__ == '__main__':
    getData()
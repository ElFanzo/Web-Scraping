import os
import re
import time
from bs4 import BeautifulSoup
from requests import get
from .bypass import getProxy, getUserAgent


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
        getInfo(stock, file, getProxy(), getUserAgent())
        getOptions(stock, getProxy(), getUserAgent())

    print('%s\nDone! All output data is in folder "Yahoo Finance Parsed Data".\nCommon info is in the file called %s'
          '\nOptions for each stock are in the folder Options.\nIf the options do not exist for any stock, then perhaps'
          '\n   this info does not exist on the site.' % ('_' * 63, file.name))
    file.close()


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
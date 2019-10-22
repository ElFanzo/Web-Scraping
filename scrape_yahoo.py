from grab import Grab
import os
import re


def parse():
    try:
        os.mkdir("Yahoo Finance Parsed Data")
    except FileExistsError:
        pass
    os.chdir("Yahoo Finance Parsed Data")
    file = open("stocks_info.csv", "w")

    # Here is stocks list
    stocks = [
        "TSLA",
        "DRIP",
        "TVIX",
        "RUN",
        "RIOT",
        "KNDI",
        "MRO",
        "GBTC",
        "INGN",
        "FAZ",
    ]
    for stock in stocks:
        get_stock_info(stock, file)
        get_options_info(stock)

    file.close()


def get_stock_info(stock, file):
    """
    Get stocks data
    :param stock: A stock's name
    :param file: An output filename
    :return:
    """
    g = Grab(transport="urllib3")
    g.go("https://finance.yahoo.com/quote/%s" % stock)

    last_price = g.doc.select(
        '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]'
    ).text()
    change, change_perc = (
        g.doc.select('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]')
        .text()
        .split()
    )
    curr = g.doc.select(
        '//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span'
    ).text()[-3:]
    mark_time = g.doc.select('//*[@id="quote-market-notice"]/span').text()
    mark_time = re.search(r"\d+:\d+\w\w \w{3}", mark_time, flags=re.ASCII).group(0)
    pat = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[%d]/td[2]'
    vol = g.doc.select(pat % 7).text().replace(",", ".")
    avg_vol = g.doc.select(pat % 8).text().replace(",", ".")
    day_r = g.doc.select(pat % 5).text()
    week_r = g.doc.select(pat % 6).text()
    mark_cap = g.doc.select(
        '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span'
    ).text()

    file.write(stock + ",")
    file.write(
        ",".join(
            i for i in [
                last_price,
                change,
                change_perc,
                curr,
                mark_time,
                vol,
                avg_vol,
                day_r,
                week_r,
                mark_cap,
                "\n",
            ]
        )
    )


def get_options_info(stock):
    """
    Get stock options data
    :param stock: A stock's name
    :return:
    """
    g = Grab(transport="urllib3")
    g.go("https://finance.yahoo.com/quote/{0}/options?p={0}".format(stock))

    try:
        os.mkdir("Options")
    except FileExistsError:
        pass
    file = open("Options/stock_%s.csv" % stock, "w")

    for i, j in zip([1, 2], ["Calls", "Puts"]):
        file.write("%s\n" % j)
        rows = g.doc.select(
            '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[%d]'
            "/div[2]/div/table/tbody/tr" % i
        )
        for row in rows:
            tds = [td.text() for td in row.select("td")]
            file.write(",".join(tds) + "\n")

    file.close()


if __name__ == "__main__":
    print("Data is been parsing...Please, wait...")

    parse()

    print(
        '%s\nDone! All the output data is in the folder "Yahoo Finance Parsed '
        'Data".\nCommon info is in the file called stocks_info.csv'
        "\nOptions for each stock are in the folder Options."
        "\nIf the options do not exist for any stock, then perhaps"
        "\n   this info does not exist on the site." % ("_" * 63)
    )

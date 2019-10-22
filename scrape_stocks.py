from bs4 import BeautifulSoup
from requests import get
from datetime import date, datetime


# Get stock's calls by the date from Yahoo
def get_data(stock, _date):
    date_string = ""
    try:
        date_string = (
            "&date=%d"
            % (
                datetime.strptime(_date, "%d%m%Y").date() - date(1970, 1, 1)
            ).total_seconds()
        )
        _date = "_" + str(_date)
    except ValueError:
        _date = ""
    req = get(
        "https://finance.yahoo.com/quote/{0}/options?p={0}{1}".format(
            stock, date_string
        )
    )

    soup = BeautifulSoup(req.content, "html5lib")
    section = soup.find("section", attrs={"class": "Mt(20px) qsp-2col-options"})

    try:
        tbody = section.find("tbody")
        trows = tbody.find_all("tr")
    except AttributeError:
        print("%s stock is invalid or data for this date have not been found"
              % stock)
        return

    file = open("stock_%s%s.csv" % (stock, _date), "w")

    for row in trows:
        cells = row.find_all("td")

        res = ",".join([cells[i].text for i in range(11)])

        file.write(res + "\n")

    print(
        "%s\nDone! Your file is ready. It is called %s\nThe data were taken "
        "from link below:\n%s" % ("_" * 62, file.name, req.url)
    )
    file.close()


if __name__ == "__main__":
    stock = input("Enter name of stock...").upper()
    _date = input('Enter date in the format "%dd%mm%YYYY" if necessary ...')
    get_data(stock, _date)

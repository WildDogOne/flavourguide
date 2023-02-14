from pprint import pprint
import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.smartblend.co.uk/flavour-guide'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    table = (soup.find_all("table", {"class": "mytable"}))
    headers = [header.text for header in table.find_all('th')]
    results = [{headers[i]: cell for i, cell in enumerate(row.find_all('td'))}
               for row in table.find_all('tr')]
    pprint(results)
if __name__ == '__main__':
    main()
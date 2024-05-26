from pylonparser.matches import BasketballMatch
from pylonparser.scraper import WebScraper
import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser
import pandas as pd

url = "https://www.basketball-reference.com/boxscores/202405240MIN.html"
scraper = WebScraper(url)
soup = scraper.get_page(url)

def basketball_table(soup):
    html = HTMLParser(str(soup))
    table = html.css_first("#box-DAL-game-basic").css("tbody tr")
    table_list = []
    for row in table:
        table_dict = {}
        header_cell = row.css("th")[0]
        if header_cell.text() not in ["", "Player", "Week", "Reserves"]:
            table_dict["id"] = header_cell.attributes["data-append-csv"].strip()
            table_dict[header_cell.attributes["data-stat"]] = header_cell.text()
            for stat in row.css("td"):
                value = stat.text()
                print(f"Stat: {stat.attributes['data-stat']}, Value: {value}")
                if value.replace(".", "").isdigit():
                    value = int(value) if value.isdigit() else float(value)
                table_dict[stat.attributes["data-stat"]] = value or 0
            table_list.append(table_dict)
    return table_list

df = pd.DataFrame(basketball_table(soup))
print(df)
import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = self.get_page(url)

    def get_page(self, url: str) -> BeautifulSoup:
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                if comment.startswith('\n\n<div class="table_container"'):
                    new_tag = BeautifulSoup(comment, "html.parser")
                    comment.replace_with(new_tag)
            return soup
        except requests.RequestException as e:
            logger.error(f"Error fetching page {url}: {e}")
            raise

    def parse_football_tr_table(self, table_id: str) -> list:
        html = HTMLParser(str(self.soup))
        table = html.css_first(f"#{table_id}").css("tbody tr")
        table_list = []
        for row in table:
            table_dict = {}
            header_cell = row.css("th")[0]
            if header_cell.text() not in ["", "Player", "Week"]:
                table_dict[header_cell.attributes["data-stat"]] = header_cell.text()
                try:
                    table_dict["id"] = header_cell.attributes["data-append-csv"].strip()
                except KeyError:
                    table_dict["id"] = row.css("td")[6].css("a")[0].attrs["href"].strip()
                for stat in row.css("td"):
                    value = stat.text()
                    if value.replace(".", "").isdigit():
                        value = int(value) if value.isdigit() else float(value)
                    table_dict[stat.attributes["data-stat"]] = value or 0
                table_list.append(table_dict)
        return table_list
    def find_basketball_table_ids(self):
        html = HTMLParser(str(self.soup))
        tables = html.css("table")
        table_ids = []
        for table in tables:
            table_id = table.attributes.get("id")
            if table_id:
                table_ids.append(table_id)
        return table_ids
    
    def basketball_table(self, table_id: str):
        html = HTMLParser(str(self.soup))
        table = html.css_first(f"#{table_id}").css("tbody tr")
        table_list = []
        for row in table:
            table_dict = {}
            header_cell = row.css("th")[0]
            if header_cell.text() not in ["", "Reserves"]:
                table_dict["id"] = header_cell.attributes["data-append-csv"].strip()
                table_dict[header_cell.attributes["data-stat"]] = header_cell.text()
                for stat in row.css("td"):
                    value = stat.text()
                    if value.replace(".", "").isdigit():
                        value = int(value) if value.isdigit() else float(value)
                    table_dict[stat.attributes["data-stat"]] = value or 0
                table_list.append(table_dict)
        return table_list

if __name__ == "__main__":
    game_url = "https://www.pro-football-reference.com/boxscores/202009100kan.htm"
    scraper = WebScraper(game_url)
    soup = scraper.get_page(game_url)

import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser
import logging
import re

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

    def parse_football_table(self, table_id: str) -> list:
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
                    table_dict["id"] = (
                        row.css("td")[6].css("a")[0].attrs["href"].strip()
                    )
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

    def parse_table_type(self, table_type: str) -> tuple:
        """
        Parses the table type string to determine the partial ID and occurrence.

        :param table_type: The type of the table (e.g., 'basic-home-stats', 'advanced-away-stats').
        :return: A tuple containing the partial ID and occurrence.
        :raises ValueError: If the table type is invalid.
        """
        if "basic" in table_type:
            partial_id = "basic"
        elif "advanced" in table_type:
            partial_id = "advanced"
        else:
            raise ValueError(f"Invalid table type: {table_type}")

        if "home" in table_type:
            occurrence = 2
        elif "away" in table_type:
            occurrence = 1
        else:
            raise ValueError(f"Invalid table type: {table_type}")

        return partial_id, occurrence

    def translate_table_id(
        self, html: HTMLParser, partial_id: str, occurrence: int
    ) -> str:
        """
        Translates a partial table ID to a full table ID based on its occurrence in the HTML content.

        :param html: The HTMLParser object containing the parsed HTML content.
        :param partial_id: The partial ID to match against.
        :param occurrence: The occurrence index (1 for first, 2 for second, etc.).
        :return: The full table ID.
        :raises ValueError: If the table ID matching the criteria is not found.
        """
        pattern = re.compile(rf"box-.*game-{partial_id}")
        matching_elements = [
            element
            for element in html.css("table[id]")
            if pattern.match(element.attributes["id"])
        ]

        if occurrence <= len(matching_elements):
            return matching_elements[occurrence - 1].attributes["id"]

        raise ValueError(
            f"Table ID matching '{partial_id}' with occurrence {occurrence} not found"
        )

    def parse_basketball_table(self, table_type: str):
        """
        Parses the HTML table based on the given table type and returns the data as a list of dictionaries.

        :param table_type: The type of the table (e.g., 'basic-home-stats', 'advanced-away-stats').
        :return: A list of dictionaries with the table data.
        """
        partial_id, occurrence = self.parse_table_type(table_type)
        html = HTMLParser(str(self.soup))
        table_id = self.translate_table_id(html, partial_id, occurrence)
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
    game_url = "https://www.basketball-reference.com/boxscores/202405220MIN.html"
    scraper = WebScraper(game_url)

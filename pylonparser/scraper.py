import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    A class for scraping and parsing HTML tables from a web page.

    Attributes:
        url (str): The URL of the web page to scrape.

    Methods:
        __init__(self, url: str): Initializes a new instance of the WebScraper class.
        get_page(self, url: str) -> BeautifulSoup: Fetches the web page content and returns it as a BeautifulSoup object.
        parse_football_table(self, table_id: str) -> list: Parses a football table from the web page and returns it as a list of dictionaries.
        find_basketball_table_ids(self): Finds the IDs of basketball tables in the web page and returns them as a list.
        parse_table_type(self, table_type: str) -> tuple: Parses the table type string to determine the partial ID and occurrence.
        translate_table_id(self, html: HTMLParser, partial_id: str, occurrence: int) -> str: Translates a partial table ID to a full table ID based on its occurrence in the HTML content.
        parse_basketball_table(self, table_type: str): Parses a basketball table from the web page and returns it as a list of dictionaries.
    """

    def __init__(self, url: str):
        self.url = url
        self.soup = self.get_page(url)

    def get_page(self, url: str) -> BeautifulSoup:
        """
        Fetches the web page content and returns it as a BeautifulSoup object.

        :param url: The URL of the web page.
        :return: A BeautifulSoup object representing the web page content.
        :raises requests.RequestException: If an error occurs while fetching the web page.
        """
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
        """
        Parses a football table from the HTML document.

        Args:
            table_id (str): The ID of the table to be parsed.

        Returns:
            list: A list of dictionaries representing the parsed table.
        """
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
        """
        Finds and returns the IDs of all basketball tables in the HTML document.

        Returns:
            list: A list of table IDs.
        """
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
        html = HTMLParser(str(self.soup))
        if table_type != "schedule":
            partial_id, occurrence = self.parse_table_type(table_type)
            table_id = self.translate_table_id(html, partial_id, occurrence)
        else:
            table_id = "schedule"
        table = html.css_first(f"#{table_id}").css("tbody tr")
        table_list = []

        for row in table:
            table_dict = {}
            header_cell = row.css("th")[0]
            if header_cell.text() not in ["", "Reserves"]:
                try:
                    table_dict["id"] = header_cell.attributes["data-append-csv"].strip()
                    table_dict[header_cell.attributes["data-stat"]] = header_cell.text()
                except KeyError:
                    pass
                for stat in row.css("td"):
                    value = stat.text()
                    if value.replace(".", "").isdigit():
                        value = int(value) if value.isdigit() else float(value)
                    table_dict[stat.attributes["data-stat"]] = value or 0
                table_list.append(table_dict)
        return table_list

    def parse_ice_hockey_table(self, table_type: str):
       html = HTMLParser(str(self.soup)) 


if __name__ == "__main__":
    game_url = "https://www.basketball-reference.com/boxscores/202405220MIN.html"
    scraper = WebScraper(game_url)
    print(scraper.parse_basketball_table("basic-home-stats"))

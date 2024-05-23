import os
import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser
import time

def get_page(url: str) -> BeautifulSoup:
    """
    Retrieves the content of a web page and returns it as a BeautifulSoup object.

    Args:
        url (str): The URL of the web page to retrieve.

    Returns:
        BeautifulSoup: The parsed HTML content of the web page.

    Raises:
        Exception: If the page is not found (status code is not 200).
    """
    page = requests.get(url)
    if page.status_code == 200:
        content = page.content
        soup = BeautifulSoup(content, "html.parser")
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if comment.startswith('\n\n<div class="table_container"'):
                new_tag = BeautifulSoup(comment, "html.parser")
                comment.replace_with(new_tag)
        return soup
    else:
        raise Exception(f"Page {url} not found")


def parse_tr_table(soup: BeautifulSoup, table_id_css: str) -> list:
    """
    Parses a table from BeautifulSoup object based on the provided table ID CSS selector.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the HTML.
        table_id_css (str): The CSS selector for the table ID. Available options are:
            - "player_offense"
            - "player_defense"
            - "returns"
            - "kicking"
            - "passing_advanced"
            - "rushing_advanced"
            - "receiving_advanced"
            - "defense_advanced"
            - "home_starters"
            - "vis_starters"
            - "home_snap_counts"
            - "vis_snap_counts"

    Returns:
        list: A list of dictionaries representing the parsed table data.
    """
    html = HTMLParser(str(soup))
    table = html.css_first(table_id_css).css("tbody tr")
    table_list = []
    for row in table:
        table_dict = {}

        if row.css("th")[0].text() not in ["", "Player", "Week"]:
            table_dict[row.css("th")[0].attributes["data-stat"]] = row.css("th")[
                0
            ].text()
            try:
                table_dict["id"] = row.css("th")[0].attributes["data-append-csv"].strip()
            except KeyError:
                table_dict["id"] = row.css("td")[6].css("a")[0].attrs["href"].strip()
                
            for stat in row.css("td"):
                table_dict[stat.attributes["data-stat"]] = stat.text()
                
            table_dict = {k: (v if v != '' else '0') for k, v in table_dict.items()}
            
            table_list.append(table_dict)
        
    return table_list

def get_game_stats(url: str, table: str) -> list:
    """
    Retrieves game statistics from a given URL and returns them as a list.

    Parameters:
    - url (str): The URL of the webpage containing the game statistics.
    - table (str): The ID or class name of the HTML table containing the statistics.

    Returns:
    - list: A list of game statistics extracted from the specified table.

    Example:
    >>> url = "https://example.com/game-stats"
    >>> table = "stats-table"
    >>> stats = get_game_stats(url, table)
    >>> print(stats)
    [10, 5, 3, 2, 1]
    """
    soup = get_page(url)
    table_list = parse_tr_table(soup, f"#{table}")
    return table_list
def get_game_stats(url:str, table: str) -> list:
    soup = get_page(url)
    table_list = parse_tr_table(soup, f"#{table}")
    return table_list
    
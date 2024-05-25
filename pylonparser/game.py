import requests
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser


class Game:
    def __init__(self, url: str):
        self.url = url
        self.soup = self.get_page(url)
        self.player_offense = self.parse_tr_table('player_offense')
        self.player_defense = self.parse_tr_table('player_defense')
        self.receiving_advanced = self.parse_tr_table('receiving_advanced')
        self.returns = self.parse_tr_table('returns')
        self.kicking = self.parse_tr_table('kicking')
        self.passing_advanced = self.parse_tr_table('passing_advanced')
        self.rushing_advanced = self.parse_tr_table('rushing_advanced')
        self.defense_advanced = self.parse_tr_table('defense_advanced')
        self.home_starters = self.parse_tr_table('home_starters')
        self.vis_starters = self.parse_tr_table('vis_starters')
        self.home_snap_counts = self.parse_tr_table('home_snap_counts')
        self.vis_snap_counts = self.parse_tr_table('vis_snap_counts')

    def get_page(self, url: str) -> BeautifulSoup:
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

    def parse_tr_table(self, table_id: str) -> list:
        html = HTMLParser(str(self.soup))
        table = html.css_first(f"#{table_id}").css("tbody tr")
        table_list = []
        for row in table:
            table_dict = {}
            if row.css("th")[0].text() not in ["", "Player", "Week"]:
                table_dict[row.css("th")[0].attributes["data-stat"]] = row.css("th")[0].text()
                try:
                    table_dict["id"] = row.css("th")[0].attributes["data-append-csv"].strip()
                except KeyError:
                    table_dict["id"] = row.css("td")[6].css("a")[0].attrs["href"].strip()
                for stat in row.css("td"):
                    if stat.text().replace(".", "").isdigit():
                        try:
                            value = int(stat.text())
                        except ValueError:
                            value = float(stat.text())
                    else:
                        value = stat.text()
                    table_dict[stat.attributes["data-stat"]] = value
                table_dict = {k: (v if v != "" else 0) for k, v in table_dict.items()}
                table_list.append(table_dict)
        return table_list


if __name__ == "__main__":
    url = "https://www.pro-football-reference.com/boxscores/202009100kan.htm"
    game = Game(url)

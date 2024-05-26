from .scraper import WebScraper


class Match(WebScraper):
    def __init__(self, url: str):
        super().__init__(url)


class FootballMatch(Match):
    """
    Represents a football match.

    Args:
        url (str): The URL of the football match.

    Attributes:
        player_offense (list): The parsed football table for player offense.
        player_defense (list): The parsed football table for player defense.
        receiving_advanced (list): The parsed football table for receiving advanced statistics.
        returns (list): The parsed football table for returns.
        kicking (list): The parsed football table for kicking.
        passing_advanced (list): The parsed football table for passing advanced statistics.
        rushing_advanced (list): The parsed football table for rushing advanced statistics.
        defense_advanced (list): The parsed football table for defense advanced statistics.
        home_starters (list): The parsed football table for home team starters.
        vis_starters (list): The parsed football table for visiting team starters.
        home_snap_counts (list): The parsed football table for home team snap counts.
        vis_snap_counts (list): The parsed football table for visiting team snap counts.
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.player_offense = self.parse_football_table("player_offense")
        self.player_defense = self.parse_football_table("player_defense")
        self.receiving_advanced = self.parse_football_table("receiving_advanced")
        self.returns = self.parse_football_table("returns")
        self.kicking = self.parse_football_table("kicking")
        self.passing_advanced = self.parse_football_table("passing_advanced")
        self.rushing_advanced = self.parse_football_table("rushing_advanced")
        self.defense_advanced = self.parse_football_table("defense_advanced")
        self.home_starters = self.parse_football_table("home_starters")
        self.vis_starters = self.parse_football_table("vis_starters")
        self.home_snap_counts = self.parse_football_table("home_snap_counts")
        self.vis_snap_counts = self.parse_football_table("vis_snap_counts")


class SoccerMatch(Match):
    def __init__(self, url: str):
        super().__init__(url)
        # Define attributes or methods specific to SoccerMatch if needed


class BasketballMatch(Match):
    """
    Represents a basketball match.

    Args:
        url (str): The URL of the basketball match.

    Attributes:
        basic_away (dict): The basic statistics of the away team.
        basic_home (dict): The basic statistics of the home team.
        advanced_away (dict): The advanced statistics of the away team.
        advanced_home (dict): The advanced statistics of the home team.
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.basic_away = self.parse_basketball_table("basic-away-stats")
        self.basic_home = self.parse_basketball_table("basic-home-stats")
        self.advanced_away = self.parse_basketball_table("advanced-away-stats")
        self.advanced_home = self.parse_basketball_table("advanced-home-stats")

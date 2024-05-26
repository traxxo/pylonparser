from .scraper import WebScraper

class Match(WebScraper):
    def __init__(self, url: str):
        super().__init__(url)

class FootballMatch(Match):
    def __init__(self, url: str):
        super().__init__(url)
        self.player_offense = self.parse_football_tr_table('player_offense')
        self.player_defense = self.parse_football_tr_table('player_defense')
        self.receiving_advanced = self.parse_football_tr_table('receiving_advanced')
        self.returns = self.parse_football_tr_table('returns')
        self.kicking = self.parse_football_tr_table('kicking')
        self.passing_advanced = self.parse_football_tr_table('passing_advanced')
        self.rushing_advanced = self.parse_football_tr_table('rushing_advanced')
        self.defense_advanced = self.parse_football_tr_table('defense_advanced')
        self.home_starters = self.parse_football_tr_table('home_starters')
        self.vis_starters = self.parse_football_tr_table('vis_starters')
        self.home_snap_counts = self.parse_football_tr_table('home_snap_counts')
        self.vis_snap_counts = self.parse_football_tr_table('vis_snap_counts')

class SoccerMatch(Match):
    def __init__(self, url: str):
        super().__init__(url)
        # Define attributes or methods specific to SoccerMatch if needed

class BasketballMatch(Match):
    def __init__(self, url: str):
        super().__init__(url)
        self.basic_stats = self.parse_basketball_tr_table('box-DAL-game-basic')
        # Define attributes or methods specific to BasketballMatch if needed
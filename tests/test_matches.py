import unittest
from pylonparser.matches import FootballMatch


class TestFootballMatch(unittest.TestCase):
    def setUp(self):
        self.match = FootballMatch("https://example.com/football-match")


if __name__ == "__main__":
    unittest.main()

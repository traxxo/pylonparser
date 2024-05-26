import unittest
from pylonparser.scraper import WebScraper
import requests


class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper("https://example.com")

    def test_get_page(self):
        # Test successful page retrieval
        soup = self.scraper.get_page("https://example.com")
        self.assertIsNotNone(soup)

        # Test invalid URL
        with self.assertRaises(requests.RequestException):
            self.scraper.get_page("https://invalidurl")

    def test_find_basketball_table_ids(self):
        # Test finding basketball table IDs
        table_ids = self.scraper.find_basketball_table_ids()
        self.assertIsInstance(table_ids, list)

    def test_parse_table_type(self):
        # Test parsing a valid table type
        partial_id, occurrence = self.scraper.parse_table_type("basic-home-stats")
        self.assertEqual(partial_id, "basic")
        self.assertEqual(occurrence, 2)

        # Test parsing an invalid table type
        with self.assertRaises(ValueError):
            self.scraper.parse_table_type("invalid-table-type")


if __name__ == "__main__":
    unittest.main()

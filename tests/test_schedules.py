import unittest
from pylonparser.schedules import BasketballSchedule


class TestBasketballSchedule(unittest.TestCase):
    def setUp(self):
        self.schedule_url = "https://example.com/schedule"
        self.schedule = BasketballSchedule(self.schedule_url)


if __name__ == "__main__":
    unittest.main()

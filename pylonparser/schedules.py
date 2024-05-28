from .scraper import WebScraper


class Schedule(WebScraper):
    def __init__(self, url: str):
        super().__init__(url)


class FootballSchedule(Schedule):
    """
    Represents a football schedule.

    Args:
        url (str): The URL of the football schedule.

    Attributes:
        schedule (list): The parsed football table for the schedule.
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.schedule = self.parse_football_table("games")


class BasketballSchedule(Schedule):
    """
    Represents a basketball schedule.

    Args:
        url (str): The URL of the basketball schedule.

    Attributes:
        schedule (list): The parsed basketball table for the schedule.
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.schedule = self.parse_basketball_table("schedule")


class SoccerSchedule(Schedule):
    """
    Represents a soccer schedule.

    Args:
        url (str): The URL of the soccer schedule.

    Attributes:
        schedule (list): The parsed soccer table for the schedule.
    """

    def __init__(self, url: str):
        super().__init__(url)

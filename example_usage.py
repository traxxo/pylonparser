from pylonparser.schedules import BasketballSchedule
import pandas as pd

if __name__ == "__main__":
    # Define the URL for the game stats
    url = "https://www.pro-football-reference.com/years/2022/games.htm"
    url = "https://www.basketball-reference.com/leagues/NBA_2024_games-november.html"
    data = BasketballSchedule(url)
    df = pd.DataFrame(data.schedule)
    print(df.head())

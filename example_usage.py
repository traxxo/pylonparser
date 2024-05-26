from pylonparser.matches import BasketballMatch
import pandas as pd

if __name__ == "__main__":
    # Define the URL for the game stats
    url = "https://www.basketball-reference.com/boxscores/202405220MIN.html"

    basketball_match = BasketballMatch(url)
    df = pd.DataFrame(basketball_match.basic_away)
    print(df.head())

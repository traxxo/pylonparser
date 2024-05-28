# PylonParser

This package is used to obtain Pro Football Reference and Basketball Reference using web scraping tables, for example to perform data analysis or data science. All rights belong to the respective sites and the package should not be used to load their servers. Please read the corresponding specifications in their robots.txt files.

## Installation

```sh
pip install pylonparser
```

Usage
Provide instructions on how to use your project. Include code examples if possible.
```sh
url = "https://www.basketball-reference.com/boxscores/202405220MIN.html"

basketball_match = BasketballMatch(url)
df = pd.DataFrame(basketball_match.basic_away)
print(df.head())

❯
          id             player     mp    fg   fga  fg_pct  fg3  fg3a  fg3_pct   ft  fta  ft_pct  orb  drb  trb  ast  stl  blk  tov   pf   pts plus_minus reason
0  washipj01    P.J. Washington  40:50   4.0  10.0   0.400  2.0   8.0     0.25  3.0  3.0   1.000  0.0  7.0  7.0  0.0  0.0  2.0  3.0  4.0  13.0        +12    NaN
1  doncilu01        Luka Dončić  40:45  12.0  26.0   0.462  3.0  10.0     0.30  6.0  7.0   0.857  0.0  6.0  6.0  8.0  3.0  1.0  4.0  2.0  33.0         -9    NaN
2  irvinky01       Kyrie Irving  40:09  12.0  23.0   0.522  0.0   3.0     0.00  6.0  6.0   1.000  1.0  4.0  5.0  4.0  0.0  1.0  2.0  3.0  30.0         +5    NaN
3  jonesde02  Derrick Jones Jr.  34:55   4.0   9.0   0.444  0.0   2.0     0.00  0.0  0.0   0.000  2.0  2.0  4.0  2.0  0.0  0.0  0.0  1.0   8.0         -8    NaN
4  gaffoda01     Daniel Gafford  21:07   5.0   9.0   0.556  0.0   0.0     0.00  0.0  0.0   0.000  4.0  5.0  9.0  0.0  0.0  1.0  2.0  2.0  10.0        -15    NaN

```
Testing
This project uses pytest for testing. To run the tests, use:

Contributing
Contributions are welcome! Please read the contributing guidelines first.

License
This project is licensed under the MIT License. See the LICENSE file for details.

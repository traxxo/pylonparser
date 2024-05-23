# PylonParser

A tool to parse football game stats.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the project and its dependencies, run:

```sh
pip install pylonparser
```

Usage
Provide instructions on how to use your project. Include code examples if possible.
```sh
import pandas as pd
from pylonparser.parser import get_game_stats

game_stats = get_game_stats("https://www.pro-football-reference.com/boxscores/202009100kan.htm", "player_offense")
df = pd.DataFrame(game_stats)
print(df.head())

❯
           player        id team pass_cmp pass_att pass_yds pass_td pass_int pass_sacked  ... rush_td rush_long targets rec rec_yds rec_td rec_long fumbles fumbles_lost
0  Deshaun Watson  WatsDe00  HOU       20       32      253       1        1           4  ...       1        13       0   0       0      0        0       0            0
1   David Johnson  JohnDa08  HOU        0        0        0       0        0           0  ...       1        19       4   3      32      0       15       0            0
2    Duke Johnson  JohnDu00  HOU        0        0        0       0        0           0  ...       0         7       1   0       0      0        0       0            0
3     Will Fuller  FullWi01  HOU        0        0        0       0        0           0  ...       0         0      10   8     112      0       31       0            0
4    Jordan Akins  AkinJo00  HOU        0        0        0       0        0           0  ...       0         0       2   2      39      1       20       0            0
```
Testing
This project uses pytest for testing. To run the tests, use:

Contributing
Contributions are welcome! Please read the contributing guidelines first.

License
This project is licensed under the MIT License. See the LICENSE file for details.

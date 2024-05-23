import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from pylonparser.parser import get_page, parse_tr_table, get_game_stats

# Sample HTML for testing
sample_html = """
<html>
<body>
<table id="example_table">
<tbody>
<tr data-row="0" class="rowSum"><th scope="row" class="left " data-append-csv="WatsDe00" data-stat="player"><a href="/players/W/WatsDe00.htm">Deshaun Watson</a></th>
<td class="left " data-stat="team">HOU</td>
<td class="right " data-stat="pass_cmp">20</td>
<td class="right " data-stat="pass_att">32</td>
<td class="right " data-stat="pass_yds">253</td>
<td class="right " data-stat="pass_td">1</td>
<td class="right " data-stat="pass_int">1</td>
<td class="right " data-stat="pass_sacked">4</td>
<td class="right " data-stat="pass_sacked_yds">11</td>
<td class="right " data-stat="pass_long">31</td>
<td class="right " data-stat="pass_rating">84.5</td>
<td class="right " data-stat="rush_att">6</td>
<td class="right " data-stat="rush_yds">27</td>
<td class="right " data-stat="rush_td">1</td>
<td class="right " data-stat="rush_long">13</td>
<td class="right iz" data-stat="targets">0</td>
<td class="right iz" data-stat="rec">0</td>
<td class="right iz" data-stat="rec_yds">0</td>
<td class="right iz" data-stat="rec_td">0</td>
<td class="right iz" data-stat="rec_long">0</td>
<td class="right iz" data-stat="fumbles">0</td>
<td class="right iz" data-stat="fumbles_lost">0</td>
</tr>
<tr data-row="1">
<th scope="row" class="left " data-append-csv="JohnDa08" data-stat="player"><a href="/players/J/JohnDa08.htm">David Johnson</a></th>
<td class="left " data-stat="team">HOU</td>
<td class="right iz" data-stat="pass_cmp">0</td>
<td class="right iz" data-stat="pass_att">0</td>
<td class="right iz" data-stat="pass_yds">0</td>
<td class="right iz" data-stat="pass_td">0</td>
<td class="right iz" data-stat="pass_int">0</td>
<td class="right iz" data-stat="pass_sacked">0</td>
<td class="right iz" data-stat="pass_sacked_yds">0</td>
<td class="right iz" data-stat="pass_long">0</td>
<td class="right iz" data-stat="pass_rating"></td>
<td class="right " data-stat="rush_att">11</td>
<td class="right " data-stat="rush_yds">77</td>
<td class="right " data-stat="rush_td">1</td>
<td class="right " data-stat="rush_long">19</td>
<td class="right " data-stat="targets">4</td>
<td class="right " data-stat="rec">3</td>
<td class="right " data-stat="rec_yds">32</td>
<td class="right iz" data-stat="rec_td">0</td>
<td class="right " data-stat="rec_long">15</td>
<td class="right iz" data-stat="fumbles">0</td>
<td class="right iz" data-stat="fumbles_lost">0</td>
</tr>
</tbody>
</table>
</body>
</html>
"""


# Mock function for requests.get
def mock_requests_get(url):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = sample_html
    return mock_response


@patch("pylonparser.parser.requests.get", side_effect=mock_requests_get)
def test_get_page(mock_get):
    url = "http://example.com"
    soup = get_page(url)
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("table", id="example_table") is not None


def test_parse_tr_table():
    soup = BeautifulSoup(sample_html, "html.parser")
    table_list = parse_tr_table(soup, "#example_table")
    assert len(table_list) == 2
    assert table_list[0]["player"] == "Deshaun Watson"
    assert table_list[0]["pass_cmp"] == "20"
    assert table_list[1]["player"] == "David Johnson"
    assert table_list[1]["pass_cmp"] == "0"  # Ensure empty strings are handled


@patch("pylonparser.parser.requests.get", side_effect=mock_requests_get)
def test_get_game_stats(mock_get):
    url = "http://example.com"
    table = "example_table"
    stats = get_game_stats(url, table)
    assert len(stats) == 2
    assert stats[0]["player"] == "Deshaun Watson"
    assert stats[0]["pass_cmp"] == "20"
    assert stats[1]["player"] == "David Johnson"
    assert stats[1]["pass_cmp"] == "0"  # Ensure empty strings are handled

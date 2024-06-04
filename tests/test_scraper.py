import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from pylonparser.scraper import WebScraper


@pytest.fixture
def mock_html():
    # Provide a simple HTML for testing
    return """
    <html>
        <head></head>
        <body>
            <table id="box-123-game-basic">
                <tbody>
                    <tr>
                        <th data-stat="player" data-append-csv="player_id">Player</th>
                        <td data-stat="pts">10</td>
                    </tr>
                    <tr>
                        <th data-stat="player" data-append-csv="another_player_id">Another Player</th>
                        <td data-stat="pts">20</td>
                    </tr>
                </tbody>
            </table>
            <table id="box-456-game-advanced">
                <tbody>
                    <tr>
                        <th data-stat="player" data-append-csv="advanced_player_id">Advanced Player</th>
                        <td data-stat="efficiency">30</td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """


@pytest.fixture
def mock_response(mock_html):
    mock_resp = Mock()
    mock_resp.content = mock_html
    return mock_resp


@patch("requests.get")
def test_get_page(mock_get, mock_response):
    mock_get.return_value = mock_response
    url = "http://fakeurl.com"
    scraper = WebScraper(url)
    assert isinstance(scraper.soup, BeautifulSoup)
    assert mock_get.called_once_with(url)


@patch("requests.get")
def test_find_basketball_table_ids(mock_get, mock_response):
    mock_get.return_value = mock_response
    url = "http://fakeurl.com"
    scraper = WebScraper(url)
    table_ids = scraper.find_basketball_table_ids()

    assert "box-123-game-basic" in table_ids
    assert "box-456-game-advanced" in table_ids


@patch("requests.get")
def test_translate_table_id(mock_get, mock_response):
    mock_get.return_value = mock_response
    url = "http://fakeurl.com"
    scraper = WebScraper(url)

    html = HTMLParser(mock_response.content)
    table_id = scraper.translate_table_id(html, "basic", 1)

    assert table_id == "box-123-game-basic"


if __name__ == "__main__":
    pytest.main()

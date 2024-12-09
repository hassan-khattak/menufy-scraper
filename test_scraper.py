import unittest
from unittest.mock import patch, MagicMock
from scraper import scrape_menufy, parse_json_ld, scrape_menu
from bs4 import BeautifulSoup

class TestMenufyScraper(unittest.TestCase):
    def setUp(self):
        self.valid_url = "https://valid-menufy-url.com"
        self.invalid_url = "https://invalid-url.com"
        self.empty_response_html = "<html></html>"
        self.valid_response_html = """
        <html>
        <script type="application/ld+json">
        {
            "name": "Test Restaurant",
            "address": {
                "streetAddress": "123 Test St",
                "addressLocality": "Test City",
                "addressRegion": "TS",
                "postalCode": "12345",
                "addressCountry": "Test Country"
            },
            "geo": {
                "latitude": "12.34",
                "longitude": "56.78"
            },
            "servesCuisine": ["Test Cuisine"]
        }
        </script>
        <div class="category">
            <h2>Appetizers</h2>
            <div class="category-item-wrapper">
                <div class="category-item-name">Spring Rolls</div>
                <div class="category-item-description">Delicious spring rolls</div>
                <div class="category-item-price">$5.99</div>
                <div class="category-item-image lazy-background-image" data-src="https://example.com/image.png"></div>
            </div>
        </div>
        </html>
        """

    @patch("scraper.requests.get")
    def test_valid_url(self, mock_get):
        # Mock a valid response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.valid_response_html
        mock_get.return_value = mock_response

        result = scrape_menufy(self.valid_url)
        self.assertIn("restaurant", result)
        self.assertIn("menu", result)
        self.assertEqual(result["restaurant"]["name"], "Test Restaurant")
        self.assertEqual(result["menu"][0]["category"], "Appetizers")
        self.assertEqual(result["menu"][0]["items"][0]["name"], "Spring Rolls")
        self.assertEqual(result["menu"][0]["items"][0]["price"], 5.99)

    @patch("scraper.requests.get")
    def test_invalid_url(self, mock_get):
        # Mock a response for an invalid URL
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = self.empty_response_html
        mock_get.return_value = mock_response

        result = scrape_menufy(self.invalid_url)
        self.assertEqual(result, {})  # Should return an empty dictionary

    @patch("scraper.requests.get")
    def test_empty_data(self, mock_get):
        # Mock a response with no restaurant or menu data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.empty_response_html
        mock_get.return_value = mock_response

        result = scrape_menufy(self.valid_url)
        self.assertEqual(result, {})  # Should return an empty dictionary

    def test_parse_json_ld_valid(self):
        # Valid JSON-LD script
        valid_json_ld = """
        {
            "name": "Test Restaurant",
            "address": {
                "streetAddress": "123 Test St",
                "addressLocality": "Test City",
                "addressRegion": "TS",
                "postalCode": "12345",
                "addressCountry": "Test Country"
            },
            "geo": {
                "latitude": "12.34",
                "longitude": "56.78"
            },
            "servesCuisine": ["Test Cuisine"]
        }
        """
        result = parse_json_ld(valid_json_ld)
        self.assertEqual(result["name"], "Test Restaurant")
        self.assertEqual(result["geo"]["latitude"], "12.34")
        self.assertEqual(result["address"], "123 Test St")

    def test_parse_json_ld_invalid(self):
        # Invalid JSON-LD script
        invalid_json_ld = "<html></html>"
        result = parse_json_ld(invalid_json_ld)
        self.assertEqual(result, {})  # Should return an empty dictionary

    def test_scrape_menu_valid(self):
        # Valid HTML with menu data
        soup = BeautifulSoup(self.valid_response_html, "html.parser")
        result = scrape_menu(soup)
        self.assertEqual(result[0]["category"], "Appetizers")
        self.assertEqual(result[0]["items"][0]["name"], "Spring Rolls")
        self.assertEqual(result[0]["items"][0]["price"], 5.99)

    def test_scrape_menu_empty(self):
        # Empty HTML
        soup = BeautifulSoup(self.empty_response_html, "html.parser")
        result = scrape_menu(soup)
        self.assertEqual(result, [])  # Should return an empty list

if __name__ == "__main__":
    unittest.main()

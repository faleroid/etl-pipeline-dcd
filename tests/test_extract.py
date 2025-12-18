import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.extract import fetch_url, extract_products_detail, scrape_products

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.get')
    def test_fetch_url_success(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Content</html>"
        mock_get.return_value = mock_response

        # Execute
        result = fetch_url("http://example.com")

        # Verify
        self.assertEqual(result, b"<html>Content</html>")
        mock_get.assert_called_once()

    @patch('utils.extract.requests.get')
    def test_fetch_url_request_exception(self, mock_get):
        # Setup mock to raise exception
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Connection error")

        # Execute
        result = fetch_url("http://example.com")

        # Verify
        self.assertIsNone(result)

    @patch('utils.extract.requests.get')
    def test_fetch_url_general_exception(self, mock_get):
        # Setup mock to raise general exception
        mock_get.side_effect = Exception("General error")

        # Execute
        result = fetch_url("http://example.com")

        # Verify
        self.assertIsNone(result)

    def test_extract_products_detail_success(self):
        html_content = """
        <div class="collection-card">
            <div class="product-details">
                <h3>Cool Shirt</h3>
                <div class="price-container">
                    <span class="price">$20.00</span>
                </div>
                <p>Rating: 4.5</p>
                <p>Colors: Red, Blue</p>
                <p>Size: M</p>
                <p>Men</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        product = soup.find("div", class_="collection-card")
        
        result = extract_products_detail(product)
        
        self.assertEqual(result["Title"], "Cool Shirt")
        self.assertEqual(result["Price"], "$20.00")
        self.assertEqual(result["Rating"], "Rating: 4.5")
        self.assertEqual(result["Colors"], "Colors: Red, Blue")
        self.assertEqual(result["Size"], "Size: M")
        self.assertEqual(result["Gender"], "Men")
        self.assertIsNotNone(result["Timestamp"])

    def test_extract_products_detail_missing_price(self):
        html_content = """
        <div class="collection-card">
            <div class="product-details">
                <h3>Mystery Item</h3>
                <p>Rating: 5.0</p>
                <p>Colors: Black</p>
                <p>Size: L</p>
                <p>Unisex</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        product = soup.find("div", class_="collection-card")
        
        result = extract_products_detail(product)
        
        self.assertEqual(result["Title"], "Mystery Item")
        self.assertIsNone(result["Price"])

    @patch('utils.extract.fetch_url')
    def test_scrape_products_success(self, mock_fetch):
        # Mock HTML content
        html_content = """
        <div class="collection-grid" id="collectionList">
            <div class="collection-card">
                <div class="product-details">
                    <h3>Item 1</h3>
                    <div class="price-container"><span class="price">$10</span></div>
                    <p>Rating: 4</p><p>Colors: R</p><p>Size: S</p><p>M</p>
                </div>
            </div>
            <div class="collection-card">
                <div class="product-details">
                    <h3>Item 2</h3>
                    <div class="price-container"><span class="price">$20</span></div>
                    <p>Rating: 5</p><p>Colors: B</p><p>Size: L</p><p>F</p>
                </div>
            </div>
        </div>
        """
        mock_fetch.return_value = html_content.encode('utf-8')

        result = scrape_products("http://example.com")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Title"], "Item 1")
        self.assertEqual(result[1]["Title"], "Item 2")

    @patch('utils.extract.fetch_url')
    def test_scrape_products_no_content(self, mock_fetch):
        mock_fetch.return_value = None
        result = scrape_products("http://example.com")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()

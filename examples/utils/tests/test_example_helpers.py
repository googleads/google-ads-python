import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import requests # Required for requests.exceptions.RequestException
from examples.utils.example_helpers import get_printable_datetime, get_image_bytes_from_url

class TestGetPrintableDatetime(unittest.TestCase): # Renamed for clarity

    def test_get_printable_datetime_returns_string(self):
        """Tests that get_printable_datetime returns a string."""
        self.assertIsInstance(get_printable_datetime(), str)

    def test_get_printable_datetime_iso_format(self):
        """Tests that get_printable_datetime returns a string in ISO format."""
        datetime_str = get_printable_datetime()
        # Attempt to parse the string to ensure it's in ISO format.
        # datetime.fromisoformat() will raise a ValueError if not.
        try:
            datetime.fromisoformat(datetime_str)
        except ValueError:
            self.fail(f"'{datetime_str}' is not a valid ISO format datetime string.")

class TestGetImageBytesFromUrl(unittest.TestCase):

    @patch('requests.get')
    def test_returns_bytes_for_valid_url(self, mock_requests_get):
        """Tests that the function returns bytes for a valid URL."""
        sample_bytes = b'sampleimagedata'
        mock_response = MagicMock()
        mock_response.content = sample_bytes
        mock_requests_get.return_value = mock_response

        result = get_image_bytes_from_url("http://example.com/image.jpg")
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, sample_bytes)
        mock_requests_get.assert_called_once_with("http://example.com/image.jpg")

    @patch('requests.get')
    def test_raises_exception_for_invalid_url(self, mock_requests_get):
        """Tests that the function raises an exception for an invalid URL."""
        mock_requests_get.side_effect = requests.exceptions.RequestException("Test error")

        with self.assertRaises(requests.exceptions.RequestException):
            get_image_bytes_from_url("http://invalid-url-that-does-not-exist.com/image.png")
        mock_requests_get.assert_called_once_with("http://invalid-url-that-does-not-exist.com/image.png")

    @patch('requests.get')
    def test_correctly_downloads_image(self, mock_requests_get):
        """Tests that the function correctly 'downloads' image bytes from a valid URL."""
        expected_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        mock_response = MagicMock()
        mock_response.content = expected_bytes
        mock_requests_get.return_value = mock_response

        actual_bytes = get_image_bytes_from_url("http://example.com/realimage.png")
        self.assertEqual(actual_bytes, expected_bytes)
        mock_requests_get.assert_called_once_with("http://example.com/realimage.png")


if __name__ == '__main__':
    unittest.main()

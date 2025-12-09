"""
BrandBook Test Suite
Basic tests for the application
"""

import pytest
from unittest.mock import patch, MagicMock


class TestImports:
    """Test that all modules can be imported correctly"""

    def test_import_app(self):
        """Test FastAPI app imports"""
        from app import app
        assert app is not None

    def test_import_generator(self):
        """Test generator module imports"""
        from generator import brochure_system_prompt, link_system_prompt
        assert brochure_system_prompt is not None
        assert link_system_prompt is not None

    def test_import_scraper(self):
        """Test scraper module imports"""
        from scraper import fetch_website_contents, fetch_website_links
        assert fetch_website_contents is not None
        assert fetch_website_links is not None

    def test_import_url_finder(self):
        """Test URL finder module imports"""
        from url_finder import find_company_url, extract_domain_from_results
        assert find_company_url is not None
        assert extract_domain_from_results is not None


class TestURLFinder:
    """Test URL finding functionality"""

    def test_extract_domain_from_results_empty(self):
        """Test with empty results"""
        from url_finder import extract_domain_from_results
        result = extract_domain_from_results([])
        assert result is None

    def test_extract_domain_from_results_with_data(self):
        """Test domain extraction with valid data"""
        from url_finder import extract_domain_from_results

        results = [
            {"href": "https://openai.com", "title": "OpenAI"},
            {"href": "https://twitter.com/openai", "title": "OpenAI Twitter"},
        ]

        result = extract_domain_from_results(results)
        assert result == "https://openai.com"

    def test_extract_domain_prefers_com(self):
        """Test that .com domains are preferred"""
        from url_finder import extract_domain_from_results

        results = [
            {"href": "https://example.ai/about", "title": "Example AI"},
            {"href": "https://example.com", "title": "Example"},
        ]

        result = extract_domain_from_results(results)
        assert ".com" in result

    def test_skip_social_media_domains(self):
        """Test that social media domains are skipped"""
        from url_finder import extract_domain_from_results

        results = [
            {"href": "https://twitter.com/company", "title": "Twitter"},
            {"href": "https://facebook.com/company", "title": "Facebook"},
            {"href": "https://company.com", "title": "Company"},
        ]

        result = extract_domain_from_results(results)
        assert "twitter" not in result
        assert "facebook" not in result


class TestScraper:
    """Test web scraping functionality"""

    @patch('scraper.requests.get')
    def test_fetch_website_contents(self, mock_get):
        """Test website content fetching"""
        from scraper import fetch_website_contents

        # Mock response
        mock_response = MagicMock()
        mock_response.content = b"""
        <html>
            <head><title>Test Page</title></head>
            <body><p>Hello World</p></body>
        </html>
        """
        mock_get.return_value = mock_response

        result = fetch_website_contents("https://example.com")

        assert "Test Page" in result
        assert "Hello World" in result

    @patch('scraper.requests.get')
    def test_fetch_website_links(self, mock_get):
        """Test website link extraction"""
        from scraper import fetch_website_links

        # Mock response
        mock_response = MagicMock()
        mock_response.content = b"""
        <html>
            <body>
                <a href="/about">About</a>
                <a href="/careers">Careers</a>
                <a href="https://example.com/contact">Contact</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = fetch_website_links("https://example.com")

        assert "/about" in result
        assert "/careers" in result
        assert "https://example.com/contact" in result


class TestGenerator:
    """Test brochure generation functionality"""

    def test_brochure_system_prompt_content(self):
        """Test brochure system prompt has required content"""
        from generator import brochure_system_prompt

        assert "brochure" in brochure_system_prompt.lower()
        assert "company" in brochure_system_prompt.lower()
        assert "English" in brochure_system_prompt

    def test_link_system_prompt_content(self):
        """Test link system prompt has required content"""
        from generator import link_system_prompt

        assert "links" in link_system_prompt.lower()
        assert "JSON" in link_system_prompt

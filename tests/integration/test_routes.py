"""Integration tests for page routes."""

import pytest


class TestMainRoutes:
    """Tests for main blueprint routes."""

    def test_homepage(self, client):
        """Test homepage loads successfully."""
        response = client.get('/')

        assert response.status_code == 200
        assert b'AnyUnit' in response.data or b'Unit Converter' in response.data

    def test_homepage_has_categories(self, client):
        """Test homepage displays unit categories."""
        response = client.get('/')

        assert response.status_code == 200
        # Check for some category names
        assert b'Length' in response.data
        assert b'Weight' in response.data
        assert b'Temperature' in response.data

    def test_privacy_policy(self, client):
        """Test privacy policy page."""
        response = client.get('/privacy-policy')

        assert response.status_code == 200
        assert b'Privacy' in response.data

    def test_robots_txt(self, client):
        """Test robots.txt endpoint."""
        response = client.get('/robots.txt')

        assert response.status_code == 200
        assert response.content_type == 'text/plain; charset=utf-8'
        assert b'User-agent' in response.data
        assert b'Sitemap' in response.data

    def test_sitemap_xml(self, client):
        """Test sitemap.xml endpoint."""
        response = client.get('/sitemap.xml')

        assert response.status_code == 200
        assert response.content_type == 'application/xml; charset=utf-8'
        assert b'<?xml' in response.data
        assert b'<urlset' in response.data
        assert b'<url>' in response.data


class TestConverterRoutes:
    """Tests for converter blueprint routes."""

    def test_category_page_length(self, client):
        """Test length category page."""
        response = client.get('/convert/length/')

        assert response.status_code == 200
        assert b'Length' in response.data
        assert b'Meter' in response.data

    def test_category_page_temperature(self, client):
        """Test temperature category page."""
        response = client.get('/convert/temperature/')

        assert response.status_code == 200
        assert b'Temperature' in response.data

    def test_category_page_weight(self, client):
        """Test weight category page."""
        response = client.get('/convert/weight/')

        assert response.status_code == 200
        assert b'Weight' in response.data

    def test_category_page_invalid(self, client):
        """Test invalid category returns 404."""
        response = client.get('/convert/invalid/')

        assert response.status_code == 404

    def test_conversion_page(self, client):
        """Test specific conversion page."""
        response = client.get('/convert/length/m-to-ft')

        assert response.status_code == 200
        assert b'Meter' in response.data
        assert b'Foot' in response.data

    def test_conversion_page_temperature(self, client):
        """Test temperature conversion page."""
        response = client.get('/convert/temperature/c-to-f')

        assert response.status_code == 200
        assert b'Celsius' in response.data
        assert b'Fahrenheit' in response.data

    def test_conversion_page_invalid_units(self, client):
        """Test conversion page with invalid units returns 404."""
        response = client.get('/convert/length/invalid-to-ft')

        assert response.status_code == 404

    def test_conversion_page_has_table(self, client):
        """Test conversion page includes conversion table."""
        response = client.get('/convert/length/km-to-mi')

        assert response.status_code == 200
        # Should have common values table
        assert b'<table' in response.data or b'table' in response.data.lower()

    def test_category_normalization(self, client):
        """Test category name normalization (redirect)."""
        response = client.get('/convert/LENGTH/', follow_redirects=True)

        assert response.status_code == 200
        assert b'Length' in response.data


class TestAviationRoutes:
    """Tests for aviation blueprint routes."""

    def test_aviation_calculators_page(self, client):
        """Test aviation calculators main page."""
        response = client.get('/aviation/')

        assert response.status_code == 200
        # Should have calculator forms
        assert b'Fuel' in response.data or b'fuel' in response.data.lower()
        assert b'Ground Speed' in response.data or b'ground' in response.data.lower()


class TestMarkdownRoutes:
    """Tests for markdown blueprint routes."""

    def test_markdown_page(self, client):
        """Test markdown converter page."""
        response = client.get('/markdown/')

        assert response.status_code == 200
        assert b'Markdown' in response.data

    def test_download_html(self, client):
        """Test HTML download endpoint."""
        response = client.post('/markdown/download/html',
            data={'markdown': '# Test\n\nHello'}
        )

        assert response.status_code == 200
        assert response.content_type == 'text/html; charset=utf-8'
        assert b'<!DOCTYPE html>' in response.data


class TestTimezoneRoutes:
    """Tests for timezone blueprint routes."""

    def test_timezone_page(self, client):
        """Test timezone converter page."""
        response = client.get('/time/')

        assert response.status_code == 200


class TestTextFilesRoutes:
    """Tests for text files blueprint routes."""

    def test_text_files_page(self, client):
        """Test text files converter page."""
        response = client.get('/text/')

        assert response.status_code == 200
        # Should list conversion formats
        assert b'JSON' in response.data or b'json' in response.data.lower()


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_page(self, client):
        """Test 404 error page."""
        response = client.get('/nonexistent-page-12345')

        assert response.status_code == 404

    def test_404_returns_error_page(self, client):
        """Test 404 returns an error page."""
        response = client.get('/nonexistent-page-12345')

        assert response.status_code == 404
        # Should indicate not found
        assert b'Not Found' in response.data or b'404' in response.data


class TestSeoFeatures:
    """Tests for SEO features in pages."""

    def test_homepage_has_meta_tags(self, client):
        """Test homepage has meta tags."""
        response = client.get('/')

        assert response.status_code == 200
        assert b'<meta' in response.data
        assert b'description' in response.data

    def test_conversion_page_has_canonical(self, client):
        """Test conversion page has canonical URL."""
        response = client.get('/convert/length/m-to-ft')

        assert response.status_code == 200
        assert b'canonical' in response.data

    def test_pages_have_title(self, client):
        """Test pages have title tags."""
        response = client.get('/convert/weight/')

        assert response.status_code == 200
        assert b'<title>' in response.data

    def test_sitemap_includes_categories(self, client):
        """Test sitemap includes category pages."""
        response = client.get('/sitemap.xml')

        assert response.status_code == 200
        assert b'/convert/length' in response.data
        assert b'/convert/weight' in response.data
        assert b'/convert/temperature' in response.data

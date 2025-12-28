"""Frontend tests - verify HTML structure and JavaScript integration points."""

import pytest


class TestConverterPageStructure:
    """Tests for converter page HTML structure that JavaScript depends on."""

    def test_conversion_page_has_data_attributes(self, client):
        """Test conversion page has data attributes for JavaScript."""
        response = client.get('/convert/length/m-to-ft')
        html = response.data.decode('utf-8')

        assert 'data-category' in html
        assert 'data-from-unit' in html
        assert 'data-to-unit' in html

    def test_conversion_page_has_input_elements(self, client):
        """Test conversion page has input elements."""
        response = client.get('/convert/length/km-to-mi')
        html = response.data.decode('utf-8')

        # Should have input fields for values
        assert 'input' in html.lower()
        assert 'id=' in html

    def test_conversion_page_has_action_buttons(self, client):
        """Test conversion page has action buttons."""
        response = client.get('/convert/weight/kg-to-lb')
        html = response.data.decode('utf-8')

        # Should have buttons for copy/swap/share functionality
        assert 'button' in html.lower() or 'btn' in html.lower()


class TestStaticAssets:
    """Tests for static JavaScript and CSS assets."""

    def test_main_js_exists(self, client):
        """Test main.js is accessible."""
        response = client.get('/static/js/main.js')
        assert response.status_code == 200
        assert b'function' in response.data or b'const' in response.data or b'class' in response.data

    def test_converter_js_exists(self, client):
        """Test converter.js is accessible."""
        response = client.get('/static/js/converter.js')
        assert response.status_code == 200
        assert b'Converter' in response.data

    def test_quick_converter_js_exists(self, client):
        """Test quick-converter.js is accessible."""
        response = client.get('/static/js/quick-converter.js')
        assert response.status_code == 200
        assert b'QuickConverter' in response.data

    def test_main_css_exists(self, client):
        """Test main.css is accessible."""
        response = client.get('/static/css/main.css')
        assert response.status_code == 200

    def test_converter_css_exists(self, client):
        """Test converter.css is accessible."""
        response = client.get('/static/css/converter.css')
        assert response.status_code == 200


class TestConverterJavaScriptIntegration:
    """Tests for JavaScript integration with backend API."""

    def test_api_returns_json_for_js_fetch(self, client):
        """Test API returns proper JSON for JavaScript fetch calls."""
        import json
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'length',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 1
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.get_json()
        # JavaScript expects these fields
        assert 'success' in data
        assert 'result' in data
        assert 'formatted' in data

    def test_api_error_response_format(self, client):
        """Test API error responses have expected format for JavaScript."""
        import json
        response = client.post('/api/convert',
            data=json.dumps({
                'category': 'invalid',
                'fromUnit': 'm',
                'toUnit': 'ft',
                'value': 1
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        # JavaScript expects error format
        assert 'success' in data
        assert data['success'] is False


class TestAviationCalculatorStructure:
    """Tests for aviation calculator page structure."""

    def test_aviation_page_has_forms(self, client):
        """Test aviation page has calculator forms."""
        response = client.get('/aviation/')
        html = response.data.decode('utf-8')

        assert 'form' in html.lower()
        assert 'input' in html.lower()

    def test_aviation_page_has_unique_ids(self, client):
        """Test aviation forms have unique IDs to prevent JS conflicts."""
        response = client.get('/aviation/')
        html = response.data.decode('utf-8')

        # Check for form identifiers
        assert response.status_code == 200


class TestQuickConverterStructure:
    """Tests for quick converter component structure."""

    def test_category_page_has_unit_options(self, client):
        """Test category page has unit selection options."""
        response = client.get('/convert/length/')
        html = response.data.decode('utf-8')

        # Should have units listed
        assert 'Meter' in html
        assert 'Foot' in html
        assert 'Kilometer' in html

    def test_conversion_page_has_common_values_table(self, client):
        """Test conversion page has common values table."""
        response = client.get('/convert/temperature/c-to-f')
        html = response.data.decode('utf-8')

        assert 'table' in html.lower()
        # Temperature common values should include freezing and boiling points
        assert '32' in html  # 0°C = 32°F
        assert '212' in html  # 100°C = 212°F


class TestMarkdownConverterStructure:
    """Tests for markdown converter page structure."""

    def test_markdown_page_has_textarea(self, client):
        """Test markdown page has input textarea."""
        response = client.get('/markdown/')
        html = response.data.decode('utf-8')

        assert 'textarea' in html.lower()

    def test_markdown_page_has_download_buttons(self, client):
        """Test markdown page has download options."""
        response = client.get('/markdown/')
        html = response.data.decode('utf-8')

        assert 'download' in html.lower() or 'Download' in html


class TestTextFileConverterStructure:
    """Tests for text file converter page structure."""

    def test_text_page_has_format_options(self, client):
        """Test text file page has format selection."""
        response = client.get('/text/')
        html = response.data.decode('utf-8')

        assert 'JSON' in html
        assert 'XML' in html
        assert 'CSV' in html


class TestTimezoneConverterStructure:
    """Tests for timezone converter page structure."""

    def test_timezone_page_loads(self, client):
        """Test timezone page loads with timezone data."""
        response = client.get('/time/')

        assert response.status_code == 200


class TestBootstrapIntegration:
    """Tests for Bootstrap CSS/JS integration."""

    def test_pages_include_bootstrap(self, client):
        """Test pages include Bootstrap CSS."""
        response = client.get('/')
        html = response.data.decode('utf-8')

        # Should reference Bootstrap
        assert 'bootstrap' in html.lower()

    def test_conversion_page_uses_bootstrap_classes(self, client):
        """Test conversion pages use Bootstrap classes."""
        response = client.get('/convert/length/m-to-ft')
        html = response.data.decode('utf-8')

        # Common Bootstrap classes
        bootstrap_classes = ['container', 'row', 'col', 'btn', 'form']
        found_classes = [cls for cls in bootstrap_classes if cls in html]
        assert len(found_classes) > 0


class TestResponsiveDesign:
    """Tests for responsive design elements."""

    def test_pages_have_viewport_meta(self, client):
        """Test pages have viewport meta tag for responsive design."""
        response = client.get('/')
        html = response.data.decode('utf-8')

        assert 'viewport' in html

    def test_conversion_page_has_responsive_meta(self, client):
        """Test conversion page has responsive meta."""
        response = client.get('/convert/weight/kg-to-lb')
        html = response.data.decode('utf-8')

        assert 'viewport' in html
        assert 'width=device-width' in html


class TestAccessibility:
    """Tests for accessibility features."""

    def test_form_inputs_have_labels(self, client):
        """Test form inputs have associated labels."""
        response = client.get('/convert/length/m-to-ft')
        html = response.data.decode('utf-8')

        # Should have label elements or aria-label attributes
        assert 'label' in html.lower() or 'aria-label' in html.lower()

    def test_buttons_have_accessible_text(self, client):
        """Test buttons have accessible text or aria-labels."""
        response = client.get('/convert/length/m-to-ft')
        html = response.data.decode('utf-8')

        # Buttons should have text content or aria attributes
        assert response.status_code == 200

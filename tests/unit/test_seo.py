"""Unit tests for seo.py module."""

import pytest
import json
from app.utils.seo import generate_meta_tags


class TestGenerateMetaTags:
    """Tests for generate_meta_tags function."""

    def test_homepage_meta_tags(self):
        """Test meta tags for homepage (no category)."""
        result = generate_meta_tags()

        assert 'title' in result
        assert 'description' in result
        assert 'canonical' in result
        assert result['canonical'] == '/'
        assert 'Unit Converter' in result['title']

    def test_homepage_with_base_url(self):
        """Test homepage meta tags with base URL."""
        result = generate_meta_tags(base_url='https://example.com/')

        assert 'json_ld' in result
        json_ld = json.loads(result['json_ld'])
        assert json_ld['@type'] == 'WebSite'
        assert json_ld['name'] == 'AnyUnit'
        assert json_ld['url'] == 'https://example.com'

    def test_category_meta_tags(self):
        """Test meta tags for category page."""
        result = generate_meta_tags(category='length')

        assert 'Length' in result['title']
        assert 'length' in result['description'].lower()
        assert result['canonical'] == '/convert/length'

    def test_category_with_base_url(self):
        """Test category meta tags with base URL."""
        result = generate_meta_tags(category='weight', base_url='https://example.com/')

        assert 'json_ld' in result
        json_ld = json.loads(result['json_ld'])
        assert json_ld['@type'] == 'BreadcrumbList'
        assert len(json_ld['itemListElement']) == 2
        assert json_ld['itemListElement'][0]['name'] == 'Home'
        assert json_ld['itemListElement'][1]['name'] == 'Weight'

    def test_conversion_meta_tags(self):
        """Test meta tags for conversion page."""
        result = generate_meta_tags(category='length', from_unit='m', to_unit='ft')

        assert 'M' in result['title'] and 'FT' in result['title']
        assert result['canonical'] == '/convert/length/m-to-ft'

    def test_conversion_with_base_url(self):
        """Test conversion meta tags with base URL."""
        result = generate_meta_tags(
            category='temperature',
            from_unit='c',
            to_unit='f',
            base_url='https://example.com/'
        )

        assert 'json_ld' in result
        json_ld = json.loads(result['json_ld'])
        assert json_ld['@type'] == 'BreadcrumbList'
        assert len(json_ld['itemListElement']) == 3

    def test_custom_overrides(self):
        """Test custom title, description, and canonical overrides."""
        result = generate_meta_tags(
            title='Custom Title',
            description='Custom description',
            canonical='/custom-page'
        )

        assert result['title'] == 'Custom Title'
        assert result['description'] == 'Custom description'
        assert result['canonical'] == '/custom-page'

    def test_custom_overrides_with_base_url(self):
        """Test custom overrides with base URL generate WebSite JSON-LD."""
        result = generate_meta_tags(
            title='Privacy Policy',
            description='Our privacy policy',
            canonical='/privacy-policy',
            base_url='https://example.com/'
        )

        assert 'json_ld' in result
        json_ld = json.loads(result['json_ld'])
        assert json_ld['@type'] == 'WebSite'

    def test_partial_category_info(self):
        """Test with category but no from/to units."""
        result = generate_meta_tags(category='speed')

        assert 'Speed' in result['title']
        assert '/convert/speed' in result['canonical']

    def test_case_handling(self):
        """Test that categories are properly capitalized in titles."""
        result = generate_meta_tags(category='pressure')

        assert 'Pressure' in result['title']

    def test_unit_symbols_uppercase(self):
        """Test that unit symbols are uppercase in titles."""
        result = generate_meta_tags(
            category='length',
            from_unit='km',
            to_unit='mi'
        )

        assert 'KM' in result['title']
        assert 'MI' in result['title']


class TestJsonLdStructure:
    """Tests for JSON-LD structured data."""

    def test_website_schema(self):
        """Test WebSite schema structure."""
        result = generate_meta_tags(base_url='https://anyunit.com/')
        json_ld = json.loads(result['json_ld'])

        assert json_ld['@context'] == 'https://schema.org'
        assert json_ld['@type'] == 'WebSite'
        assert 'name' in json_ld
        assert 'url' in json_ld

    def test_breadcrumb_schema_category(self):
        """Test BreadcrumbList schema for category page."""
        result = generate_meta_tags(category='volume', base_url='https://anyunit.com/')
        json_ld = json.loads(result['json_ld'])

        assert json_ld['@context'] == 'https://schema.org'
        assert json_ld['@type'] == 'BreadcrumbList'

        items = json_ld['itemListElement']
        assert items[0]['@type'] == 'ListItem'
        assert items[0]['position'] == 1
        assert items[0]['name'] == 'Home'

    def test_breadcrumb_schema_conversion(self):
        """Test BreadcrumbList schema for conversion page."""
        result = generate_meta_tags(
            category='energy',
            from_unit='j',
            to_unit='cal',
            base_url='https://anyunit.com/'
        )
        json_ld = json.loads(result['json_ld'])

        items = json_ld['itemListElement']
        assert len(items) == 3
        assert items[2]['position'] == 3
        assert 'J to CAL' in items[2]['name']

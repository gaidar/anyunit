# app/utils/seo.py
import json
from typing import Optional, Dict


def _absolute_url(base_url: str, path: str) -> str:
    base = base_url.rstrip('/')
    if path.startswith('http://') or path.startswith('https://'):
        return path
    return f"{base}{path}"


def _json_ld_home(base_url: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AnyUnit",
        "url": base_url,
    }
    return json.dumps(data)


def _json_ld_category(base_url: str, category: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": base_url
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": f"{category.title()}"
            }
        ]
    }
    return json.dumps(data)


def _json_ld_conversion(base_url: str, category: str, from_unit: str, to_unit: str, canonical_path: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": base_url
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": f"{category.title()}",
                "item": _absolute_url(base_url, f"/convert/{category}")
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{from_unit.upper()} to {to_unit.upper()}",
                "item": _absolute_url(base_url, canonical_path)
            }
        ]
    }
    return json.dumps(data)


def generate_meta_tags(category: Optional[str] = None,
                       from_unit: Optional[str] = None,
                       to_unit: Optional[str] = None,
                       base_url: Optional[str] = None,
                       title: Optional[str] = None,
                       description: Optional[str] = None,
                       canonical: Optional[str] = None) -> Dict[str, str]:
    """Generate meta tags for different pages.

    Args:
        category: optional category slug
        from_unit: optional source unit
        to_unit: optional target unit
        base_url: optional absolute base URL (e.g., request.url_root)
        title: optional custom title override
        description: optional custom description override
        canonical: optional canonical path (begin with '/') or absolute URL
    Returns:
        Dict with title, description, canonical (path), and optional json_ld string
    """
    # If full overrides provided, use them directly
    if title and description and canonical:
        meta = {
            'title': title,
            'description': description,
            'canonical': canonical,
        }
        if base_url and canonical.startswith('/'):
            # Provide basic WebSite JSON-LD for generic pages
            meta['json_ld'] = _json_ld_home(base_url.rstrip('/'))
        return meta

    if category and from_unit and to_unit:
        meta = {
            'title': f"Convert {from_unit.upper()} to {to_unit.upper()} | {category.title()} Converter",
            'description': f"Convert {from_unit.upper()} to {to_unit.upper()} easily with our free online converter. Get instant, accurate {category} conversions.",
            'canonical': f"/convert/{category}/{from_unit}-to-{to_unit}"
        }
        if base_url:
            meta['json_ld'] = _json_ld_conversion(base_url.rstrip('/'), category, from_unit, to_unit, meta['canonical'])
        return meta
    elif category:
        meta = {
            'title': f"{category.title()} Converter | Unit Conversion",
            'description': f"Convert between different {category} units instantly. Free online {category} converter with common conversions and formulas.",
            'canonical': f"/convert/{category}"
        }
        if base_url:
            meta['json_ld'] = _json_ld_category(base_url.rstrip('/'), category)
        return meta
    else:
        meta = {
            'title': "Unit Converter | Convert Any Unit Instantly",
            'description': "Free online unit converter. Convert between different units of measurement including length, weight, temperature, and more.",
            'canonical': "/"
        }
        if base_url:
            meta['json_ld'] = _json_ld_home(base_url.rstrip('/'))
        return meta
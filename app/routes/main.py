# app/routes/main.py
from flask import Blueprint, render_template, request, Response, url_for
from app.utils.unit_converter import UnitManager
from app.utils.seo import generate_meta_tags

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get the complete unit data from UnitManager
    unit_manager = UnitManager()
    categories_data = unit_manager._units_data['categories']
    meta_tags = generate_meta_tags(base_url=request.url_root)
    
    return render_template('pages/index.html',
                         categories=categories_data,
                         meta_tags=meta_tags)

@main_bp.route('/privacy-policy')
def privacy_policy():
    meta_tags = generate_meta_tags(
        base_url=request.url_root,
        title="Privacy Policy | AnyUnit",
        description="Read AnyUnit's privacy policy to learn how we handle your data and cookies.",
        canonical="/privacy-policy"
    )
    return render_template('pages/privacy_policy.html', meta_tags=meta_tags)

@main_bp.route('/robots.txt')
def robots_txt():
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /static/',
        f'Sitemap: {request.url_root.rstrip("/")}/sitemap.xml'
    ]
    return Response("\n".join(lines), mimetype='text/plain')

@main_bp.route('/sitemap.xml')
def sitemap_xml():
    unit_manager = UnitManager()
    base = request.url_root.rstrip('/')

    urls = []
    # Home
    urls.append({
        'loc': f"{base}{url_for('main.index')}",
        'changefreq': 'weekly',
        'priority': '1.0'
    })

    # Utility pages
    urls.append({
        'loc': f"{base}{url_for('markdown.index')}",
        'changefreq': 'monthly',
        'priority': '0.6'
    })
    urls.append({
        'loc': f"{base}{url_for('timezone.index')}",
        'changefreq': 'monthly',
        'priority': '0.5'
    })
    urls.append({
        'loc': f"{base}{url_for('text_files.index')}",
        'changefreq': 'monthly',
        'priority': '0.5'
    })
    # Aviation calculators landing
    try:
        from app.routes.aviation import aviation  # noqa: F401
        urls.append({
            'loc': f"{base}{url_for('aviation.aviation_calculators')}",
            'changefreq': 'monthly',
            'priority': '0.5'
        })
    except Exception:
        pass

    # Categories and popular conversions
    categories = unit_manager._units_data.get('categories', {})
    for cat_id, data in categories.items():
        # Category page
        urls.append({
            'loc': f"{base}{url_for('converter.category', category=cat_id)}",
            'changefreq': 'weekly',
            'priority': '0.8'
        })
        # Popular conversions
        for conv in data.get('popular_conversions', []):
            loc = f"{base}{url_for('converter.convert', category=cat_id, from_unit=conv['from'], to_unit=conv['to'])}"
            urls.append({
                'loc': loc,
                'changefreq': 'monthly',
                'priority': '0.7'
            })

    # Build XML
    items_xml = "".join([
        f"<url><loc>{u['loc']}</loc><changefreq>{u['changefreq']}</changefreq>"
        f"<priority>{u['priority']}</priority></url>" for u in urls
    ])
    xml = f"<?xml version='1.0' encoding='UTF-8'?>" \
          f"<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>{items_xml}</urlset>"
    return Response(xml, mimetype='application/xml')
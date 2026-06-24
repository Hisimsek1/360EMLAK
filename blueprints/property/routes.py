"""
Property Blueprint Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, abort
from core.data_manager import get_data_manager

property_bp = Blueprint('property', __name__, template_folder='../../templates/property')


@property_bp.route('/')
def index():
    """Property listings page with search and filtering."""
    dm = get_data_manager()
    data = dm.read_all()

    all_properties = [p for p in data.get('properties', []) if p.get('status') == 'active']
    categories = data.get('categories', [])
    cities = data.get('cities', [])

    # Collect query params
    q = request.args.get('q', '').strip()
    listing_type = request.args.get('listing_type', '')
    category = request.args.get('category', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    rooms = request.args.get('rooms', '')
    with_tour = request.args.get('with_tour') == 'on'
    sort = request.args.get('sort', 'newest')

    filtered = []
    for prop in all_properties:
        if q:
            searchable = ' '.join([
                prop.get('title', ''),
                prop.get('description', ''),
                prop.get('city', ''),
                prop.get('district', ''),
            ]).lower()
            if q.lower() not in searchable:
                continue
        if listing_type and prop.get('listing_type') != listing_type:
            continue
        if category and prop.get('category') != category:
            continue
        if city and prop.get('city') != city:
            continue
        if min_price is not None and (prop.get('price') or 0) < min_price:
            continue
        if max_price is not None and (prop.get('price') or 0) > max_price:
            continue
        if rooms and prop.get('rooms') != rooms:
            continue
        if with_tour and not prop.get('tour', {}).get('scenes'):
            continue
        filtered.append(prop)

    if sort == 'price_asc':
        filtered.sort(key=lambda p: p.get('price') or 0)
    elif sort == 'price_desc':
        filtered.sort(key=lambda p: p.get('price') or 0, reverse=True)
    else:
        filtered.sort(key=lambda p: p.get('created_at', ''), reverse=True)

    filters = dict(q=q, listing_type=listing_type, category=category, city=city,
                   min_price=min_price, max_price=max_price, rooms=rooms,
                   with_tour=with_tour, sort=sort)

    return render_template(
        'property/list.html',
        properties=filtered,
        categories=categories,
        cities=cities,
        filters=filters,
        total=len(all_properties),
    )


@property_bp.route('/<property_id>')
def detail(property_id):
    """Property detail page — redirect to the full tour/detail view."""
    dm = get_data_manager()
    prop = dm.find_one('properties', lambda p: p.get('id') == property_id)
    if prop is None:
        abort(404)
    return redirect(url_for('tour.view', id=property_id))

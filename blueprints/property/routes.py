"""
Property Blueprint Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, abort
from core.data_manager import get_data_manager

property_bp = Blueprint('property', __name__, template_folder='../../templates/property')


@property_bp.route('/')
def index():
    """Property listings page"""
    dm = get_data_manager()

    all_properties = dm.find_many('properties', lambda p: p.get('status') == 'active')
    all_properties.sort(key=lambda p: p.get('created_at', ''), reverse=True)

    return render_template('property/list.html', properties=all_properties)


@property_bp.route('/<property_id>')
def detail(property_id):
    """Property detail page — redirect to the full tour/detail view."""
    dm = get_data_manager()
    prop = dm.find_one('properties', lambda p: p.get('id') == property_id)
    if prop is None:
        abort(404)
    return redirect(url_for('tour.view', id=property_id))

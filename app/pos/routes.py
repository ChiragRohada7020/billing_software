# app/sales/routes.py
from flask import Blueprint, render_template,request,jsonify
from app import db

pos_bp = Blueprint('pos_bp', __name__)

@pos_bp.route('/', methods=['GET'])
def pos():
    # Fetch products with prices from MongoDB
    products = db.products.find({}, {'name': 1, 'selling_price': 1, 'barcode': 1})
    products_list = list(products)
    return render_template("pos/pos.html", products=products_list)

@pos_bp.route('/search_products', methods=['POST'])
def search_products():
    try:
        search_term = request.json.get('searchTerm', '').lower()
        
        if not search_term:
            return jsonify([])

        products = db.products.find({
            '$or': [
                {'name': {'$regex': search_term, '$options': 'i'}},
                {'barcode': {'$regex': search_term, '$options': 'i'}}
            ]
        }, {'name': 1, 'barcode': 1, 'selling_price': 1}).limit(4)  # Limit to top 4 results
        
        suggestions = [{
            'name': product['name'],
            'barcode': product['barcode'],
            'selling_price': product['selling_price']
        } for product in products]
        
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# app/sales/routes.py
from flask import Blueprint, render_template,request,jsonify
from app import db
from datetime import datetime,timezone
from bson import ObjectId


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
    



@pos_bp.route('/search_customer', methods=['GET'])
def search_customer():
    

    # MongoDB query to find customers by name
    cursor = db.customers.find({})  # Limit to 5 results

    # Convert cursor to list of dictionaries
    suggestions = [{
            'name': name['username'],
            'id':str(name['_id'])
           
        } for name in cursor]
    print(suggestions)
    # Return suggestions as JSON
    return jsonify(suggestions)
    

@pos_bp.route('/save_sale', methods=['POST'])
def save_sale():
    data = request.json

    
    # Get the current date and time

    # Save customer
    if data:

    # Format the date and time as per the desired format
        current_utc_datetime = datetime.now(timezone.utc)

    # Add the formatted datetime to the data
        data['datetime'] = current_utc_datetime

        db.sales.insert_one(data)
        return jsonify({"message": "Sale saved successfully!"})


    # Save sale with date


    return jsonify({"message": "Error"})


@pos_bp.route('/add_customer', methods=['POST'])
def add_customer():
    customers_collection = db['customers']  # Collection to store customers

    data = request.json
    existing_customer = customers_collection.find_one({"mobile": data.get("mobile")})

    if existing_customer:
        return jsonify({"error": "Customer with this mobile number already exists"}), 400


    # Save customer data to MongoDB
    customer_id = customers_collection.insert_one(data).inserted_id

    # Return the inserted customer ID as confirmation
    return jsonify({"customer_id": str(customer_id)}), 200
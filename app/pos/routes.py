# app/sales/routes.py
from flask import Blueprint, render_template,request,jsonify
from app import db
from datetime import datetime
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
    customer_name = request.json.get('customerName', '')
    sale_items = request.json.get('saleItems', [])
    total_amount = request.json.get('totalAmount', 0)
    amount_paid = request.json.get('amountPaid', 0)
    change_due = request.json.get('changeDue', 0)
    discount = request.json.get('discount', 0)
    commission_rate = request.json.get('commissionRate', 0)
    commission_amount = request.json.get('commissionAmount', 0)
    
    # Get the current date and time
    current_date = datetime.now()

    # Save customer
    customer_data = {'name': customer_name}
    db.customers.insert_one(customer_data)

    # Save sale with date
    sale_data = {
        'customer_name': customer_name,
        'sale_items': sale_items,
        'total_amount': total_amount,
        'amount_paid': amount_paid,
        'change_due': change_due,
        'discount': discount,
        'commission_rate': commission_rate,
        'commission_amount': commission_amount,
        'date': current_date  # Add date field
    }
    db.sales.insert_one(sale_data)

    return jsonify({"message": "Sale saved successfully!"})


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
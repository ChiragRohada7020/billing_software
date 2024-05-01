# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db
from bson.json_util import dumps
from datetime import datetime, timezone
from bson import ObjectId



sales_bp = Blueprint('sales', __name__)


# app/sales/routes.py
# app/sales/routes.py

from bson.json_util import dumps


def is_valid_objectid(search_term):
    try:
        ObjectId(search_term)
        return True
    except:
        return False
    


@sales_bp.route('/search_customer', methods=['GET'])
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
    





@sales_bp.route('/search_products', methods=['POST'])
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


@sales_bp.route('/get_sale_details/<sale_id>', methods=['GET'])
def get_sale_details(sale_id):
    try:
        # Fetch sale details from MongoDB based on the provided sale ID
        sale = db.sales.find_one({'_id': ObjectId(sale_id)})
        

        if sale:
            # Prepare the response data
            sale_details = {
                'id': str(sale['_id']),
                'customer_id': sale.get('customer_id', ''),
                'customer_name': sale.get('customer_name', ''),
                'totalAmount': sale.get('totalAmount', ''),
                'payingAmount': sale.get('payingAmount', ''),
                'dueAmount': sale.get('dueAmount', ''),
                'paymentChoice': sale.get('paymentChoice', ''),
                'totalProduct': sale.get('totalProduct', ''),
                'GST': sale.get('GST', ''),
                'discount': sale.get('discount', ''),
                'payment_status': sale.get('payment_status', ''),
                'salesItems': sale.get('salesItems', []),
                'datetime': sale.get('datetime', '')
            }
            return jsonify(sale_details), 200
        else:
            return jsonify({'error': 'Sale not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500






@sales_bp.route('/create_sale/', defaults={'sale_id': None}, methods=['GET', 'POST'])


@sales_bp.route('/create_sale/<sale_id>', methods=['GET','POST'])
def edit_sale(sale_id):

    if request.method=="POST":
            data = request.json

            # Check if data is provided
            if data:
                # Get the sale ID from the data

                # Check if sale ID is provided
                if sale_id:
                    # Update the sale with the provided data
                    # For example, you might update the sale in your database here
                    db.sales.update_one({"_id": ObjectId(sale_id)}, {"$set": data})
                    return jsonify({"message": f"Sale with ID {sale_id} edited successfully!"})
                else:
                    return jsonify({"message": "Sale ID is missing."}), 400
            else:
                return jsonify({"message": "No data provided for editing the sale."}), 400
            

    return render_template("sales/create_sale.html",)  

@sales_bp.route('/search', methods=['get'])
def search_sales():
    try:
        search_term = request.args.get('searchTerm', '').lower()
        print(search_term)
        
        query = {
            '$or': [
                {'customer_name': {'$regex': search_term, '$options': 'i'}}
                # Add more fields to search here if needed
            ]
        }

        if is_valid_objectid(search_term):
            query['$or'].append({'_id': ObjectId(search_term)})

        # Perform the search
        sales = db.sales.find(query).limit(4) # Limit to top 4 results
        
        suggestions = [{
            'customer_name': sale['customer_name'],
            'totalAmount': sale['totalAmount'],
            'customer_id': str(sale['_id']),           
            'payingAmount':sale['payingAmount'],
            'payment_status':sale['payment_status'],
            'dueAmount':sale['dueAmount'],
            'datetime':str(sale['datetime'])


            # Add more fields to return here if needed
        } for sale in sales]
        
        return dumps(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@sales_bp.route('/', methods=['GET'])
def get_sales():
    sales_collection = db.sales
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    customer_name = request.args.get('customer_name')
    due = request.args.get('due')

    # Provide default time and timezone if not present
    start_date_str = start_date_str + " 00:00:00+00:00" if start_date_str else None
    end_date_str = end_date_str + " 23:59:59+00:00" if end_date_str else None

    # Parse date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S%z') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S%z') if end_date_str else None

    # Create a base query
    query = {}

    # Apply filters to the base query
    if start_date:
        query['datetime'] = {'$gte': start_date}
    
    if end_date:
        query['datetime'] = {'$lte': end_date}
    
    if customer_name:
        query['customer_name'] = {'$regex': f'.*{customer_name}.*', '$options': 'i'}
    
    if due:
        query['dueAmount'] = int(due)  # Convert due to integer if necessary

    # Fetch filtered sales records from MongoDB
    sales_data = sales_collection.find(query)

    # Convert MongoDB cursor to JSON

    # Return JSON response
    return render_template("sales/sales.html", sales=sales_data)
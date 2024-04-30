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
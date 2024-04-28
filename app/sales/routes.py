# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db
from bson.json_util import dumps
from datetime import datetime, timezone



sales_bp = Blueprint('sales', __name__)


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
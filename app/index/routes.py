# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from datetime import datetime, timezone



index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def home():
    sales_data = sale_data()
    # number_of_sales = sales_data.get('number_of_sales', 0)  # Using .get() to avoid KeyError
    return render_template("index.html", total_sales_amount=sales_data['total_sales_today'],percentage_change_sales=sales_data['percentage_change'],num_sales_today=sales_data['num_sales_today'],percentage_change_customer=sales_data['percentage_change_customer'])


@index_bp.route('/search_routes', methods=['POST'])
def search_routes():
    search_term = request.json.get('searchTerm', '').lower()

    # Define available routes
    available_routes = [
        {'name': 'Dashboard', 'url': '/dashboard'},
        {'name': 'Admin Panel', 'url': '/admin'},
        {'name': 'Settings', 'url': '/settings'},
        {'name': 'Profile', 'url': '/profile'},
        {'name': 'Create Product', 'url': '/product/create_product'}
    ]

    # Filter routes based on search term
    matched_routes = [route for route in available_routes if search_term in route['name'].lower()]

    return jsonify(matched_routes)

def sale_data():
    # Get the current UTC date and time as a datetime object
    # Get the current UTC date and time as a datetime object
    current_utc_datetime = datetime.now(timezone.utc)
    
    # Calculate the start and end of today in UTC
    start_of_today = datetime(current_utc_datetime.year, current_utc_datetime.month, current_utc_datetime.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_today = datetime(current_utc_datetime.year, current_utc_datetime.month, current_utc_datetime.day, 23, 59, 59, tzinfo=timezone.utc)
    
    # Calculate the start and end of yesterday in UTC
    start_of_yesterday = start_of_today - timedelta(days=1)
    end_of_yesterday = end_of_today - timedelta(days=1)
    
    # Query MongoDB for sales records between start_of_yesterday and end_of_yesterday
    sales_records_yesterday = db.sales.find({
        "datetime": {
            "$gte": start_of_yesterday,
            "$lte": end_of_yesterday
        }
    })
    
    sales_records_yesterday_list=list(sales_records_yesterday)
    
    # Calculate the total sales for yesterday
    total_sales_yesterday = sum([float(sale['totalAmount']) for sale in sales_records_yesterday_list])
    
    # Query MongoDB for sales records between start_of_today and end_of_today
    sales_records_today = db.sales.find({
        "datetime": {
            "$gte": start_of_today,
            "$lte": end_of_today
        }
    })
    sales_records_today_list=list(sales_records_today)

 
    # Calculate the total sales for today
    total_sales_today = sum([float(sale['totalAmount']) for sale in sales_records_today_list])
    
    # Calculate the percentage change compared to yesterday
    if total_sales_yesterday == 0:
        percentage_change = 100  # To avoid division by zero
    else:
        percentage_change = ((total_sales_today - total_sales_yesterday) / total_sales_yesterday) * 100

    print(sales_records_today_list)





    if len(sales_records_yesterday_list) == 0:
        percentage_change_customer = 100  # To avoid division by zero
    else:
        percentage_change_customer = ((len(sales_records_today_list) - len(sales_records_yesterday_list)) / len(sales_records_yesterday_list)) * 100
    
    return {
        "total_sales_yesterday": int(total_sales_yesterday),
        "total_sales_today": int(total_sales_today),
        "percentage_change": int(percentage_change),
        "num_sales_today": len(sales_records_today_list),
        "percentage_change_customer": int(percentage_change_customer)
    }

# @index_bp.route('/sales', methods=['POST'])
# def add_sale():
#     # Implementation to add a new sale to MongoDB
#     pass

# Implement other routes for updating and deleting sales as needed

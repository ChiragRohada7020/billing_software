# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from datetime import datetime, timezone



index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def home():
    sales_data = today_sales_sum()
    total_sales_amount = sales_data.get('total_sales_amount', 0)  # Using .get() to avoid KeyError
    number_of_sales = sales_data.get('number_of_sales', 0)  # Using .get() to avoid KeyError
    print(total_sales_amount)
    return render_template("index.html", total_sales_amount=total_sales_amount, number_of_sales=number_of_sales)



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


def today_sales_sum():
    # Get today's date and time
    today_date = datetime.combine(datetime.now().date(), datetime.min.time())
    print(f"Today's date: {today_date}")

    # Convert to UTC datetime for MongoDB query
    utc_today_date = today_date.astimezone(timezone.utc)
    print(f"UTC Today's date: {utc_today_date}")

    # Query for distinct sales made today
    today_sales = db.sales.distinct('total_amount', {
        "date": {"$gte": utc_today_date, "$lt": utc_today_date + timedelta(days=1)}
    })

    # Calculate total sales amount and number of sales
    total_sales_amount = sum(today_sales)
    number_of_sales = len(today_sales)
    print(f"Number of sales for today: {number_of_sales}")

    return {
        "message": "Today's sales sum calculated successfully!",
        "total_sales_amount": total_sales_amount,
        "number_of_sales": number_of_sales
    }
    
    
    

# @index_bp.route('/sales', methods=['POST'])
# def add_sale():
#     # Implementation to add a new sale to MongoDB
#     pass

# Implement other routes for updating and deleting sales as needed

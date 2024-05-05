# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db
from bson.json_util import dumps
from datetime import datetime, timezone
from bson import ObjectId
from bson.json_util import dumps




Users = Blueprint('Users', __name__)



@Users.route('/customers', methods=['GET'])
def customer_data():
    return render_template("people/customer.html")
    




def is_valid_objectid(search_term):
    try:
        ObjectId(search_term)
        return True
    except:
        return False






@Users.route('/edit_customer', methods=['POST'])
def edit_customer():
    print("hello")

    try:
        print("hello")
        data = request.json

        # Fetch customer data from the request
        customer_id = data.get('customer_id')

        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        customer_mobile = data.get('customer_mobile')
        customer_dob = data.get('customer_dob')
        customer_notes = data.get('customer_notes')
        print(customer_name)

        # Update the customer data in the database
        customer_collection = db.customers
        customer_collection.update_one(
            {'_id': ObjectId(customer_id)},
            {'$set': {
                'username': customer_name,
                'email': customer_email,
                'mobile': customer_mobile,
                'dob': customer_dob,
                'notes': customer_notes
            }}
        )

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})




@Users.route('/customer_data', methods=['get'])
def search_sales():
    customer_collection = db.customers
    try:
        search_term = request.args.get('searchTerm', '').lower()
        print(search_term)
        
        query = {
            '$or': [
                {'username': {'$regex': search_term, '$options': 'i'}}
                # Add more fields to search here if needed
            ]
        }

        if is_valid_objectid(search_term):
            query['$or'].append({'_id': ObjectId(search_term)})

        # Perform the search
        Customers_Data = customer_collection.find(query)
        print(Customers_Data) # Limit to top 4 results
        
        suggestions = [{
            'customer_name': Customer_Data['username'],
            'customer_email': Customer_Data['email'],
            'customer_id': str(Customer_Data['_id']),           
            'customer_mobile':Customer_Data['mobile'],
            'customer_dob':Customer_Data['dob'],
            'customer_notes':Customer_Data['notes'],
            # 'datetime':str(sale['datetime'])


            # Add more fields to return here if needed
        } for Customer_Data in Customers_Data]
        
        return dumps(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500




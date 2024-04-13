# app/sales/routes.py
from flask import Blueprint, jsonify, request,render_template
from app import db

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")


    
    
    

# @index_bp.route('/sales', methods=['POST'])
# def add_sale():
#     # Implementation to add a new sale to MongoDB
#     pass

# Implement other routes for updating and deleting sales as needed

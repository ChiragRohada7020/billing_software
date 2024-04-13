# app/sales/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app import db

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        category = request.form.get('category')
        otherCategoryInput = request.form.get('otherCategoryInput')
        brand = request.form.get('brand')
        otherBrandInput = request.form.get('otherBrandInput')  # New brand input field
        gst = request.form.get('gst')
        barcode = request.form.get('barcode')
        cost = request.form.get('cost')
        selling_price = request.form.get('selling_price')

        # Check and add new category
        if category == 'other' and otherCategoryInput:
            category = otherCategoryInput
            db.categories.insert_one({'name': category})

        # Check and add new brand
        if brand == 'other' and otherBrandInput:
            brand = otherBrandInput
            db.brands.insert_one({'name': brand})

        # Insert product data into MongoDB
        db.products.insert_one({
            'name': name,
            'category': category,
            'brand': brand,
            'gst': gst,
            'barcode': barcode,
            'cost': cost,
            'selling_price': selling_price
        })

        # Redirect to product listing or home page
        return redirect(url_for('index.home'))
    categories = [category['name'] for category in db.categories.find()]
    brands = [brand['name'] for brand in db.brands.find()]

    # Render product creation form
    return render_template("product/create_product/product.html",categories=categories, brands=brands)

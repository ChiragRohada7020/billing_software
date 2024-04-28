# app/sales/routes.py
from flask import Blueprint, render_template, request, redirect, url_for,flash
from app import db
from bson import ObjectId
from flask import jsonify


product_bp = Blueprint('product_bp', __name__)



@product_bp.route('/search_product', methods=['GET'])
def search_product():
    query = request.args.get('query', '').lower().strip()

    # Fetch all products from MongoDB
    products = list(db.products.find())

    # Filter products based on the query
    filtered_products = [{
        'name': product['name'],
        'barcode': product['barcode'],
        'brand': product['brand'],
        'category': product['category'],
        'cost': product['cost'],
        'selling_price': product['selling_price'],
        'id': str(product['_id'])
    } for product in products if 
        (product['name'] and query in product['name'].lower()) or  # Check if name exists and matches query
        (product['barcode'] and query in product['barcode'].lower()) or  # Check if barcode exists and matches query
        (product['brand'] and query in product['brand'].lower()) or  # Check if brand exists and matches query
        (product['category'] and query in product['category'].lower())]  # Check if category exists and matches query

    # Return filtered products as JSON
    print(filtered_products)
    return jsonify(filtered_products)


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




@product_bp.route('/products', methods=['GET'])
def list_products():
    # Fetch all products from MongoDB
    products = list(db.products.find())
    
    return render_template('product/all_product/all_product.html', products=products)

@product_bp.route('/delete_product/<string:product_id>', methods=['get'])
def delete_product(product_id):
    try:
        # Convert product_id to ObjectId
        obj_id = ObjectId(product_id)

        # Delete the product from MongoDB
        db.products.delete_one({'_id': obj_id})

        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')

    return redirect(url_for('product_bp.list_products'))



@product_bp.route('/edit/<string:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Fetch product from MongoDB by product_id
    product = db.products.find_one({'_id': ObjectId(product_id)})
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('product_bp.list_products'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        category = request.form.get('category')
        otherCategoryInput = request.form.get('otherCategoryInput')
        brand = request.form.get('brand')
        otherBrandInput = request.form.get('otherBrandInput')
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

        # Update product data into MongoDB
        db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {
                'name': name,
                'category': category,
                'brand': brand,
                'gst': gst,
                'barcode': barcode,
                'cost': cost,
                'selling_price': selling_price
            }}
        )

        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_bp.list_products'))

    categories = [category['name'] for category in db.categories.find()]
    brands = [brand['name'] for brand in db.brands.find()]

    # Render product edit form
    return render_template('product/all_product/edit.html', product=product, categories=categories, brands=brands)
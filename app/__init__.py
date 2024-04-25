# app/__init__.py
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['billing']
app.config['SECRET_KEY'] = 'your_secret_key_here'


from app.sales.routes import sales_bp
from app.index.routes import index_bp

# from app.purchase.routes import purchase_bp
from app.product.routes import product_bp
from app.pos.routes import pos_bp

# from app.parties.routes import parties_bp
# from app.expenses.routes import expenses_bp
# from app.reports.routes import reports_bp

app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(index_bp, url_prefix='/')

# app.register_blueprint(purchase_bp, url_prefix='/purchase')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(pos_bp, url_prefix='/pos')

# app.register_blueprint(parties_bp, url_prefix='/parties')
# app.register_blueprint(expenses_bp, url_prefix='/expenses')
# app.register_blueprint(reports_bp, url_prefix='/reports')

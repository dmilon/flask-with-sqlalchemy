from flask import Flask, request, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
from schemas import product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

# CREATE
@app.route('/products', methods=['POST'])
def create_product():
    if "name" in request.get_json():
        name = request.get_json()["name"]
        product = Product()
        product.name = name
        db.session.add(product)
        db.session.commit()
        return (product_schema.jsonify(product), 201)
    else:
        return ('', 400)

# READ ALL
@app.route('/products')
def read_products():
    products = db.session.query(Product).all()
    return (products_schema.jsonify(products), 200)

# READ ONE
@app.route('/products/<int:id>')
def read_product(id):
    product = db.session.query(Product).get(id)
    if product:
        return (product_schema.jsonify(product), 200)
    else:
        return ('', 404)

# UPDATE
@app.route('/products/<int:id>', methods=["PUT", "PATCH"])
def update_product(id):
    product = db.session.query(Product).get(id)
    if product and "name" in request.get_json():
        name = request.get_json()["name"]
        product.name = name
        db.session.commit()
        return ('', 204)
    else:
        return ('', 422)

# DELETE
@app.route('/products/<int:id>', methods=["DELETE"])
def delete_product(id):
    product = db.session.query(Product).get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)






from myapp import app, db
from flask import request, jsonify
from myapp.models.products import Products
from flask_jwt_extended import jwt_required


@app.route('/insert_product', methods=['POST'])
@jwt_required()
def insert_product_view():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify(error="Product name and price are required"), 400

    new_product = Products(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify(msg="Product inserted successfully"), 201


@app.route('/get_one_product/<int:id>', methods=['GET'])
@jwt_required()
def get_one_product(id):
    product = Products.query.get(id)
    if not product:
        return jsonify(error="Product not found"), 404

    return jsonify(
        id=product.id,
        name=product.name,
        price=product.price
    ), 200


@app.route('/update_product/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    data = request.get_json()
    if not data:
        return jsonify(error="Missing data"), 400

    product = Products.query.get(id)
    if not product:
        return jsonify(error="Product not found"), 404

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()
    return jsonify(msg="Product updated successfully"), 200


@app.route('/delete_product/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Products.query.get(id)
    if not product:
        return jsonify(error="Product not found"), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify(msg="Product deleted successfully"), 200

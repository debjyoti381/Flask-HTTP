from myapp import app, db
from flask import request, jsonify
from myapp.models.products import Products
from flask_jwt_extended import jwt_required


@app.route('/insert_product', methods=['POST'])
@jwt_required()
def insert_product_view():
    if request.method == "POST":
        data = request.get_json()
        if data:
            user = Products(name=data['name'], price=data['price'])
            db.session.add(user)
            db.session.commit()
            return jsonify(msg="Product inserted successfully")
        return jsonify(msg="Provide valid credentials")
    return jsonify(msg="Provide valid method")
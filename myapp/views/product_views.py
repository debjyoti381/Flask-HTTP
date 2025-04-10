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

@app.route('/get_one_data/<id>', methods=['GET'])
@jwt_required()
def get_one_views(id):
    if request.method == "GET":
        data = Products.query.get(id)
        print(data)
        return jsonify(msg=f"id = {data.id}, name = {data.name}, price = {data.price}"), 200
    return jsonify(error="Please provide a valid method"), 405

@app.route("/update/<id>", methods=["PUT"])
@jwt_required()
def update_views(id):
    if request.method == "PUT":
        data = request.get_json()
        if data:
            prod = Products.query.get(id)
            if prod:
                prod.name = data['name']
                prod.price = data['price']
                db.session.commit()
                return jsonify(msg="product update successfully"), 201
            return jsonify(error="product is not available"), 400
        return jsonify(error="provide valid credentials"), 401
    return jsonify(error="provide proper method"), 405

@app.route("/delete/<id>",methods=['DELETE'])
@jwt_required()
def delete_product(id):
    if request.method=="DELETE":
        data = Products.query.get(id)
        if data:
            db.session.delete(data)
            db.session.commit()
            return jsonify(msg="Data deleted successfully"), 200
        return jsonify(error="data not found"), 404
    return jsonify(error="provide a valid method"), 405
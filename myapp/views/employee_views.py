from myapp import app, db
from flask import request, jsonify
from myapp.models.employee_models import Employee


# POST-Insert the data To database
@app.route('/insert_data', methods=['POST'])
def insert_emp_views():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            name = data['name']
            email = data['email']
            password = data['password']
            print(name, email,password)
            if name is not None and email is not None and password is not None:
                user = Employee.query.filter_by(email=email).first()
                if user:
                    return jsonify(msg=f"User with email id {user.email} is already exist"), 200
                user1 = Employee(name=name,email=email)
                user1.generate_password(password)
                db.session.add(user1)
                db.session.commit()
                return jsonify(msg=f"User with email {user1.email} insert successfully"), 201
        return jsonify(error="Please provide proper credentials"), 400
    return jsonify(error="Method not found"), 405
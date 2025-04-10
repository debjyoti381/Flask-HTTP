from myapp import app, db
from flask import request, jsonify
from myapp.models.employee_models import Employee
from flask_jwt_extended import create_access_token


@app.route('/')
def index():
    return app.send_static_file('index.html')


# POST - Register a new employee
@app.route('/insert_data', methods=['POST'])
def insert_emp_views():
    data = request.get_json()
    if not data:
        return jsonify(error="Missing JSON data"), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify(error="All fields (name, email, password) are required"), 400

    existing_user = Employee.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(msg=f"User with email {email} already exists"), 200

    new_user = Employee(name=name, email=email)
    new_user.set_password(password)  # renamed from generate_password

    db.session.add(new_user)
    db.session.commit()

    return jsonify(msg=f"User with email {email} inserted successfully"), 201


# POST - Login
@app.route('/login', methods=['POST'])
def login_emp_data():
    data = request.get_json()
    if not data:
        return jsonify(error="Missing JSON data"), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify(error="Email and password are required"), 400

    user = Employee.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.name)
        return jsonify(access_token=access_token), 200

    return jsonify(error="Invalid email or password"), 401

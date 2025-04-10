from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    user_password = db.Column(db.String(50), nullable = False)

    def generate_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.user_password,password)
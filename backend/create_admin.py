import os
from werkzeug.security import generate_password_hash
from models import db, Admin
from app import app 

def create_admin(username, password):
    with app.app_context():
        existing_admin = Admin.query.filter_by(UserName=username).first()
        if existing_admin:
            print(f"Admin with username '{username}' already exists.")
            return

        hashed_password = generate_password_hash(password)
        new_admin = Admin(UserName=username, Password=hashed_password)
        
        db.session.add(new_admin)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully.")

if __name__ == '__main__':
    username = input("Enter username for new admin: ")
    password = input("Enter password for new admin: ")
    create_admin(username, password)

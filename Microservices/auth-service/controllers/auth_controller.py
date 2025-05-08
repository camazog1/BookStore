from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_login import logout_user, login_required
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

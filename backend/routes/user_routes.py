from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password_hash'):
        return jsonify({"error": "Missing required fields: name, email, password_hash"}), 400
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=data['password_hash'],
        phone=data.get('phone'),
        address=data.get('address'),
        license_number=data.get('license_number'),
        license_expiry=data.get('license_expiry'),
        motocycle_model=data.get('motocycle_model'),
        motocycle_year=data.get('motocycle_year'),
        subscription_plan_id=data.get('subscription_plan_id'),
        subscription_start=data.get('subscription_start'),
        is_active=data.get('is_active', True),
        role=data.get('role', 'user')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id, "name": user.name, "email": user.email, "phone": user.phone,
        "address": user.address, "license_number": user.license_number,
        "license_expiry": str(user.license_expiry) if user.license_expiry else None,
        "motocycle_model": user.motocycle_model, "motocycle_year": user.motocycle_year,
        "subscription_plan_id": user.subscription_plan_id,
        "subscription_start": str(user.subscription_start) if user.subscription_start else None,
        "is_active": user.is_active, "role": user.role,
        "created_at": str(user.created_at), "updated_at": str(user.updated_at)
    } for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id, "name": user.name, "email": user.email, "phone": user.phone,
        "address": user.address, "license_number": user.license_number,
        "license_expiry": str(user.license_expiry) if user.license_expiry else None,
        "motocycle_model": user.motocycle_model, "motocycle_year": user.motocycle_year,
        "subscription_plan_id": user.subscription_plan_id,
        "subscription_start": str(user.subscription_start) if user.subscription_start else None,
        "is_active": user.is_active, "role": user.role,
        "created_at": str(user.created_at), "updated_at": str(user.updated_at)
    })

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    user.license_number = data.get('license_number', user.license_number)
    user.license_expiry = data.get('license_expiry', user.license_expiry)
    user.motocycle_model = data.get('motocycle_model', user.motocycle_model)
    user.motocycle_year = data.get('motocycle_year', user.motocycle_year)
    user.subscription_plan_id = data.get('subscription_plan_id', user.subscription_plan_id)
    user.subscription_start = data.get('subscription_start', user.subscription_start)
    user.is_active = data.get('is_active', user.is_active)
    user.role = data.get('role', user.role)
    if data.get('password_hash'):
        user.password_hash = data.get('password_hash')

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
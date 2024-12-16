from flask import Blueprint, request, jsonify
from backend.models import db, User, Task, TaskModel
from ..auth import role_required
from backend.models.user import UserModel  # Import UserModel from user.py

auth_bp = Blueprint('auth', __name__)

# Controller for user registration
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

# New routes with role_required

@auth_bp.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user_model = UserModel(db)  # Initialize UserModel with the database
    user = user_model.find_by_email(data['email'])
    
    if user and user_model.check_password(data['email'], data['password']):
        return jsonify({"success": True, "user": {"email": user['email'], "role": user.get('role', 'User')}}), 200
    return jsonify({"success": False, "message": "Invalid email or password"}), 401
@auth_bp.route('/tasks', methods=['POST'])
@role_required('can_create_tasks')
def create_task_role_required():
    data = request.json  # Retrieve the JSON data from the request
    department_id = data.get('department_id')
    title = data.get('title')
    status = data.get('status', 'Pending')
    description = data.get('description', '')

    task_model.create_task(department_id, title, status, description)
    return jsonify({'message': 'Task created successfully!'}), 201

@auth_bp.route('/tasks/approve/<task_id>', methods=['POST'])
@role_required('can_approve_tasks')
def approve_task(task_id):
    # Logic to approve a task
    return jsonify({"message": "Task approved successfully"}), 200

@auth_bp.route('/users', methods=['GET'])
@role_required('can_manage_users')
def manage_users():
    # Logic to manage users
    return jsonify({"message": "User management access granted"}), 200

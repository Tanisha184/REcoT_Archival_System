from flask import Blueprint, request, jsonify
from models import db, User, Task
from ..auth import role_required  # Import role_required from auth.py

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
@app.route('/tasks', methods=['POST'])
@role_required('can_create_tasks')
def create_task_role_required():
    # Logic to create a task
    return jsonify({"message": "Task created successfully"}), 201

@app.route('/tasks/approve/<task_id>', methods=['POST'])
@role_required('can_approve_tasks')
def approve_task(task_id):
    # Logic to approve a task
    return jsonify({"message": "Task approved successfully"}), 200

@app.route('/users', methods=['GET'])
@role_required('can_manage_users')
def manage_users():
    # Logic to manage users
    return jsonify({"message": "User management access granted"}), 200

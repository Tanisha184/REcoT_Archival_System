from flask import Blueprint, request, jsonify
from models import db, User, Task

auth_bp = Blueprint('auth', __name__)

# Controller for user registration
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

# Controller for creating tasks
@auth_bp.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully"}), 201

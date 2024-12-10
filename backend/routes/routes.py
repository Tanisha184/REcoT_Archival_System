from flask import Blueprint, request, jsonify
from models import db, User, Task
from utils import authorize
auth_bp = Blueprint('auth', __name__)
from models.user import MongoDB, UserModel, DepartmentModel,TaskModel



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
@authorize(role_required=['admin', 'superuser'], department_check=True)
def create_task():
    data = request.get_json()
    department_id = data['department_id']
    title = data['title']
    status = data.get('status', 'pending')

    TaskModel(db).create_task(department_id, title, status)
    return jsonify({"message": "Task created successfully"}), 201

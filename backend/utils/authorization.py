from functools import wraps
from flask import request, jsonify
from models.user import UserModel  # Import your UserModel
from models import db
from models.user import MongoDB, UserModel, DepartmentModel,TaskModel



# Assuming `db` is initialized elsewhere in your app
def authorize(role_required=None, department_check=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            email = request.headers.get('email')  # Assume email is in headers
            user = UserModel(db).get_user_by_email(email)  # Use UserModel to fetch user
            
            if not user:
                return jsonify({"message": "Unauthorized"}), 403
            
            if role_required and user['role'] not in role_required:
                return jsonify({"message": "Forbidden"}), 403

            if department_check:
                department_id = kwargs.get('department_id')
                if user['role'] == 'user' and user.get('department') != department_id:
                    return jsonify({"message": "Access denied to this department"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

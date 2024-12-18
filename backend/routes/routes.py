from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import db, User, Task, TaskModel
from ..auth import role_required
from backend.models.user import UserModel
from backend.models.archive import ArchiveModel
from backend.models.report_template import ReportTemplateModel

auth_bp = Blueprint('auth', __name__)

# Initialize models
archive_model = ArchiveModel(db)
report_template_model = ReportTemplateModel(db)

# Controller for user registration
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

# New routes with role_required

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user_model = UserModel(db)  # Initialize UserModel with the database
    user = user_model.find_by_email(data['email'])
    
    if user and user_model.check_password(data['email'], data['password']):
        return jsonify({"success": True, "user": {"email": user['email'], "role": user.get('role', 'User')}}), 200
    return jsonify({"success": False, "message": "Invalid email or password"}), 401
# Query Management Routes
@auth_bp.route('/tasks/search', methods=['POST'])
@role_required('can_view_tasks')
def search_tasks():
    """
    Search and filter tasks based on multiple criteria
    Expected JSON body:
    {
        "department_id": "optional",
        "title": "optional search text",
        "status": "optional status",
        "start_date": "optional ISO date",
        "end_date": "optional ISO date"
    }
    """
    filters = request.json
    
    # Convert date strings to datetime objects if present
    if 'start_date' in filters:
        filters['start_date'] = datetime.fromisoformat(filters['start_date'])
    if 'end_date' in filters:
        filters['end_date'] = datetime.fromisoformat(filters['end_date'])
    
    # Get user's role and department
    user = UserModel(db).find_by_email(request.user['email'])
    is_admin = 'admin' in user.get('roles', [])
    
    # If not admin, restrict to user's department
    if not is_admin:
        filters['department_id'] = user['department_id']
    
    tasks = TaskModel(db).search_tasks(filters)
    return jsonify({'tasks': tasks}), 200

# Archive Management Routes
@auth_bp.route('/tasks/archive/<task_id>', methods=['POST'])
@role_required('can_archive_tasks')
def archive_task(task_id):
    """Archive a completed task"""
    try:
        archive_model.archive_task(task_id, request.user['email'])
        return jsonify({'message': 'Task archived successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to archive task'}), 500

@auth_bp.route('/archives/search', methods=['POST'])
@role_required('can_view_archives')
def search_archives():
    """Search archived tasks with filters"""
    filters = request.json
    archives = archive_model.search_archives(filters)
    return jsonify({'archives': archives}), 200

# Report Template Routes
@auth_bp.route('/report-templates', methods=['POST'])
@role_required('can_manage_templates')
def create_template():
    """Create a new report template"""
    data = request.json
    template = report_template_model.create_template(
        name=data['name'],
        template_type=data['template_type'],
        fields=data['fields'],
        layout=data['layout']
    )
    return jsonify({'message': 'Template created successfully', 'template_id': str(template.inserted_id)}), 201

@auth_bp.route('/report-templates', methods=['GET'])
@role_required('can_view_templates')
def get_templates():
    """Get all report templates"""
    templates = report_template_model.get_all_templates()
    return jsonify({'templates': templates}), 200

@auth_bp.route('/reports/generate', methods=['POST'])
@role_required('can_generate_reports')
def generate_report():
    """
    Generate a report based on filtered data and template
    Expected JSON body:
    {
        "template_name": "template_name",
        "filters": {
            // task filters
        }
    }
    """
    data = request.json
    template = report_template_model.get_template_by_name(data['template_name'])
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    # Get filtered tasks
    tasks = TaskModel(db).search_tasks(data['filters'])
    
    # Generate report based on template and data
    report = {
        'template': template['name'],
        'generated_at': datetime.now().isoformat(),
        'data': tasks,
        'layout': template['layout']
    }
    
    return jsonify({'report': report}), 200

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

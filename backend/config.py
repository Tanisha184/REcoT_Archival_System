from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from backend.models import MongoDB, UserModel, DepartmentModel, TaskModel
from backend.models.report_template import ReportTemplateModel
from backend.models.archive import ArchiveModel
from bson import ObjectId
from backend.tasks_data import tasks_data
from backend.routes.routes import auth_bp  # Import the auth_bp blueprint

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# Initialize database and models
db = MongoDB(uri="mongodb://localhost:27017/", db_name="archival_471")
user_model = UserModel(db)
department_model = DepartmentModel(db)
task_model = TaskModel(db)
report_template_model = ReportTemplateModel(db)
archive_model = ArchiveModel(db)

# Create a default user if it does not exist
def create_default_user():
    default_user = user_model.find_by_email("admin@example.com")
    if not default_user:
        user_model.create_user(
            "Admin User", 
            "admin@example.com", 
            "password", 
            roles=['admin', 'user']
        )

create_default_user()

# Register the auth_bp blueprint with the correct prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/login', methods=['GET'])
def serve_login():
    return app.send_static_file('index.html')

@app.route('/register', methods=['GET'])
def serve_register():
    return app.send_static_file('index.html')

@app.route('/dashboard', methods=['GET'])
def serve_dashboard():
    return app.send_static_file('index.html')

departments = [
    {"id": 1, "name": "Computer Science", "description": "Explore programming, AI, and software development."},
    {"id": 2, "name": "Electrical Engineering", "description": "Focus on circuits, electronics, and energy systems."},
    {"id": 3, "name": "Mechanical Engineering", "description": "Learn about machines, design, and thermodynamics."},
    {"id": 4, "name": "Business Administration", "description": "Study finance, marketing, and management."},
]

@app.route('/api/departments', methods=['GET'])
def get_departments():
    return jsonify(departments)

@app.route('/api/departments', methods=['GET', 'POST'])
def handle_departments():
    if request.method == 'GET':
        departments = department_model.get_all_departments()
        for dept in departments:
            dept['_id'] = str(dept['_id'])  # Convert ObjectId to string
        return jsonify(departments)
    
    if request.method == 'POST':
        data = request.get_json()
        department_model.create_department(data['name'], data['description'])
        return jsonify({'message': 'Department created successfully'}), 201

@app.route('/api/departments/<string:department_id>', methods=['PUT', 'DELETE'])
def update_delete_department(department_id):
    if request.method == 'PUT':
        data = request.get_json()
        department_model.update_department(ObjectId(department_id), data)
        return jsonify({'message': 'Department updated successfully'})

    if request.method == 'DELETE':
        department_model.delete_department(ObjectId(department_id))
        return jsonify({'message': 'Department deleted successfully'})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_model.create_task(
        data['department_id'], 
        data['title'], 
        data.get('status', 'Not Started'),
        data.get('description', '')
    )
    return jsonify({'message': 'Task created successfully'}), 201

# Query Management Routes
@app.route('/api/tasks/search', methods=['POST'])
def search_tasks():
    filters = request.get_json()
    tasks = task_model.search_tasks(filters)
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify({'tasks': tasks})

# Archive Management Routes
@app.route('/api/tasks/archive/<task_id>', methods=['POST'])
def archive_task(task_id):
    try:
        archive_model.archive_task(ObjectId(task_id), request.user['email'])
        return jsonify({'message': 'Task archived successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/archives/search', methods=['POST'])
def search_archives():
    filters = request.get_json()
    archives = archive_model.search_archives(filters)
    for archive in archives:
        archive['_id'] = str(archive['_id'])
    return jsonify({'archives': archives})

# Report Template Routes
@app.route('/api/report-templates', methods=['GET', 'POST'])
def handle_report_templates():
    if request.method == 'GET':
        templates = report_template_model.get_all_templates()
        for template in templates:
            template['_id'] = str(template['_id'])
        return jsonify({'templates': templates})
    
    if request.method == 'POST':
        data = request.get_json()
        template = report_template_model.create_template(
            name=data['name'],
            template_type=data['template_type'],
            fields=data['fields'],
            layout=data['layout']
        )
        return jsonify({
            'message': 'Template created successfully',
            'template_id': str(template.inserted_id)
        }), 201

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    data = request.get_json()
    template = report_template_model.get_template_by_name(data['template_name'])
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    tasks = task_model.search_tasks(data['filters'])
    for task in tasks:
        task['_id'] = str(task['_id'])
    
    report = {
        'template': template['name'],
        'generated_at': datetime.now().isoformat(),
        'data': tasks,
        'layout': template['layout']
    }
    
    return jsonify({'report': report}), 200

@app.route('/api/departments/<string:department_id>/tasks', methods=['GET'])
def get_tasks_for_department(department_id):
    tasks = task_model.get_tasks_by_department(department_id)
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
    return jsonify(tasks)

@app.route('/')
def index():
    return "Welcome to the REcoT Archival System API!"

if __name__ == "__main__":
    app.run(debug=True)

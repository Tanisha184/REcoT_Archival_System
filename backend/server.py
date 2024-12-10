from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from backend.models import MongoDB, UserModel, DepartmentModel, TaskModel
from bson import ObjectId
from backend.tasks_data import tasks_data
from .routes.routes import auth_bp  # Import the auth_bp blueprint

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# Initialize database and user model
db = MongoDB(uri="mongodb://localhost:27017/", db_name="archival_471")
user_model = UserModel(db)
department_model = DepartmentModel(db)
task_model = TaskModel(db)

# Create a default user if it does not exist
def create_default_user():
    default_user = user_model.find_by_email("admin@example.com")
    if not default_user:
        user_model.create_user("Admin User", "admin@example.com", "password")

create_default_user()

# Register the auth_bp blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('fullName')
    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    if user_model.find_by_email(email):
        return jsonify({'success': False, 'message': 'User already exists'})

    # Register the user
    user_model.create_user(full_name, email, password)
    response = {'success': True, 'message': 'Registration successful'}
    print("Response:", response)  # Log the response for debugging
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Verify user credentials
    user = user_model.find_by_email(email)
    if user and user_model.check_password(email, password):
        user_data = {
            'id': str(user['_id']),
            'fullName': user['full_name'],
            'email': user['email'],
            'role': user['role']
        }
        return jsonify({'success': True, 'user': user_data})
    
    return jsonify({'success': False, 'message': 'Invalid email or password'})

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
    task_model.create_task(data['department_id'], data['title'], data['status'])
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/api/departments/<string:department_id>/tasks', methods=['GET'])
def get_tasks_for_department(department_id):
    tasks = task_model.get_tasks_by_department(department_id)
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
    return jsonify(tasks)

@app.route('/api/departments/<department>/tasks', methods=['GET'])
def get_department_tasks(department):
    if department in tasks_data:
        return jsonify({"tasks": tasks_data[department]})
    else:
        return jsonify({"tasks": []}), 404

@app.route('/')
def index():
    return "Welcome to the REcoT Archival System API!"

if __name__ == "__main__":
    app.run(debug=True)

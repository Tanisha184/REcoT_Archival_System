from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from bson import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# MongoDB Setup
class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="archival_471"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Models
class UserModel:
    def __init__(self, db):
        self.collection = db.get_collection("users")

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def create_user(self, full_name, email, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.collection.insert_one({
            "full_name": full_name,
            "email": email,
            "password": hashed_password
        })

    def check_password(self, email, password):
        user = self.find_by_email(email)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return True
        return False

class DepartmentModel:
    def __init__(self, db):
        self.collection = db.get_collection("departments")  # Assuming you have a "departments" collection

    def find_by_id(self, department_id):
        return self.collection.find_one({"_id": ObjectId(department_id)})

    def create_department(self, name, description):
        self.collection.insert_one({
            "name": name,
            "description": description
        })

# Initialize MongoDB and models
db = MongoDB()
user_model = UserModel(db)
department_model = DepartmentModel(db)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Archival API!"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")

    if user_model.find_by_email(email):
        return jsonify({"success": False, "message": "User already exists"}), 400

    user_model.create_user(full_name, email, password)
    return jsonify({"success": True, "message": "Registration successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if user_model.check_password(email, password):
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route("/api/dashboard-stats", methods=["GET"])
def dashboard_stats():
    stats = {
        "total_users": db.get_collection("users").count_documents({}),
        "total_tasks": db.get_collection("tasks").count_documents({}),
    }
    return jsonify({"status": "success", "data": stats})
@app.route('/api/departments', methods=['GET'])
def get_all_departments():
    departments = department_model.collection.find()  # Get all departments
    departments_list = []
    for department in departments:
        departments_list.append({
            'id': str(department['_id']),
            'name': department.get('name'),
            'description': department.get('description')
        })
    return jsonify(departments_list)

@app.route('/api/departments/<string:department_id>', methods=['GET'])
def get_department(department_id):
    department = department_model.find_by_id(department_id)

    if department:
        return jsonify({
            'id': str(department['_id']),
            'name': department.get('name'),
            'description': department.get('description')
        })
    return jsonify({"success": False, "message": "Department not found"}), 404
@app.route('/api/departments/<string:department_name>/tasks', methods=['GET'])
def get_department_tasks(department_name):
    # Logic to fetch tasks for the department by its name
    tasks = db.get_collection('tasks').find({"department_name": department_name})
    task_list = [{"title": task["title"], "status": task["status"]} for task in tasks]
    return jsonify({"tasks": task_list})
@app.route('/api/departments', methods=['POST'])
def add_department():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if name and description:
        department_model.create_department(name, description)
        return jsonify({"message": "Department added successfully!"}), 201
    return jsonify({"message": "Missing required fields!"}), 400


if __name__ == "__main__":
    app.run(debug=True)

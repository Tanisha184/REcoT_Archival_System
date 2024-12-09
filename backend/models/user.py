from pymongo import MongoClient
import bcrypt

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="archival_471"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def __getitem__(self, collection_name):
        return self.get_collection(collection_name)


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserModel:
    def __init__(self, db):
        self.collection = db.get_collection('users')

    def find_by_email(self, email):
        """Find a user by their email."""
        return self.collection.find_one({'email': email})

    def create_user(self, full_name, email, password):
        """Create a new user."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.collection.insert_one({
            'full_name': full_name,
            'email': email,
            'password': hashed_password
        })

    def check_password(self, email, password):
        """Check if the provided password matches the stored hash."""
        user = self.find_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return True
        return False




class DepartmentModel:
    def __init__(self, db):
        self.collection = db.get_collection("departments")

    def create_department(self, name, description):
        return self.collection.insert_one({"name": name, "description": description})

    def get_all_departments(self):
        return list(self.collection.find())

    def update_department(self, department_id, updated_data):
        return self.collection.update_one({"_id": department_id}, {"$set": updated_data})

    def delete_department(self, department_id):
        return self.collection.delete_one({"_id": department_id})

class TaskModel:
    def __init__(self, db):
        self.collection = db.get_collection("tasks")

    def create_task(self, department_id, title, status):
        return self.collection.insert_one({"department_id": department_id, "title": title, "status": status})

    def get_tasks_by_department(self, department_id):
        return list(self.collection.find({"department_id": department_id}))

    def update_task(self, task_id, updated_data):
        return self.collection.update_one({"_id": task_id}, {"$set": updated_data})

    def delete_task(self, task_id):
        return self.collection.delete_one({"_id": task_id})
<<<<<<< HEAD
from bson import ObjectId
from pymongo import MongoClient
import bcrypt
=======
from datetime import datetime
from bson import ObjectId
>>>>>>> 6b90a5a00dcd86f68ebde68c19fd0aea2b7a4cbf

class User:
    ROLES = {
        'SUPER_ADMIN': 'super_admin',
        'ADMIN': 'admin',
        'DEPARTMENT_HEAD': 'department_head',
        'FACULTY': 'faculty',
        'STAFF': 'staff'
    }

    DEPARTMENTS = {
        'CSE': 'Computer Science and Engineering',
        'ECE': 'Electronics and Communication Engineering',
        'ME': 'Mechanical Engineering',
        'RESEARCH': 'Research',
        'ADMIN': 'Administration'
    }

    def __init__(self, db):
        self.db = db
        self.collection = db.users

    def create_user(self, data):
        user = {
            'email': data['email'],
            'password': data['password'],  # Should be hashed before storing
            'name': data['name'],
            'department': data['department'],
            'roles': data.get('roles', ['staff']),
            'permissions': self._get_permissions_for_roles(data.get('roles', ['staff'])),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }
        result = self.collection.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user

<<<<<<< HEAD
    def create_user(self, full_name, email, password, role='user', department=None):
        """Create a new user with a role and optionally a department."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.collection.insert_one({
            'full_name': full_name,
            'email': email,
            'password': hashed_password,
            'role': role,  # Add role field
            'department': department  # Add department field (nullable)
        })
    def get_user_by_email(self, email):
        """Retrieve user information including role and department."""
        return self.collection.find_one({'email': email})
=======
    def get_user_by_email(self, email):
        user = self.collection.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
        return user
>>>>>>> 6b90a5a00dcd86f68ebde68c19fd0aea2b7a4cbf

    def get_user_by_id(self, user_id):
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except:
            return None

    def update_user(self, user_id, data):
        data['updated_at'] = datetime.utcnow()
        if 'roles' in data:
            data['permissions'] = self._get_permissions_for_roles(data['roles'])
        
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def get_department_users(self, department):
        users = list(self.collection.find({'department': department}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    def get_users_by_role(self, role):
        users = list(self.collection.find({'roles': role}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users

<<<<<<< HEAD
class DepartmentModel:
    def __init__(self, db):
        self.collection = db.get_collection("departments")
        
    def find_by_id(self, department_id):
        return self.collection.find_one({"_id": ObjectId(department_id)})
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
        """Create a task associated with a department."""
        return self.collection.insert_one({
            "department_id": department_id,
            "title": title,
            "status": status
        })

    def get_tasks_by_department(self, department_id):
        return list(self.collection.find({"department_id": department_id}))

    def update_task(self, task_id, updated_data):
        return self.collection.update_one({"_id": task_id}, {"$set": updated_data})

    def delete_task(self, task_id):
        return self.collection.delete_one({"_id": task_id})
=======
    def _get_permissions_for_roles(self, roles):
        permissions = set()
        
        for role in roles:
            if role == self.ROLES['SUPER_ADMIN']:
                permissions.update([
                    'manage_users', 'manage_roles', 'manage_departments',
                    'create_task', 'edit_task', 'delete_task', 'view_all_tasks',
                    'approve_task', 'generate_reports', 'access_archives',
                    'view_department_tasks', 'view_assigned_tasks'
                ])
            elif role == self.ROLES['ADMIN']:
                permissions.update([
                    'manage_users', 'manage_roles',
                    'create_task', 'edit_task', 'view_all_tasks',
                    'approve_task', 'generate_reports', 'access_archives',
                    'view_department_tasks', 'view_assigned_tasks'
                ])
            elif role == self.ROLES['DEPARTMENT_HEAD']:
                permissions.update([
                    'create_task', 'edit_task', 'view_department_tasks',
                    'approve_task', 'generate_reports', 'generate_department_reports',
                    'view_assigned_tasks'
                ])
            elif role == self.ROLES['FACULTY']:
                permissions.update([
                    'create_task', 'edit_task', 'view_department_tasks',
                    'approve_task', 'generate_reports', 'view_assigned_tasks'
                ])
            elif role == self.ROLES['STAFF']:
                permissions.update([
                    'create_task', 'edit_task', 'view_assigned_tasks',
                    'generate_reports'
                ])
                
        return list(permissions)
>>>>>>> 6b90a5a00dcd86f68ebde68c19fd0aea2b7a4cbf

from pymongo import MongoClient

class DepartmentModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['departments']

    def get_all_departments(self):
        return list(self.collection.find())

    def create_department(self, name, description):
        department = {
            'name': name,
            'description': description
        }
        self.collection.insert_one(department)

    def update_department(self, department_id, data):
        self.collection.update_one({'_id': department_id}, {'$set': data})

    def delete_department(self, department_id):
        self.collection.delete_one({'_id': department_id})

from pymongo import MongoClient

class Task:
    def __init__(self, department_id, title, status):
        self.department_id = department_id
        self.title = title
        self.status = status

class TaskModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['tasks']

    def create_task(self, department_id, title, status):
        task = {
            'department_id': department_id,
            'title': title,
            'status': status
        }
        self.collection.insert_one(task)

    def get_tasks_by_department(self, department_id):
        return list(self.collection.find({'department_id': department_id}))

    def update_task(self, task_id, data):
        self.collection.update_one({'_id': task_id}, {'$set': data})

    def delete_task(self, task_id):
        self.collection.delete_one({'_id': task_id})

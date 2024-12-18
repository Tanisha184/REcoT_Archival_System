from pymongo import MongoClient
from datetime import datetime

class Task:
    def __init__(self, department_id, title, status, description):
        self.department_id = department_id
        self.title = title
        self.status = status
        self.description = description
        self.created_at = datetime.now()

class TaskModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['tasks']

    def create_task(self, department_id, title, status, description):
        task = {
            'department_id': department_id,
            'title': title,
            'status': status,
            'description': description,
            'created_at': datetime.now()
        }
        self.collection.insert_one(task)

    def get_tasks_by_department(self, department_id):
        return list(self.collection.find({'department_id': department_id}))

    def update_task(self, task_id, data):
        self.collection.update_one({'_id': task_id}, {'$set': data})

    def delete_task(self, task_id):
        self.collection.delete_one({'_id': task_id})

    def search_tasks(self, filters):
        """
        Search tasks with multiple filters
        filters: dict containing search criteria like:
        {
            'department_id': 'dept_id',
            'title': 'search_text',
            'status': 'status',
            'start_date': datetime,
            'end_date': datetime
        }
        """
        query = {}
        
        if 'department_id' in filters and filters['department_id']:
            query['department_id'] = filters['department_id']
        
        if 'title' in filters and filters['title']:
            query['title'] = {'$regex': filters['title'], '$options': 'i'}
        
        if 'status' in filters and filters['status']:
            query['status'] = filters['status']
        
        if 'start_date' in filters or 'end_date' in filters:
            date_query = {}
            if 'start_date' in filters:
                date_query['$gte'] = filters['start_date']
            if 'end_date' in filters:
                date_query['$lte'] = filters['end_date']
            query['created_at'] = date_query

        return list(self.collection.find(query))

    def get_task_by_id(self, task_id):
        """Get a single task by its ID"""
        return self.collection.find_one({'_id': task_id})

    def get_tasks_by_status(self, status):
        """Get all tasks with a specific status"""
        return list(self.collection.find({'status': status}))

    def get_tasks_by_date_range(self, start_date, end_date):
        """Get tasks created within a date range"""
        return list(self.collection.find({
            'created_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        }))

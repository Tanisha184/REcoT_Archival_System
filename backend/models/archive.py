from datetime import datetime
from pymongo import MongoClient

class Archive:
    def __init__(self, task_id, department_id, title, description, status, archived_by):
        self.task_id = task_id
        self.department_id = department_id
        self.title = title
        self.description = description
        self.status = status
        self.archived_by = archived_by
        self.archived_at = datetime.now()

class ArchiveModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['archives']
        self.tasks_collection = self.db['tasks']

    def archive_task(self, task_id, archived_by):
        # Get the task from tasks collection
        task = self.tasks_collection.find_one({'_id': task_id})
        if not task:
            raise ValueError("Task not found")

        # Create archive entry
        archive_entry = {
            'task_id': task_id,
            'department_id': task['department_id'],
            'title': task['title'],
            'description': task['description'],
            'status': task['status'],
            'archived_by': archived_by,
            'archived_at': datetime.now(),
            'original_task_data': task  # Store complete original task data
        }

        # Insert into archives
        self.collection.insert_one(archive_entry)
        
        # Update task status in original collection
        self.tasks_collection.update_one(
            {'_id': task_id},
            {'$set': {'status': 'Archived'}}
        )

    def get_department_archives(self, department_id, start_date=None, end_date=None):
        query = {'department_id': department_id}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['archived_at'] = date_query

        return list(self.collection.find(query))

    def search_archives(self, filters):
        """
        Search archives with multiple filters
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
        
        if 'department_id' in filters:
            query['department_id'] = filters['department_id']
        
        if 'title' in filters and filters['title']:
            query['title'] = {'$regex': filters['title'], '$options': 'i'}
        
        if 'status' in filters:
            query['status'] = filters['status']
        
        if 'start_date' or 'end_date' in filters:
            date_query = {}
            if 'start_date' in filters:
                date_query['$gte'] = filters['start_date']
            if 'end_date' in filters:
                date_query['$lte'] = filters['end_date']
            query['archived_at'] = date_query

        return list(self.collection.find(query))

    def get_archive_by_id(self, archive_id):
        return self.collection.find_one({'_id': archive_id})

    def delete_archive(self, archive_id):
        return self.collection.delete_one({'_id': archive_id})

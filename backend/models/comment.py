from datetime import datetime
from bson import ObjectId

class Comment:
    def __init__(self, db):
        self.db = db
        self.collection = db.comments  # Reference to comments collection

    def add_comment(self, task_id, user_id, comment_text):
        comment = {
            'task_id': ObjectId(task_id),
            'user_id': ObjectId(user_id),
            'comment_text': comment_text,
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(comment)
        comment['_id'] = str(result.inserted_id)
        return comment

    def get_comments_by_task_id(self, task_id):
        comments = list(self.collection.find({'task_id': ObjectId(task_id)}))
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['user_id'] = str(comment['user_id'])  # Convert user_id to string
        return comments

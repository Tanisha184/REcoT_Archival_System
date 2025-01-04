from pymongo import MongoClient

# Initialize the MongoDB client
db = MongoClient("mongodb://localhost:27017/").archival_471

from .user import User
from .department import DepartmentModel
from .task import Task

__all__ = ["MongoDB", "UserModel", "User", "DepartmentModel", "TaskModel", "Task", "db"]

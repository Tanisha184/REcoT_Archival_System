import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["archival_471"]

# Verify the connection
print("Connected to MongoDB")

# Check if the collections exist
if "departments" in db.list_collection_names():
    print("Departments collection exists")
else:
    print("Departments collection does not exist")
    # Create the departments collection and insert sample data
    departments = [
        {"name": "Computer Science", "description": "Explore programming, AI, and software development."},
        {"name": "Electrical Engineering", "description": "Focus on circuits, electronics, and energy systems."},
        {"name": "Mechanical Engineering", "description": "Learn about machines, design, and thermodynamics."},
        {"name": "Business Administration", "description": "Study finance, marketing, and management."}
    ]
    db.departments.insert_many(departments)
    print("Departments collection created and populated with sample data")

if "tasks" in db.list_collection_names():
    print("Tasks collection exists")
else:
    print("Tasks collection does not exist")
    # Create the tasks collection and insert sample data
    tasks = [
        {"department_id": "1", "title": "Implement new feature", "status": "In Progress"},
        {"department_id": "2", "title": "Design circuit board", "status": "Not Started"},
        {"department_id": "3", "title": "Analyze machine performance", "status": "Completed"},
        {"department_id": "4", "title": "Prepare financial report", "status": "In Progress"}
    ]
    db.tasks.insert_many(tasks)
    print("Tasks collection created and populated with sample data")

# Check the departments collection
print("\nDepartments:")
for department in db.departments.find():
    print(department)

# Check the tasks collection
print("\nTasks:")
for task in db.tasks.find():
    print(task)

import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

db = None

def get_db():
    return db

def create_app(config_name='default'):
    global db
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize MongoDB connection with error handling
    try:
        print("Attempting to connect to MongoDB...")
        client = MongoClient(app.config['MONGO_URI'])
        # Force a connection to verify it works
        client.server_info()
        db = client.get_default_database()
        app.db = db  # Also attach to app for compatibility
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        raise
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.users import users_bp
    from routes.reports import reports_bp
    
    # Attach db to blueprints
    auth_bp.db = db
    tasks_bp.db = db
    users_bp.db = db
    reports_bp.db = db
    
    app.register_blueprint(auth_bp)  # URL prefix is defined in blueprint
    app.register_blueprint(tasks_bp)  # URL prefix is defined in blueprint
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(reports_bp)  # URL prefix is defined in blueprint
    
    return app

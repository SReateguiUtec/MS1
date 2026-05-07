from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from app.models import db
    db.init_app(app)
    
    CORS(app)
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_m1',
                "route": '/apispec_m1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static_m1",
        "swagger_ui": True,
        "specs_route": "/swagger-ui/m1"
    }
    Swagger(app, config=swagger_config)
    
    with app.app_context():
        db.create_all()
    
    from app.routes import register_routes
    register_routes(app)
    
    return app
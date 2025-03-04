from flask import Flask
from config import Config
from models import db
from routes import app_routes  # Import routes

app = Flask(__name__)
app.config.from_object(Config)  # Load Configurations

db.init_app(app)  # Initialize SQLAlchemy

# Create database tables
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(app_routes)

if __name__ == "__main__":
    app.run(debug=True)

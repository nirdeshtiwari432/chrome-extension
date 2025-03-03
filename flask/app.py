from flask import Flask
from models import db
import secrets
from routes import app_routes  # Import routes

app = Flask(__name__)
app.config.from_object("config.Config")  # Load Configurations
app.register_blueprint(app_routes)  # Register Routes
db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)  # Secure secret key
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:1234@localhost/yourdatabase"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

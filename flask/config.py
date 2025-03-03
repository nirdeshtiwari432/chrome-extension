import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)  # Secure secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

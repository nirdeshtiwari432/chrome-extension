from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = "your_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rank = db.Column(db.String(255), nullable=True)  # "Rank" is a reserved keyword, so avoid using it directly
    domain = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<Test {self.id}, {self.domain}, {self.ip_address}>"

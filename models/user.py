from sqlalchemy import func
from database import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(), default=func.current_timestamp())
    last_modified_at = db.Column(db.DateTime(), default=func.current_timestamp())
    
    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

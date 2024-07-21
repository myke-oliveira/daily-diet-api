from database import db
from sqlalchemy import func
from .user import User
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(180), nullable=False, default="")
    date_time: datetime = db.Column(db.DateTime(), nullable=False)
    on_the_diet = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    last_modifiled_at = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_time": self.date_time.isoformat(),
            "on_the_diet": self.on_the_diet,
        }
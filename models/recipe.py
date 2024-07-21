from database import db

class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(180), nullable=False, default="")
    date_time = db.Column(db.DateTime(), nullable=False)
    on_the_diet = db.Column(db.Boolean(), nullable=False)
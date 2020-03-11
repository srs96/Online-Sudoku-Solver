from app import db

class Puzzles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle = db.Column(db.String(81), index=True, unique=False)
    difficulty = db.Column(db.String(20), index=True, unique=False)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    program = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Record {self.name}>"
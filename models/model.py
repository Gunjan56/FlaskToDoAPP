
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='PENDING')

    def __repr__(self):
        return f'<Todo {self.id} - {self.title}>'
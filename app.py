from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} - {self.title}>'

@app.route('/')
def home():
    todos = Todo.query.all()
    error = None
    success = None
    return render_template('home.html', todos=todos, error=error, success=success)

@app.route('/todos/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    error = None
    success = None
    if not title:
        error = 'Title is required'
    else:
        existing_todo = Todo.query.filter_by(title=title).first()
        if existing_todo:
            error = 'Todo item already exists'

    if error:
        todos = Todo.query.all()
        return render_template('home.html', error=error, todos=todos, success=success)

    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    success = 'Todo added successfully'
    flash(success, 'success')
    return redirect(url_for('home'))

@app.route('/todos/complete/<int:id>', methods=['POST'])
def complete_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.completed= True
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/todos/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

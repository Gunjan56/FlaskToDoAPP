from flask import (Flask, get_flashed_messages, render_template, request, redirect, url_for, flash)
from flask_migrate import Migrate
from models.model import db, Todo

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'gunjan'
    db.init_app(app) 
    migrate = Migrate(app, db)
    return app

def register_routes(app):
    @app.route('/')
    def home():
        todos = Todo.query.all()
        messages = get_flashed_messages(with_categories=True)
        return render_template('home.html', todos=todos, messages=messages)

    @app.route('/todos/add', methods=['POST'])
    def add_todo():
        title = request.form['title']
        description = request.form.get('description')
        error = None

        if not title:
            error = 'Title is required'
        else:
            existing_todo = Todo.query.filter_by(title=title).first()
            if existing_todo:
                error = 'Todo item already exists'

        if error:
            flash(error, 'error')
        else:
            new_todo = Todo(title=title, description=description)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added successfully', 'success')

        return redirect(url_for('home'))

    @app.route('/todos/complete/<int:id>', methods=['PUT'])
    def complete_todo(id):
        todo = Todo.query.get_or_404(id)
        todo.status = 'COMPLETED'
        db.session.commit()
        return redirect(url_for('home'))

    @app.route('/todos/uncomplete/<int:id>', methods=['PUT'])
    def uncomplete_todo(id):
        todo = Todo.query.get_or_404(id)
        todo.status = 'PENDING'
        db.session.commit()
        return redirect(url_for('home'))

    @app.route('/todos/delete/<int:id>', methods=['POST'])
    def delete_todo(id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully', 'success')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app = create_app()
    register_routes(app)
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect
from . import db
from .models import Todo

views = Blueprint('views', __name__)


# Home page, default
@views.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # Grabbing data from <input> where name is 'content'
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')  # redirect to index.html
        except:
            return 'There was an issue adding your task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# Delete task functionality
@views.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'


# Update task functionality
@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task)

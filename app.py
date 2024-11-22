from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Initialize the `rr_tasks` Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rr_tasks.db'
tasks_db = SQLAlchemy(app)


class Todo(tasks_db.Model):
    id = tasks_db.Column(tasks_db.Integer, primary_key=True)
    content = tasks_db.Column(tasks_db.String(200), nullable=False)
    completed = tasks_db.Column(tasks_db.Integer, default=0)
    date_created = tasks_db.Column(tasks_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Default route, so we do not get 404 error
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'Testing post method...'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # Run the app, with debug on, so we can see errors on screen.
    app.run(debug=True)

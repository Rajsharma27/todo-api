from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, flash
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from flask_cors import CORS
CORS(app)


class todomodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    task = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Boolean, default=False)

todo_args = reqparse.RequestParser()
todo_args.add_argument("title", type=str, help="Task title", required=True)
todo_args.add_argument("task", type=str, help="Task description", required=True)
todo_args.add_argument("completed", type=bool)

todo_update_args = reqparse.RequestParser()
todo_update_args.add_argument("title", type=str, help="Task title", required=True)
todo_update_args.add_argument("task", type=str, help="Task description", required=True)
todo_update_args.add_argument("completed", type=bool)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'task': fields.String,
    'completed': fields.Boolean
}

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        todo = todomodel.query.get(task_id)
        if not todo:
            abort(404, message="No task available with this ID.")
        return todo

    @marshal_with(resource_fields)
    def patch(self, task_id):
        args = todo_update_args.parse_args()
        result = todomodel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Task with this ID does not exist.")

        if args['title'] is not None:
            result.title = args['title']
        if args['task'] is not None:
            result.task = args['task']
        if args['completed'] is not None:
            result.completed = args['completed']

        db.session.commit()
        return result

    def delete(self, task_id):
        todo = todomodel.query.get(task_id)
        if not todo:
            abort(404, message="Task with this ID does not exist.")
        db.session.delete(todo)
        db.session.commit()
        return '', 204

class TodoList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return todomodel.query.all()

class TodoCreate(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = todo_args.parse_args()
        todos = todomodel(
            title=args['title'],
            task=args['task'],
            completed=args.get('completed', False)
        )
        db.session.add(todos)
        db.session.commit()
        return todos, 201

api.add_resource(TodoCreate, "/todo")
api.add_resource(Todo, "/todo/<int:task_id>")
api.add_resource(TodoList, "/todos")

with app.app_context():
    db.create_all()
    with app.app_context():
        print(f"Rows in database: {todomodel.query.count()}")

@app.route('/')
def index():
    todos = todomodel.query.order_by(todomodel.id.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    task = request.form.get('task')
    completed = bool(request.form.get('completed'))
    if not title or not task:
        flash('Title and task required')
        return redirect(url_for('index'))
    todo = todomodel(title=title, task=task, completed=completed)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    t = todomodel.query.get_or_404(task_id)
    t.completed = not t.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    t = todomodel.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

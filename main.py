from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gnjfdsgnj99'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    all_todos = Todos.query.all()
    if request.method == 'POST':
        task = request.form.get('task')
        new_task = Todos(todo=task)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', todos=all_todos)


@app.route('/del')
def delete_todo():
    del_id = request.args.get('delete_id')
    task_to_delete = Todos.query.filter_by(id=del_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/del-all')
def delete_all():
    all_task = Todos.query.all()
    for task in all_task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

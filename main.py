from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Donelist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,vehicle, content, completed):
        self.vehicle = vehicle
        self.content = content
        self.completed = completed

    def __repr__(self):
        return '<task %r>' % self.id


@app.route('/')
def index():
    tasks = Donelist.query.order_by(Donelist.date_created).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task_vehicle = request.form['vehicle']
        task_content = request.form['content']
        task_completed = request.form['completed']
        new_task = Donelist(vehicle=task_vehicle, content=task_content, completed=task_completed)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Iškilo problema'

    else:
        return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    delete = Donelist.query.get_or_404(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Iškilo problema ištrinant įrašą'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Donelist.query.get_or_404(id)

    if request.method == 'POST':
        task.vehicle = request.form['vehicle']
        task.content = request.form['content']
        task.completed = request.form['completed']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Iškilo problema atnaujinant informacija'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
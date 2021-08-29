from flask import Flask , render_template ,request ,redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return self.title



@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == "POST":
        todos = Todo(title = request.form['title'],desc=request.form['desc'])
        db.session.add(todos)
        db.session.commit()
    todo = Todo.query.all()
    return render_template('index.html', alltodo = todo)


@app.route('/update/<int:sno>',methods = ['POST','GET'])
def update(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    data = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo = data)



@app.route('/delete/<int:sno>')
def delete(sno):
    data = Todo.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)

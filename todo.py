from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Ozzz/Desktop/Flask Todo App Projesi/todo.db'
db = SQLAlchemy(app)



class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)



@app.route("/")
def index():
    todos = Todo.query.all() #Bir tane liste dönecek.


    return render_template("index.html",todos = todos)


@app.route("/add",methods=["POST"])  #Sadece post request'e izin vermek istiyoruz.
def addTodo():
    # Şimdi,name parametresine göre input değerini alacaz,todo class'ından bir tane obje oluşturarak veritabanımıza ekleme yapmaya çalışacaz.

    title = request.form.get("title")
    newTodo = Todo(title=title,complete=False)

    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route('/complete/<string:id>')
def completeTodo(id):
   
    todo = Todo.query.filter_by(id=id).first()  # first() bu id'ye göre ilk değeri alacak.
    """
    if todo.complete:

        todo.complete = False
    else:
        todo.complete = True
    """
    todo.complete = not todo.complete

    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):

    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)
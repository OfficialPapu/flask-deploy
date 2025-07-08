from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

@app.route('/add', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        db.session.add(User(name=name, email=email))
        db.session.commit()
        return f"User {name} added successfully."
    else:
        return render_template('index.html')

@app.route("/get")
def get_users():
    users = User.query.all()
    return '<br>'.join([f"{u.id} - {u.name} - {u.email} | <a href='/edit/{u.id}'>Edit</a> | <a href='/delete/{u.id}'>Delete</a>" for u in users])

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
     user = User.query.get_or_404(id)
     name = request.form.get('name')
     email = request.form.get('email')
     user.name = name
     user.email = email
     db.session.commit()
     return f"User {user.name} updated successfully."
    else:
        return render_template('edit.html', user=User.query.get_or_404(id))

@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return f"User {user.name} deleted successfully."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from fr import check
from capture import shot
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/hritik/Documents/WS/database.db'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    ans = check()
    login = user.query.filter_by(username=ans).first()
    print(login)
    if login is not None:
        return render_template("success.html", ans=ans)
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        passw = hashlib.sha256(passw.encode()).hexdigest()

        unique = user.query.filter_by(username=uname).first()
        ans = "Username already exists"
        if unique is not None:
            return render_template("register.html", ans=ans)

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        shot(uname)
        return redirect(url_for("index"))
    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz-flask:blog@localhost:3307/blogz-flask'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blogs', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        verified_password = request.form["verifypassword"]

        user_error1 = ""
        user_error2 = ""
        password_error = ""
        password_error2 = ""
        veri_error = ""
        veri_error2 = ""
        user_exists_error = ""
        is_error = False

        if (not username) or username.strip() == "":
            user_error1 = "Please enter username."
            is_error = True

        if username and (len(username) < 3 or len(username) > 20 or username.isspace()):
            user_error2 = "Invalid username."
            is_error = True

        if (not password) or (password.strip() == ""):
            password_error = "Please enter password."
            is_error = True


        if (password and (len(password) < 3 or len(password) > 20 or password.isspace())):
            password_error2 = "Invalid password."
            is_error = True


        if (not verified_password) or (verified_password.strip() == ""):
            veri_error = "Please verify password."
            is_error = True


        if (verified_password != password):
            veri_error2 = "Verified password is invalid."
            is_error = True

        if is_error:
            return render_template("signup.html", error1 = user_error1, error2 = user_error2, error3 = password_error, error4 = password_error2, error5 = veri_error, error6 = veri_error2)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/index')
        else:
            user_exists_error = "This user already exists"
            return render_template("signup.html", user_exists_error)

    return render_template('signup.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        verified_password = request.form["verifypassword"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            redirect('/index')
        else:
            flash("User password incorrect, or user does not exist", "error")

    return render_template("login.html")



@app.route('/blog')
def singleUser():
    blog_id = request.args.get("id")
    post = Blogs.query.get(blog_id)
    if post:
        return render_template("singleUser.html", post=post)
    else:
        post = ""
        return render_template("singleUser.html", post=post)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        new_post = Blogs(title, body, user)
        if title and body:
            db.session.add(new_post)
            db.session.commit()
            return redirect("/blog?id="+str(new_post.id))
        else:
            error = "Don't leave title or body empty!"
            return render_template("newpost.html", error = error, title=title, body=body)

    return render_template("newpost.html")

@app.route('/index')
def index():
    user = User.query.filter_by(username=session['username']).first()
    username = ""
    if user is not None:
        username = user.username
    blogs = Blogs.query.all()
    return render_template('index.html', blogs=blogs, username = username)

if __name__ == "__main__":
    app.run()

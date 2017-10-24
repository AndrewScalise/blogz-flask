from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    # def __repr__(self):
    #    return '<Blogs title ={} body={}>'.format(self.title, self.body)


@app.route('/blog')
def indi_blog():
    blog_id = request.args.get("id")
    post = Blogs.query.get(blog_id)
    return render_template("indi_blog.html", post=post)

@app.route('/newblog', methods=['POST', 'GET'])
def newblog():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blogs(title, body)
        if title and body:
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id="+str(new_blog.id))
        else:
            error = "Don't leave title or body empty!"
            return render_template("addnewblog.html", error = error, title=title, body=body)

    return render_template("addnewblog.html")

@app.route('/')
def index():
    blogs = Blogs.query.all()
    return render_template('front_blogs.html', blogs=blogs)

if __name__ == "__main__":
    app.run()

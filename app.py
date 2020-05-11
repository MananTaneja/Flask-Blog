from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/manantaneja/Desktop/CB.EN.U4CSE17634/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(50))
    datePosted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    votes = db.Column(db.Integer)

@app.route('/')
def home():
    data = BlogPost.query.all()
    return render_template('index.html', posts=data)

@app.route('/addblog')
def addBlog():
    return render_template('addBlog.html')

@app.route('/view/<int:post_id>')
def view(post_id):
    data = BlogPost.query.filter_by(id=post_id).one()
    date_posted = data.datePosted.strftime('%B %d, %Y')
    return render_template('post.html', data=data, date_posted=date_posted)


@app.route('/upvote/<int:post_id>')
def upvote(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    post.votes = post.votes + 1
    db.session.commit()

    return redirect(url_for('view', post_id=post_id))


@app.route('/publish', methods=['POST'])
def publish():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    votes = 0
    post = BlogPost(title=title, author=author, content=content, datePosted=datetime.now(), votes=votes)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy,desc
from contextlib import closing
import os,datetime

app = Flask(__name__)

try:
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError:
  DATABASE_URL = "ec2-54-227-238-25.compute-1.amazonaws.com" 
  app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

#app.config.from_object(__name__)

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  url = db.Column(db.String(120))
  date = db.Column(db.DateTime, default=datetime.datetime.now())
  description = db.Column(db.Text)
  tags = db.Column(db.Text)

  def __init__(self,name,url,description,tags,date=None):
    self.name = name
    self.url = url
    self.description = description
    self.date = date
    self.tags = tags

  def __repr__(self):
    return '<boogers %s>' % self.name

class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80))
  date = db.Column(db.DateTime, default=datetime.datetime.now())
  text = db.Column(db.Text)
  tags = db.Column(db.Text)

  def __init__(self,title,text,tags,date=None):
    self.title = title
    self.date = date
    self.text = text
    self.tags = tags

  def __repr__(self):
    return '<boogers %s>' % self.title

pages = ['home','about','contact','art','prog','misc','bike']


#######
#VIEWS#
#######

@app.route('/blog')
def show_entries():
  cur = g.db.execute('SELECT title, date, text, tags FROM entries ORDER BY id DESC')
  entries = [dict(title=row[0], date=row[1], text=row[2], tags=row[3]) for row in cur.fetchall()]
  return render_template('blog.html', menu=pages, entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('INSERT INTO entries (title, text, tags) VALUES (?, ?, ?)', [request.form['title'], request.form['text'], request.form['tags']])
  g.db.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_entries'))

@app.route('/prog')
def load_prog():
  asdf = Project.query.order_by(desc(Project.date))
  projs = asdf 
  projectsList = "projxlist"#[p.name for p in projs]
  entries = "hello"#Entry.query.order_by(desc(Entry.date))
  return render_template('prog.html', current='prog', projectsList=projectsList, projects=projs, menu=pages, entries=entries)

@app.route('/')
@app.route('/<name>')
def load_home(name="home"):
  return render_template(name+".html",current=name, menu=pages)

if __name__ == '__main__':
  #app.run(host='10.211.27.196')
  app.run(debug=True)

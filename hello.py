from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
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

"""
def connect_db():
  return psycopg2.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()
"""

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
  projs = Project.query.order_by(desc(Project.date))
  projectsList = [p.name for p in projs]
  entries = "asdf"
  return render_template('prog.html', current='prog', projectsList=projectsList, projects=projs, menu=pages, entries=entries)

@app.route('/')
@app.route('/<name>')
def load_home(name="home"):
  return render_template(name+".html",current=name, menu=pages)

if __name__ == '__main__':
  #app.run(host='10.211.27.196')
  app.run(debug=True)

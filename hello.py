from flask import Flask, render_template
app = Flask(__name__)

pages = ['home','about','contact','art','prog','misc','bike']

@app.route('/')
@app.route('/<name>')
def load_home(name="home"):
  return render_template(name+".html",current=name, menu=pages)

if __name__ == '__main__':
  app.run(host='10.211.27.196')
  app.run(debug=True)

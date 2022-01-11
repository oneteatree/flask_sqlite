import random, string
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deliverys.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class deliverys(db.Model):
   id = db.Column('delivery_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   item_name = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   quantity = db.Column(db.String(10))

   def __init__(self, name, item_name, addr,quantity):
      self.name = name
      self.item_name = item_name
      self.addr = addr
      self.quantity = quantity

@app.route('/')
def show_all():
   return render_template('show_all.html', deliverys = deliverys.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['item_name'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         delivery = deliverys(request.form['name'], request.form['item_name'],
            request.form['addr'], request.form['quantity'])
         
         db.session.add(delivery)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == "__main__":  # Makes sure this is the main process
	db.create_all()
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)

	)
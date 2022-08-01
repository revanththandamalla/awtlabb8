from unicodedata import name
from urllib.parse import uses_relative
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key = True)
	fname = db.Column(db.String(100))
	lname = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))

	def __init__(self, namef,namel,mail, pwrd):
		self.fname = namef
		self.lname = namel
		self.email = mail
		self.password = pwrd

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
	if(request.method == 'POST'):
		fname = request.form['fname']
		lname = request.form['lname']	
		email = request.form['email']
		passw = request.form['pass']	
		cpass = request.form['cpass']

		if(passw != cpass):
			return render_template('signup.html', content='Passwords Not matched')
		else:
			if(fname != "" and lname !="" and email != "" and passw !="" and cpass !=""):
				res = db.session.query(users.email).filter(users.email == email).all()

				if(len(res) > 1):
					return render_template('signup.html', content="The Email Id already exists")
				usr = users(fname, lname, email, passw)
				db.session.add(usr)
				db.session.commit()
				return render_template('Thankyou.html')

	return render_template('signup.html', content="")


@app.route('/', methods=['GET','POST'])
def hello_world():
	if(request.method == 'POST'):
		email = request.form['username']
		passw = request.form['password']
		temp = db.session.query(users.password).filter(users.email == email) 
		pwd = temp[0].password

		if(passw == pwd):
			return render_template('secretPage.html')
	

	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)
    
from flask import Flask, render_template, session, request, redirect
import sqlite3
from db import *
#future import methods

app = Flask(__name__)

app.secret_key = "HI" # dummy key CHANGE LATER

@app.route('/', methods=['GET'])
def login():
#  if 'username' in session:
#    return redirect('/home') # go to displ homepage if has cookies
#  return render_template('login.html')
  return redirect('/home')

@app.route('/register', methods=['GET'])
def register():
  return render_template('registration.html')

@app.route('/signup', methods=['GET', 'POST'])
def make_account():
  #method to create entry into DB
  if user_exist(request.form.get('username')):
    return render_template('registration.html', status='username in use')

  create_user(request.form.get('username'), request.form.get('password'))
  session['username'] = request.form['username']
  return render_template("profile.html")

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  # check if user in db
  # Method to check if login in DB
  if verify(request.form.get('username'), request.form.get('password')):
    return render_template('index.html', status='Incorrect login info')
  return render_template('profile.html')

# homepage
@app.route('/home', methods=['GET'])
def home():
  #if not session:
  #  return redirect('/')

  return render_template('index.html')


if __name__ == '__main__':
  app.debug = True
  app.run()

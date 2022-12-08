from flask import Flask, render_template, session, request, redirect
import sqlite3
from db import *
#future import methods

app = Flask(__name__)

app.secret_key = "HI" # dummy key CHANGE LATER

#login page is landing page
@app.route('/', methods=['GET'])
def login():
  if 'username' in session:
    return redirect('/profile') # go to displ homepage if has cookies
  return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
  return render_template('registration.html')

@app.route('/signup', methods=['GET', 'POST'])
def make_account():
  #if not unique
  if user_exist(request.form.get('username')):
    return render_template('registration.html', status='Pick another Username (In Use)')
  #if user or pass don't ok
  #if len(request.form.get('password')) < 8:
  #  return render_template('registration.html', status='Password is too short')

  #new entry
  create_user(request.form.get('username'), request.form.get('password'))
  session['username'] = request.form['username']
  #return render_template("profile.html")
  return redirect('/profile')

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  # Method to check if login in DB
  print('hi')
  print(verify(request.form.get('username'), request.form.get('password')))
  if verify(request.form.get('username'), request.form.get('password')):
    return render_template('index.html', status='Incorrect login info')
  #return render_template('profile.html')
  return redirect('/profile')

#prof page
@app.route('/profile', methods=['GET'])
def profile():
  if not session:
    return redirect('/')
  return render_template('profile.html')


if __name__ == '__main__':
  app.debug = True
  app.run()

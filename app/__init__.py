from flask import Flask, render_template, session, request, redirect
import sqlite3
from db import *
from grass_calc import *
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
  if (request.form.get('password') != request.form.get('password-confirm')):
    return render_template('registration.html', status='The password you typed is not the same as your confirmation')
  create_user(request.form.get('username'), request.form.get('password'))
  session['username'] = request.form['username']
  #return render_template("profile.html")
  return redirect('/profile')

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  # Method to check if login in DB
  
  if not verify(request.form.get('username'), request.form.get('password')):
    return render_template('index.html', status='Incorrect login info')
  #return render_template('profile.html')
  session['username'] = request.form['username']
  return redirect('/profile')

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')

#prof page
@app.route('/profile', methods=['GET'])
def profile():
  if not session:
    return redirect('/')
  return render_template('profile.html')

#quiz page
@app.route('/quiz', methods=['GET'])
def quiz():
  q = new_quiz()
  a1 = random.choice(q['wrong'])
  a2 = ""
  a3 = ""
  a4 = ""
  #answer choices


if __name__ == '__main__':
  app.debug = True
  app.run()

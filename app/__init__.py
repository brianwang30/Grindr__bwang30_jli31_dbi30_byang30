from flask import Flask, render_template, session, request, redirect
import sqlite3
import os
from db import *
from grass_calc import *
import api
# from grass_calc import *
#future import methods

app = Flask(__name__)

app.secret_key = os.urandom(32)

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

#logout
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

#pokemon quiz page
@app.route('/pokequiz', methods=['GET'])
def pokequiz():
  #THESE ARE BROKEN RN
  q = new_quiz()
  #return render_template('pokequiz.html')
  return render_template('pokequiz.html', img = q['img'], correct = q['right'], a0 = q['ans'][0], a1 = q['ans'][1], a2 = q['ans'][2], a3 = q['ans'][3])
  #return render_template('pokequiz.html', img = q['img'], correct = q['right'], a0 = q['ans'][0], a1 = q['ans'][1], a2 = q['ans'][2])

@app.route('/pokecorrect')
def pokecorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, get_grass(id) - 250)

  q = new_quiz()
  print("correct")
  #replace with random render_template version
  return render_template('pokequiz.html', status = "correct!", img = q['img'], correct = q['right'], a0 = q['ans'][0], a1 = q['ans'][1], a2 = q['ans'][2], a3 = q['ans'][3])

@app.route('/pokeincorrect')
def pokeincorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, get_grass(id) + 100)

  q = new_quiz()
  print("incorrect")
  #replace with random render_template version
  return render_template('pokequiz.html', status = "wrong!", img = q['img'], correct = q['right'], a0 = q['ans'][0], a1 = q['ans'][1], a2 = q['ans'][2], a3 = q['ans'][3])

@app.route('/animequiz', methods=['GET'])
def animequiz():
    animes = api.random_anime()

    if len(animes) == 0:
        return render_template('animequiz.html', status = 'No/Wrong API key')
    else:
        return render_template('animequiz.html', correct = animes.get("anime0")[0], img = animes.get("anime0")[1], a0 = animes.get("anime1")[0], a1 = animes.get("anime2")[0], a2 = animes.get("anime3")[0])

@app.route("/animecorrect")
def animecorrect():
#    id = get_userID(session['username'])
#    update_grass(id, get_grass(id) - 250) doesnt work for now
    animes = api.random_anime()

    return render_template('animequiz.html', status = "correct!", correct = animes.get("anime0")[0], img = animes.get("anime0")[1], a0 = animes.get("anime1")[0], a1 = animes.get("anime2")[0], a2 = animes.get("anime3")[0])

if __name__ == '__main__':
  app.debug = True
  app.run()

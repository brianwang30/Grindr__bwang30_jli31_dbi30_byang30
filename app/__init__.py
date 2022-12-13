from flask import Flask, render_template, session, request, redirect
import sqlite3
import os
from db import *
from grass_calc import *
import api
import pprint, random
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
  id = get_userID(session['username'])
  if not session:
    return redirect('/')
  return render_template('profile.html', grassometer = get_grass(id))

#pokemon quiz page
@app.route('/pokequiz/<stat>', methods=['GET'])
def pokequiz(stat):
  q = new_quiz()
  choices = q['ans']
  correct_img = q['img']
  choices_status = ['incorrect','incorrect','incorrect','incorrect']
  correct_index = choices.index(q['right'])
  choices_status[correct_index] = 'correct'
  #return render_template('pokequiz.html')
  id = get_userID(session['username'])
  return render_template('pokequiz.html', 
  status = stat,
  choices = choices, 
  correct_img = correct_img, 
  choices_status = choices_status , 
  grassometer = get_grass(id))
  #return render_template('pokequiz.html', img = q['img'], correct = q['right'], a0 = q['ans'][0], a1 = q['ans'][1], a2 = q['ans'][2])

@app.route('/pokecorrect', methods = ['GET'])
def pokecorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, int("-250"))

  return redirect('/pokequiz/correct')


@app.route('/pokeincorrect', methods = ['GET'])
def pokeincorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, int("+100"))

  return redirect('/pokequiz/wrong')

@app.route('/animequiz', methods=['GET'])
def animequiz():
    animes = api.random_anime()
    id = get_userID(session['username'])
    
    
    if len(animes) == 0: #len 0 dictionary is printed when API key is wrong or not provided
      return render_template('animequiz.html', status = 'No/Wrong API key')
    else:
      choices = []
      for anime in animes.keys():
        #appends anime names to choices
        choices.append(animes[anime][0])
      correct_index = random.randrange(0,4)
      correct_img = animes[f'anime{correct_index}'][1] #gets the correct anime's image
      choices_status = ['incorrect','incorrect','incorrect','incorrect']
      choices_status[correct_index] = 'correct'


      return render_template('animequiz.html', 
      choices = choices,
      correct_img = correct_img,
      choices_status = choices_status,
      grassometer = get_grass(id))

@app.route("/animecorrect")
def animecorrect():
    id = get_userID(session["username"])
    update_grass(id, int("-250")) #function gets called nothing updates on the Grass o' meter
    animes = api.random_anime()
    return render_template('animequiz.html', status = "correct!", correct = animes.get("anime0")[0], img = animes.get("anime0")[1], a0 = animes.get("anime1")[0], a1 = animes.get("anime2")[0], a2 = animes.get("anime3")[0], grassometer = get_grass(id))

if __name__ == '__main__':
  app.debug = True
  app.run()

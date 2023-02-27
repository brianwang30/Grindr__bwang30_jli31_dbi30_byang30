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
  return redirect('/questionnaire')

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  # Method to check if login in DB

  if not verify(request.form.get('username'), request.form.get('password')):
    return render_template('index.html', status='Incorrect login info')
  #return render_template('profile.html')
  session['username'] = request.form['username']
  return redirect('/profile')

#questionnaire stuff
@app.route('/questionnaire', methods=['GET'])
def questionnaire():
  return render_template('questionnaire.html')

@app.route('/submitquestionnaire', methods=['POST'])
def submitquestionnaire():
  sports_hours = int(request.form['sports'])
  games_hours = int(request.form['games'])
  submit_questions(session['username'])
  user_id = get_userID(session['username'])

  update_quiz_grass(user_id, 
  sports_hours*50 +
  games_hours*-50)
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
  league_user = get_gameuser(id, 'league')
  apex_user = get_gameuser(id, 'apex')
  
  league_info = {}
  if league_user != None:
    league_info = find_summoner_info(league_user)
    
  apex_info = None
  if apex_user != None:
    apex_platform = get_apex_platform(id, apex_user)
    apex_info = apexL_info(apex_platform, apex_user)
  
  if not session:
    return redirect('/')
  #elif user_did_questions(session['username']):
  return render_template('profile.html', grassometer = get_grass(id), 
  league_user = league_user, apex_user = apex_user,
  league_info = league_info, apex_info = apex_info)
  #return redirect('/questionnaire')

#pokemon quiz page
@app.route('/pokequiz/<stat>', methods=['GET'])
def pokequiz(stat):
  q = new_quiz()
  choices = q['ans']
  #capitalizes all the pokemon in the list
  choices = list(map(lambda x: x.capitalize(), choices))
  correct_img = q['img']
  choices_status = ['incorrect','incorrect','incorrect','incorrect']
  #find the index of the correct pokemon and makes the element in choices_status correct
  correct_index = choices.index(q['right'].capitalize())
  choices_status[correct_index] = 'correct'
  #return render_template('pokequiz.html')
  id = get_userID(session['username'])

  grass_diff = '-250'
  if stat == 'wrong': grass_diff = '+100'

  return render_template('pokequiz.html', 
  status = stat.capitalize(),
  grass_diff = grass_diff,
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

@app.route('/animequiz/<stat>', methods=['GET'])
def animequiz(stat):
    animes = api.random_anime()
    id = get_userID(session['username'])


    if len(animes) == 0: #len 0 dictionary is printed when API key is wrong or not provided
      print(animes)
      return render_template('error.html', status = 'No/Wrong API key')
    else:
      choices = []
      for anime in animes.keys():
        #appends anime names to choices
        choices.append(animes[anime][0])
      correct_index = random.randrange(0,4)
      correct_img = animes[f'anime{correct_index}'][1] #gets the correct anime's image
      choices_status = ['incorrect','incorrect','incorrect','incorrect']
      choices_status[correct_index] = 'correct'

      grass_diff = '-250'
      if stat == 'wrong': grass_diff = '+100'

      return render_template('animequiz.html',
      status = stat.capitalize(),
      grass_diff = grass_diff,
      choices = choices,
      correct_img = correct_img,
      choices_status = choices_status,
      grassometer = get_grass(id))

@app.route('/animecorrect', methods = ['GET'])
def animecorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, int("-250"))

  return redirect('/animequiz/correct')


@app.route('/animeincorrect', methods = ['GET'])
def animeincorrect():
  #code to change grass count
  id = get_userID(session['username'])
  update_grass(id, int("+100"))

  return redirect('/animequiz/wrong')

#calculate games
@app.route('/games', methods = ['GET', 'POST'])
def game():
  id = get_userID(session['username'])
  #update_gameusername(id, )
  #when funct
  levelL = 0
  levelA = 0

  league_username = request.form.get('league', )
  if (league_username != "" and league_username != None):
    update_gameusername(id, 'league', league_username)
    league = find_summoner_info(league_username)
    print(league)
    levelL = -league["Level"]
  
  apex_platform = request.form.get('platform')
  apex_username = request.form.get('apex')
  if (apex_platform != None and apex_username != "" and apex_username != None):
    update_gameusername(id, f'{apex_platform}-apex', apex_username)
    apex = apexL_info(int(apex_platform), apex_username)
    print(apex)
    levelA = -apex

  total = levelL + levelA
  update_game_grass(id, total)

  return redirect('/profile')

  


if __name__ == '__main__':
  app.debug = True
  app.run()

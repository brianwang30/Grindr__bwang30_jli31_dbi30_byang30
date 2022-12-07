from flask import Flask, render_template, session, request, redirect
#future import methods

app = Flask(__name__)

app.secret_key = "HI" # dummy key CHANGE LATER

@app.route('/', methods=['GET'])
def login():
#  if 'username' in session:
#    return redirect('/home') # go to displ homepage if has cookies
#  return render_template('login.html')
  return redirect('/home')

'''
@app.route('/register', methods=['GET'])
def register():
  if 'username' in session:
    return redirect('/home') # go to displ homepage if has cookies
  return render_template('registration.html')

@app.route('/verify', methods=['GET', 'POST'])
def make_account():
  if request.method != 'POST':
    return redirect('/')
  
  #method to create entry into DB
  if not signup(request.form['username'], request.form['password']):
    if not request.form['password']:
      return render_template('registration.html', status='enter a password')
    return render_template('registration.html', status='username in use')
  
  session['username'] = request.form['username']
  return redirect('/home')

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  if request.method != 'POST':
    return redirect('/')

  # check if user in db
  #Method to check if login in DB
  if not verify(request.form['username'], request.form['password']): 
    return render_template('login.html', status='Incorrect login info')
  
  session['username'] = request.form['username']
  return redirect('/home')
'''

# homepage
@app.route('/home', methods=['GET'])
def home():
  #if not session:
  #  return redirect('/')

  return render_template('index.html', name=session['username'])
  
if __name__ == '__main__':
  app.debug = True
  app.run()

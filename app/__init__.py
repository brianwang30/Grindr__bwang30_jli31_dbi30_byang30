from flask import Flask
app = Flask(__name__)

@app.route("/")
def func():
    return None
    
if __name__ == "__main__":
    app.debug = True
    app.run()

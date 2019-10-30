import pyrebase
from flask import Flask, render_template, redirect, url_for, request
from flask import json
from string import Template

app = Flask(__name__, template_folder='templates', static_folder='static')

# # ---- Pyrebase config ---- #
# config = {
#     "apiKey": "AIzaSyDLDdQ_qcgm6R4CU2iPesBDt_etoJEnY-k",
#     "authDomain": "hippodrome-e434f.firebaseapp.com",
#     "databaseURL": "https://hippodrome-e434f.firebaseio.com",
#     "projectId": "hippodrome-e434f",
#     "storageBucket": "",
#     "messagingSenderId": "295932205335",
#     "appId": "1:295932205335:web:99122bf40d9b27c2"
# }
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()

# ---- route function ---- #
''' Decorator which tells the 
    application which URL should call the 
    associated function '''

# HTTP methods GET and POST as argument in route decorator
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        try:
            # auth.sign_in_with_email_and_password(email, password)
            return redirect('/home')
        except:
            return 'Login Failed.'
    return render_template('login.html')

# ---- run method ---- #
if __name__ == "__main__":
    app.run(debug=True)
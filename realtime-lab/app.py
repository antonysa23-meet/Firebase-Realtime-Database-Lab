from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


firebaseConfig = {
  "apiKey": "AIzaSyBaw03-ukkgjLdAa24Equz40zSc28qVwhs",
  "authDomain": "livelovelaugh-d8e5b.firebaseapp.com",
  "projectId": "livelovelaugh-d8e5b",
  "storageBucket": "livelovelaugh-d8e5b.appspot.com",
  "messagingSenderId": "504635082050",
  "appId": "1:504635082050:web:a791926afc6157d418b4db",
  "measurementId": "G-FD16HH3S9X",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
           login_session['user'] = auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
       #except:
        error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signout')
def signout():
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)
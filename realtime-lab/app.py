from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime

firebaseConfig = {
  "apiKey": "AIzaSyBaw03-ukkgjLdAa24Equz40zSc28qVwhs",
  "authDomain": "livelovelaugh-d8e5b.firebaseapp.com",
  "projectId": "livelovelaugh-d8e5b",
  "storageBucket": "livelovelaugh-d8e5b.appspot.com",
  "messagingSenderId": "504635082050",
  "appId": "1:504635082050:web:a791926afc6157d418b4db",
  "measurementId": "G-FD16HH3S9X",
  "databaseURL": "https://livelovelaugh-d8e5b-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

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
        full_name = request.form['full_name']
        bio = request.form['bio']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name": full_name, "email": email, "bio" : bio, 'username':username}
            db.child("Users").child(login_session['user']
            ['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        tweet = {'title':request.form['title'],'text':request.form['text'],'date':dt_string,'likes':0,'uid':(login_session['user']['localId'])}
        db.child("tweets").push(tweet)
        return redirect(url_for("home"))
    else:
        return render_template("add_tweet.html")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signout')
def signout():
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    return render_template("tweets.html", tweets=db.child("tweets").get().val())

@app.route('/add_like/<string:tweetid>', methods=['GET', 'POST'])
def add_like(tweetid):
    if request.method == 'POST':
        likes = {'likes' : db.child('tweets').child(tweetid).get().val()['likes'] + 1}
        db.child("tweets").child(tweetid).update(likes)
        return redirect(url_for('all_tweets'))

if __name__ == '__main__':
    app.run(debug=True)
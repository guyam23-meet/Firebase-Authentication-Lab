from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
#from here up is no no zone

config = {
  "apiKey": "AIzaSyBLjpaAtI9I5rzgBVmmZzriWqK0GGSmAWA",
  "authDomain": "new-name-6e363.firebaseapp.com",
  "projectId": "new-name-6e363",
  "storageBucket": "new-name-6e363.appspot.com",
  "messagingSenderId": "1049441953646",
  "appId": "1:1049441953646:web:4ef19ea059a8f63ebe037f",
  "measurementId": "G-4RV1J1TTE5",
  "databaseURL":"https://new-name-6e363-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            print("signin error")
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        #try:
        login_session['user']=auth.create_user_with_email_and_password(email,password)
        user = {'email':email,'password':password}
        db.child('users').child(login_session['user']['localId']).set(user)
        return redirect(url_for('add_tweet'))
        #except:
        print("sign up error")
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user']=None
    auth.current_user=None
    return redirect(url_for('signup'))  

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

#from here down is black magic and I ain't touching that

if __name__ == '__main__':
    app.run(debug=True)
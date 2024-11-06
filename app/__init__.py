'''
Swedish Fish - Kishi Wijaya, Jason Chao, Tahmim Hassan, Tanzeem Hasan
SoftDev
P00: Move Slowly and Fix Things
2024-10-30
Time Spent: 0.2
'''

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 # for accessing DBs
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# placeholder example logins (until we have functioning databases)
logins = {
    "jason" : "chao",
    "kishi" : "wijaya",
    "tahmim" : "hassan",
    "tanzeem" : "hasan",
}

# MAIN PAGE
@app.route('/', methods=['GET','POST'])
def home():
    # print("=====================\n")
    # print(app)
    # print("=====================\n")
    # print(request)
    # print("=====================\n")
    # print(request.args)
    if 'username' in session:
        return render_template("home.html", logged_in_text="Welcome " + session['name'])
    else:
        return render_template('home.html')

# USER LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/auth_login', methods=["GET", "POST"])
def auth_login():
    if request.method == "POST":
        # if username and password match in USER DB, then...
        username = request.form['username']
        password = request.form['password']
        if username in logins and logins[username] == password:
            session['username'] = 'username'
            session['name'] = username
            return redirect('/')
            # return render_template("home.html", logged_in_text="Welcome " + username)
        else:
            return render_template("login.html", error_text="Incorrect username or password.")

# USER REGISTRATIONS
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/auth_reg', methods=["GET", "POST"])
def auth_reg():
    if request.method == "POST":
        new_username = request.form['new_user']
        new_password = request.form['new_pass']
        if len(new_username) < 4:
            return render_template("register.html", error_text="Please provide a new username of at least 4 characters.")
        elif len(new_password) < 8:
            return render_template("register.html", error_text="Please provide a new password of at least 8 characters.")
        else:
            # ADD USERNAME AND PASSWORD AS NEW ROW IN USER DB
            logins[new_username] = new_password
            return render_template("login.html", registered_text="You are now registered! Please log in.")
    else:
        return None

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")



# STORIES
@app.route("/view/" + ttl)
def edit():
    if user:
        return render_template( 'view.html', username = user, storyname = ttl, content = story)
    return render_template(' account.html ')

@app.route("/newstory")
def newstory():
    return render_template( 'newStory.html', username = user)

@app.route("/edit/" + ttl)
def edit():
    if user:
        return render_template( 'editing.html', username = user, storyname = ttl, content = story)

@app.route('/history')
def history():
    return "View edit histories here"

if __name__ == "__main__":
    app.debug = True
    app.run()

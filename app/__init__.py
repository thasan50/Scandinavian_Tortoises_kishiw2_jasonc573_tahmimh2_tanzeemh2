from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

logins = {"victor" : "casado",
          "jason" : "chao",
          "evan" : "chan"}

@app.route('/')
def login():
    if 'username' in session:
        return redirect('/auth')
    else:
        return render_template("login.html")

@app.route('/auth')
def auth_login():
    if 'username' in session:
        return render_template("home.html", user = session['username'])
    login = request.args
    # print(login['username'])
    # print(login['password'])
    username = login['username']
    password = login['password']
    if username in logins:
        if logins[username] == password:
            session['username'] = username
            return render_template("home.html", user = username)
        else:
            return redirect('/')
    else:
        return redirect('/') # redirect back to / route

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()

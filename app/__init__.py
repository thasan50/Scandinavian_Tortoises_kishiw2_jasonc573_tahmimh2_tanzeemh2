'''
Swedish Fish - Kishi Wijaya, Jason Chao, Tahmim Hassan, Tanzeem Hasan
SoftDev
P00: Move Slowly and Fix Things
2024-11-06
Time Spent: 8 hours
'''

from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3
import sys
sys.path.insert(0, 'db_maker/') # when running __init__.py, user MUST be in project root directory
import db_maker as db


app = Flask(__name__)
app.secret_key = os.urandom(32)

# placeholder example logins (until we have functioning databases)
logins = {
    "jason" : "chao",
    "kishi" : "wijaya",
    "tahmim" : "hassan",
    "tanzeem" : "hasan",
}

# CONNECTION TO DATABASES
db.setup()

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
        if db.verify_user(username, password):
        # if username in logins and logins[username] == password:
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
            # logins[new_username] = new_password
            try: 
                db.create_user(new_username, new_password)
                return render_template("login.html", registered_text="You are now registered! Please log in.")
            except:
                return render_template("register.html", error_text="Username already exists.")
    else:
        return None

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")


# STORIES
@app.route("/view/<title>")
def view(title):
    if 'username' not in session:
        return redirect(url_for('login'))

    # gets story id from url 
    story_id = session.get('storyID')
    if request.args.get('id'):
        story_id = request.args.get('id')
        session['storyID'] = story_id

    # uses story Id to get story data
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT storyContent, title, lastContent FROM storyData WHERE storyID = ?", (story_id,))
    story = c.fetchone()
    db.close()
    if not story:
        return "Story not found", 404
    story_content, title, last_entry = story
    return render_template('view.html', story=story_content, title=title, lastentry=last_entry)

@app.route("/newstory", methods=["GET", "POST"])
def newstory():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # takes data from form
        title = request.form['title']
        entry = request.form['entry']
        user_id = session['username']
        # adding the new story to the database
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # Find the next story ID by checking the maximum current storyID
        c.execute("SELECT MAX(storyID) FROM storyData")
        result = c.fetchone()
        story_id = (result[0] + 1) if result[0] is not None else 1
        # Insert the new story into storyData
        c.execute('''
            INSERT INTO storyData (storyID, title, storyContent, allAuthors, lastContent, lastAuthor, editNumber)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (story_id, title, entry, user_id, entry, user_id, 1))
        db.commit()
        db.close()
        # Save the story ID in the session
        session['storyID'] = story_id
        # Redirect to the newly created story's view page
        return redirect(url_for('view_story'))
    return render_template('newStory.html', user=session['username'])

@app.route("/edit/<title>", methods=["GET", "POST"])
def edit(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    # Retrieve story ID from the session
    story_id = session.get('storyID')
    if request.method == 'POST':
        # Get the new entry from the form
        new_entry = request.form['content']
        user_id = session['username']
        # Update the story in the database
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # Update the story content
        c.execute('''
            UPDATE storyData
            SET storyContent = storyContent || '\n' || ?, lastContent = ?, lastAuthor = ?, editNumber = editNumber + 1
            WHERE storyID = ?
        ''', (new_entry, new_entry, user_id, story_id))
        db.commit()
        db.close()
        # Redirect to the view page after updating the story
        return redirect(url_for('view_story'))
    # Searcjes fpr the story using the storyID
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT lastContent FROM storyData WHERE storyID = ?", (story_id,))
    last_entry = c.fetchone()
    db.close()
    if not last_entry:
        return "Story not found", 404
    return render_template('editing.html', lastentry=last_entry[0], user=session['username'])

@app.route('/history')
def history():
    stories = db.get_all_stories()  # Fetch all stories from the database
    return render_template('existing.html', user=session['name'], stories=stories)

if __name__ == "__main__":
    app.debug = True
    app.run()
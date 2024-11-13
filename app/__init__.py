'''
Swedish Fish - Kishi Wijaya, Jason Chao, Tahmim Hassan, Tanzeem Hasan
SoftDev
P00: Move Slowly and Fix Things
2024-11-06
Time Spent: 8 hours
'''

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3
import sys
sys.path.insert(0, 'db_maker') # when running __init__.py, user MUST be in project root directory
import db_maker as dbx
DB_FILE = "stories.db" # Names db_file in __init__.py
app = Flask(__name__)

app.secret_key = os.urandom(32)
# # placeholder example logins (until we have functioning databases)
# logins = {
#     "jason" : "chao",
#     "kishi" : "wijaya",
#     "tahmim" : "hassan",
#     "tanzeem" : "hasan",
# }

# CONNECTION TO DATABASES
dbx.setup() #sets up databases

# MAIN PAGE
@app.route('/', methods=['GET','POST'])
def home():
    if 'username' in session:
        return render_template("home.html", logged_in_text="Welcome " + session['username'])  # Logged in
        # Want to print list of stories contributed to on this page
    else:
        return redirect("/login") # Logged out

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
        app.secret_key = os.urandom(32)
        if dbx.verify_user(username, password):
        # if username in logins and logins[username] == password:
            session['username'] = username
            session['name'] = username
            return redirect('/')
        else:
            flash("Incorrect username or password.", 'error')
            return redirect("/login")

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
            flash("Please provide a new username of at least 4 characters.", 'error')
            return render_template("register.html")
        elif len(new_password) < 8:
            flash("Please provide a new password of at least 8 characters.", 'error')
            return render_template("register.html")
        elif new_password != request.form['confirm_pass']:
            flash("Passwords do not match.", 'error')
            return render_template("register.html")
        else:
            try:
                dbx.create_user(new_username, new_password)
                flash("You are now registered! Please log in.", 'success')
                return render_template("login.html")
            except sqlite3.IntegrityError: # I need something like this for when titles repeat
                flash("Username already exists.", 'error')
                return render_template("register.html")

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")


# STORIES
@app.route("/view/<title>")
def view(title):
    # It's clear that the story content, title and other details are not displayed when on their page
    if 'username' not in session:
        return redirect(url_for('login'))

    # gets story id from url
    # story_id = session.get('storyID')
    # if request.args.get('id'): # Where is id ever referenced, in html or python? I can't find it
    #     story_id = request.args.get('id')
    #     session['storyID'] = story_id

    # # uses story title to get story data
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT storyContent, title FROM storyData WHERE title = ?", (title,))
    story = c.fetchone()
    db.close()
    if not story:
        return "Story not found", 404
    story_content, story_title = story # Since when does it work like this?
    return render_template('view.html', content=story_content, storyname=story_title, user=session['username']) # Isn't it a problem to have so many overlapping names?

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
        print(title)
        print(entry)
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
        return redirect(url_for('view', title=title))
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
        return redirect(url_for('view'))
    # Searches fpr the story using the storyID
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
    stories = dbx.get_user_story(session['username'])  # Fetch all stories from the database
    return render_template('existing.html', user=session['name'], stories=stories)

if __name__ == "__main__":
    app.debug = True
    app.run()

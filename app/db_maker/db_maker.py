import sqlite3

DB_FILE = "stories.db" #create a database for stories

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        );
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS allStories (
            storyID INTEGER,
            title TEXT,
            lastContent TEXT,
            firstAuthor TEXT,
            lastAuthor TEXT,
            editNumber INTEGER
        );
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS storyData (
            storyID INTEGER,
            title TEXT NOT NULL UNIQUE,
            storyContent TEXT,
            allAuthors TEXT,
            lastContent TEXT,
            lastAuthor TEXT,
            editNumber INTEGER
        );
    ''')
    
    db.commit()
    db.close()
    
# Implement a userID and storyID counter
def create_user(username, password):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    db.commit()
    db.close()
    
def verify_user(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    db.close()
    return user is not None # returns true if the user is in the database

def add_to_all_stories(title, storyContent, author):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    c.execute("INSERT INTO allStories(title, storyContent, author, author, editNumber) VALUES(?, ?, ?, ?, ?)", (title, storyContent, author, author, 0))
    db.commit()
    db.close()
    create_story(title, storyContent, author)

def create_story(title, storyContent, firstAuthor):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    c.execute("INSERT INTO storyData(title, storyContent, allAuthors, lastContent, lastAuthor, editNumber) VALUES(?, ?, ?, ?, ?, ?)", (title, storyContent, firstAuthor, storyContent, firstAuthor, 0))
    db.commit()
    db.close()

def edit_all_stories(story_id, lastContent, lastAuthor):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    edit = get_edit_number(story_id)+1
    c.execute("UPDATE allStories SET lastContent=?, lastAuthor=?, editNumber=? WHERE storyID=?", (lastContent, lastAuthor, edit, story_id))
    db.commit()
    db.close()
    edit_story(story_id, lastContent, lastAuthor)
    
def edit_story(story_id, lastContent, lastAuthor):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    temp = get_story_content(story_id) + "\n" + lastContent
    temp2 = get_authors() + ", " + lastAuthor
    c.execute("UPDATE storyData SET storyContent=?, allAuthors=?, lastContent=?, lastAuthor=? WHERE storyID=?", (temp, temp2, lastContent, lastAuthor, story_id))
    db.commit()
    db.close()

def get_user_story(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c=db.cursor()
    c.execute('''
        SELECT DISTINCT allStories.storyID, allStories.title, allstories.lastContent
        FROM allStories
        JOIN storyData ON allStories.storyID = storyData.StoryID
        WHERE storyData.author = ?
        ''', (username)
    )
    stories = c.fetchall()
    db.close()
    return stories

def get_authors(story_id):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    result = c.execute("SELECT allAuthors FROM storyData WHERE storyID=?", (story_id))
    db.commit()
    db.close()
    return result

def get_story_content(story_id):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    result = c.execute("SELECT storyContent FROM storyData WHERE storyID=?", (story_id))
    db.commit()
    db.close()
    return result

def get_story_ID(title):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    result = c.execute("SELECT storyID FROM storyData WHERE title=?", (title))
    db.commit()
    db.close()
    return result

def get_edit_number(story_id):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    result = c.execute("SELECT editNumber FROM storyData WHERE storyID=?", (story_id))
    db.commit()
    db.close()
    return result


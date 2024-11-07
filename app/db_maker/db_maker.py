import sqlite3

DB_FILE = "stories.db" #create a database for stories

def initialize_db():
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() #facilitate database operators to trigger db events

    c.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            );
    ''')
    c.execute(
    '''
    CREATE TABLE IF NOT EXISTS allStories (
            storyID INTEGER
            title TEXT,
            lastContent TEXT,
            firstAuthor TEXT,
            lastAuthor TEXT,
            editNumber INTEGER,
            PRIMARY KEY(storyID, title)
            );
    ''')
    c.execute(
    '''
    CREATE TABLE IF NOT EXISTS storyData (
            storyID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            storyContent TEXT,
            lastContent TEXT,
            lastAuthor TEXT,
            editNumber INTEGER
            FOREIGN KEY(storyID) REFERENCES allStories(storyID)
            );
    ''')
    db.commit()
    db.close()
    
# Implement a userID and storyID counter
def create_user(username, password):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    c.execute("INSERT INTO users(username, password) VALUES (?, ?, ?)", (username, password))
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
    c.execute("INSERT INTO storyData(title, storyContent, lastContent, author, editNumber) VALUES(?, ?, ?, ?, ?)", (title, storyContent, storyContent, firstAuthor, 0))
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
        ''', (username,)
    )
    stories - c.fetchall()
    db.close()
    return stories
   
def edit_all_stories(story_id, lastContent, lastAuthor):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor() 
    edit = editNumber+1
    c.execute("UPDATE allStories SET lastContent=?, lastAuthor=?, editNumber=? WHERE storyID=?", lastContent, lastAuthor, edit)
    db.commit()
    db.close()
    editStory(story_id, lastContent, lastAuthor)
    
def edit_story(story_id, lastContent, lastAuthor):
    db=sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    temp = storyContent + "\n" + lastContent
    c.execute("UPDATE storyData SET storyContent=?, lastContent=?, lastAuthor=? WHERE storyID=?", temp, lastContent, lastAuthor, story_id)
    db.commit()
    db.close()

# If a title is in the database, I need to tell the user to pick another title

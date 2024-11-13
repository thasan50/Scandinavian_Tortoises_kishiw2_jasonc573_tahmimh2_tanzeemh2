import sqlite3
import os

DB_FILE = "app/stories.db" 

def setup():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS allStories (
            storyID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            lastContent TEXT,
            firstAuthor TEXT,
            lastAuthor TEXT,
            editNumber INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS storyData (
            storyID INTEGER,
            title TEXT NOT NULL UNIQUE,
            storyContent TEXT,
            allAuthors TEXT,
            lastContent TEXT,
            lastAuthor TEXT,
            editNumber INTEGER,
            FOREIGN KEY (storyID) REFERENCES allStories(storyID)
        )
    ''')
    
    db.commit()
    db.close()

def create_user(username, password):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))

def verify_user(username, password):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return c.fetchone() is not None

def add_to_all_stories(title, storyContent, author):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute('''
            INSERT INTO allStories(title, lastContent, firstAuthor, lastAuthor, editNumber) VALUES(?, ?, ?, ?, ?)
        ''', (title, storyContent, author, author, 1))
        story_id = c.lastrowid
        c.execute('''
            INSERT INTO storyData(storyID, title, storyContent, allAuthors, lastContent, lastAuthor, editNumber) VALUES(?, ?, ?, ?, ?, ?, ?)
        ''', (story_id, title, storyContent, author, storyContent, author, 1))

def edit_all_stories(story_id, lastContent, lastAuthor):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT allAuthors FROM storyData WHERE storyID=?", (story_id,))
        authors = c.fetchone()[0]
        if lastAuthor in authors.split(", "):
            return "You've already edited this story"
        edit_num = get_edit_number(story_id) + 1
        c.execute('''
            UPDATE allStories 
            SET lastContent=?, lastAuthor=?, editNumber=? 
            WHERE storyID=?
        ''', (lastContent, lastAuthor, edit_num, story_id))
        c.execute("SELECT storyContent, allAuthors FROM storyData WHERE storyID=?", (story_id,))
        current_content, current_authors = c.fetchone()
        new_content = current_content + "\n" + lastContent
        new_authors = current_authors + ", " + lastAuthor
        c.execute('''
            UPDATE storyData 
            SET storyContent=?, allAuthors=?, lastContent=?, lastAuthor=?, editNumber=?
            WHERE storyID=?
        ''', (new_content, new_authors, lastContent, lastAuthor, edit_num, story_id))
        return "Success"

def get_user_story(username):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute('''
            SELECT DISTINCT s.storyID, s.title, s.lastContent
            FROM allStories s
            JOIN storyData d ON s.storyID = d.storyID
            WHERE d.allAuthors LIKE ?
        ''', (f'%{username}%',))
        return c.fetchall()

def get_story_content(story_id):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT lastContent FROM storyData WHERE storyID=?", (story_id,))
        result = c.fetchone()
        return result[0] if result else None

def get_story_ID(title):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT storyID FROM storyData WHERE title=?", (title,))
        result = c.fetchone()
        return result[0] if result else None

def get_edit_number(story_id):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT editNumber FROM storyData WHERE storyID=?", (story_id,))
        result = c.fetchone()
        return result[0] if result else 0
import sqlite3

DB_FILE = "stories.db" #create a database for stories

db=sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor() #facilitate database operators to trigger db events

c.execute(
'''
CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        password TEXT,
        privatekey TEXT
        );
''')
c.execute(
'''
CREATE TABLE IF NOT EXISTS blogs (
        title TEXT PRIMARY KEY,
        summary TEXT,
        content TEXT,
        author TEXT,
        datePublished TEXT,
        userKey TEXT
        );
''')
db.commit()
db.close()

'''
Swedish Fish - Kishi Wijaya, Jason Chao, Tahmim Hassan, Tanzeem Hasan
SoftDev
P00: Move Slowly and Fix Things
2024-10-30
Time Spent: 0.2
'''

from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)

@app.route('/')
def home():
    return "Home page goes here"

@app.route('/login')
def login():
    return "Login & registration goes here"

@app.route('/view')
def view():
    return "Viewing stories goes here"

@app.route('/create')
def create():
    return "Creating stories goes here"

@app.route('/edit')
def edit():
    return "Editing stories goes here"

@app.route('/history')
def history():
    return "View edit histories here"

if __name__ == "__main__":
    app.debug = True
    app.run()

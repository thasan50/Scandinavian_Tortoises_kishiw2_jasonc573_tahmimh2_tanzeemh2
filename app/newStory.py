'''
Swedish Fish - Kishi Wijaya, Jason Chao, Tahmim HAssan, Tanzeem Hasan
SoftDev
Editing an existing story python file
'''

from flask import Flask
from flask import render_template
from flask import request
from flask import session

app = Flask(__name__)

user = "b"



@app.route("/newstory")
def edit():
    if user:
        return render_template( 'newStory.html', username = user)
    return render_template(' account.html ')

if __name__ == "__main__":
    app.debug = True
    app.run()


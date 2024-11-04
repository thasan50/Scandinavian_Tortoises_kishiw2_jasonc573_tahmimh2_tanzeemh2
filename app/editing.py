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

ttl = "a"
user = "b"

@app.route("/" + ttl)
def edit():
    if username:
        return render_template( 'editing.html', username = user, title = )
    return render_template(' account.html ')

if __name__ == "__main__":
    app.debug = True
    app.run()

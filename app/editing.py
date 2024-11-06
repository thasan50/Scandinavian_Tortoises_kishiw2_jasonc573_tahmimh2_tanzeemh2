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
story = """

Lorem ipsum odor amet, consectetuer adipiscing elit. Habitasse tristique elit platea consectetur cursus. Eros ultricies dui habitant id dui pretium iaculis. Aest lectus rutrum feugiat quisque porta. Eleifend mus blandit platea ac maximus lectus semper. In consequat velit finibus phasellus primis adipiscing eget; suspendisse consectetur. Sapien senectus ad ridiculus gravida quisque viverra, nullam consectetur. Eros donec non et hac enim. Sagittis fermentum curae feugiat fringilla molestie facilisi nibh.

Tempus varius nulla tempor arcu diam suspendisse est enim. Ridiculus porta tortor orci accumsan egestas; lectus elementum euismod. Suscipit hac amet lectus; ac vulputate lacinia? Mi eu at et netus in viverra ex. Penatibus finibus vel risus risus platea convallis. Tempor dictumst ac class lobortis enim vehicula porta? Felis nisl ullamcorper efficitur et est, potenti congue. Metus potenti et malesuada convallis; fusce risus dis. Tempus non porta quis morbi velit iaculis hendrerit.

Aptent egestas nec malesuada arcu ac. Nam potenti vel; sollicitudin urna et imperdiet est posuere vivamus. Massa vehicula inceptos a massa sit cursus donec. Ac ad suscipit nibh nostra montes ullamcorper ac sem. Faucibus netus congue lobortis consequat fermentum leo vestibulum urna iaculis. Gravida justo nec nunc mattis nec efficitur. Pretium imperdiet efficitur eget erat tincidunt parturient condimentum dictum.

"""


@app.route("/" + ttl)
def edit():
    if user:
        return render_template( 'editing.html', username = user, storyname = ttl, content = story)
    return render_template(' account.html ')

if __name__ == "__main__":
    app.debug = True
    app.run()


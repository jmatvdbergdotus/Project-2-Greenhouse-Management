from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<table border=1><tr>"+ \
           "<td colspan=4>Test</td>"+ \
           "</tr><tr>"+ \
           "<td>"+insteadof1()+"</td><td>2</td><td>3</td><td>4</td>"+ \
           "</tr></table>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


def insteadof1():
    return "Freek"
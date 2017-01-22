from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/<path:path>')
def index(path = 'address.html'):
    #stat = request.cookies.get('state')
    #dist = request.cookies.get('district')

    #if (stat != '' and dist != ''):
        # Generate Index
    #else if (path == 'address.html'):
    return app.send_static_file(path)

from flask import Flask

app = Flask(__name__, static_url_path='')

import api

@app.route('/')
def index():
    return app.send_static_file("index.html")


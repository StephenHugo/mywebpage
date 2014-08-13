import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'I AM THE KING OF WEB DEVELOPMENT!'
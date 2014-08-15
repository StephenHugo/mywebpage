import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'I followed the directions on Heroku to create this page.'
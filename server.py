from flask import Flask
from waitress import serve
import os

app = Flask(__name__)

@app.route('/')
def index():
	return "Welcome to sislisten"


if __name__ == '__main__':
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env is not None and flask_env.lower() == 'production':
        serve(app, host='127.0.0.1', port=5000, threads=6)
    else:
        app.run(debug=True)

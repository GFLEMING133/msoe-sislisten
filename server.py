from flask import Flask
from waitress import serve
import os
import argparse
from queue import Queue

app = Flask(__name__)

@app.route('/mood_lighting', methods=['POST'])
def mood_lighting():
    # TODO
	return "Welcome to sislisten"

def parse_arguments():
    client_args = argparse.ArgumentParser(
        description="A server that listens for audio on a sisyphus table"
    )
    client_args.add_argument(
        '-s',
        '--seconds',
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=5,
        help="Number of seconds recorded before sent for processing"
    )
    client_args.add_argument(
        '-sr',
        '--samplingrate',
        type=int,
        choices=[4000, 8000, 16000, 32000, 44100],
        default=8000,
        help="Recording sampling rate"
    )
    client_args.add_argument(
        '-ai',
        '--aiservice',
        type=str,
        default="https://sisyphus-mood-lighting-server.herokuapp.com/get_mood_color_from_audio_stream",
        help="URL for AI Service"
    )
    client_args.add_argument(
        '-sp',
        '--sisbotport',
        type=str,
        default="3002",
        help="The port that the sisbot server is using on the table"
    )
    return client_args.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    app.config['record_seconds'] = args.seconds
    app.config['sampling_rate'] = args.samplingrate
    app.config['ai_service'] = args.aiservice
    app.config['sisbot_port'] = args.sisbotport
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env is not None and flask_env.lower() == 'production':
        serve(app, host='127.0.0.1', port=5000, threads=6)
    else:
        app.run(debug=True)

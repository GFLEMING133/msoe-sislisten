from flask import Flask
from waitress import serve
import os
import argparse
import pyaudio
from queue import Queue
import io
import requests

app = Flask(__name__)
audio_sample_queue = Queue()

def call_mood_lighting_ai_service(audio_sample):
    data = { 'audioSample': audio_sample }
    response = requests.post(app.config['ai_service'], data=data) # Note this will make the content type application/x-www-form-urlencoded
    return response.json()

def translate_audio_to_color():
    global audio_sample_queue
    if not audio_sample_queue.empty():
        audio_sample = audio_sample_queue.get()
        ai_service_response = call_mood_lighting_ai_service(audio_sample)

def read_from_input_device():
    global audio_sample_queue
    buffer_size = app.config['sampling_rate'] * app.config['record_seconds']
    input_stream = app.config['input_stream']
    data_bytes = stream.read(buffer_size)
    data_stream = io.BytesIO(data_bytes)
    audio_sample_queue.put(data_stream)

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
        default="https://sisyphus-mood-lighting-server.herokuapp.com/get_mood_color_from_audio",
        help="URL for AI Service"
    )
    client_args.add_argument(
        '-ta',
        '--tableservice',
        type=str,
        default="http://127.0.0.1:3002/sisbot/set_led_color",
        help="Service that the RGB value should be sent to"
    )
    return client_args.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    app.config['record_seconds'] = args.seconds
    app.config['sampling_rate'] = args.samplingrate
    app.config['ai_service'] = args.aiservice
    app.config['table_service'] = args.tableservice
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sampling_rate,
        input=True,
        frames_per_buffer=app.config['record_seconds'] * app.config['sampling_rate']
    )
    app.config['input_stream'] = stream
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env is not None and flask_env.lower() == 'production':
        serve(app, host='127.0.0.1', port=5000, threads=6)
    else:
        app.run(debug=True)

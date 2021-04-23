import os
import argparse
from flask import Flask, request, jsonify
from waitress import serve
from queue import Queue
from time import sleep
from color_settings import Color_Settings
from scheduler import Scheduler
from listener import listen

app = Flask(__name__)

@app.route('/mood_lighting_begin', methods=['GET'])
def mood_lighting_begin():
    global scheduler
    scheduler.start()
    return "Listener started!"

@app.route('/mood_lighting_end', methods=['GET'])
def mood_lighting_end():
    global scheduler
    scheduler.stop()
    return "Listener stopped!"

@app.route('/mood_lighting_settings', methods=['POST'])
def update_settings():
    """
    This method accepts a request body like below:
     { "settings" :  
        {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
     }
    """
    if 'settings' not in request.json:
        return jsonify({'error': 'No settings were found on the request'}), 400
    if type(request.json['settings']) is dict:
        for emotion_name, color_value in request.json["settings"].items():
            is_valid_color = type(color_value) is list and len(color_value) == 3 and \
                             is_valid_rgb_value(color_value[0]) and is_valid_rgb_value(color_value[1]) and \
                             is_valid_rgb_value(color_value[2])
            if not is_valid_color:
                return jsonify({'error': f"The emotion {emotion_name} has the invalid color value {color_value}"}), 400


        all_emotions_are_present = all_emotions_present(request.json['settings'])
        if not all_emotions_are_present:
            return jsonify({'error': "Incomplete settings. Need emotions disgust, anger, alert, happy, calm, relaxed, sad and neutral."}), 400
        
        settings = Color_Settings(request.json["settings"])
        return jsonify({'message': "Settings applied!"})
    return jsonify({'error': 'Settings request object is not a valid type'}), 400

@app.route('/mood_lighting_settings', methods=['GET'])
def get_settings():
    """
    This endpoint returns a response something like:
     { "settings" :  
        {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],bet
            "neutral": [0, 0, 0]
        }
     }
    """
    settings = Color_Settings().color_dictionary
    if settings:
        return jsonify({"settings" : settings})
    else:
        return jsonify({"message" : "Settings not set"})

def is_valid_rgb_value(rgb_value):
    return type(rgb_value) is int and rgb_value >= 0 and rgb_value <= 255

def all_emotions_present(settings):
    return "disgust" in settings and \
            "anger" in settings and \
            "alert" in settings and \
            "happy" in settings and \
            "calm" in settings and \
            "relaxed" in settings and \
            "sad" in settings and \
            "neutral" in settings

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
        default="https://sisbot-ai-service.uc.r.appspot.com/get_mood_coordinates_from_audio_stream",
        help="URL for AI Service"
    )
    client_args.add_argument(
        '-ts',
        '--tableservice',
        type=str,
        default="http://seniordesigntable.msoe.edu:3002/sisbot/set_led_color",
        help="The port that the sisbot server is using on the table"
    )
    return client_args.parse_args()


# TODO - move to own module
def call_listen():
    listen(app.config['sampling_rate'], app.config['record_seconds'], app.config['ai_service'], app.config['table_service'])

if __name__ == '__main__':
    args = parse_arguments()
    app.config['record_seconds'] = args.seconds
    app.config['sampling_rate'] = args.samplingrate
    app.config['ai_service'] = args.aiservice
    app.config['table_service'] = args.tableservice

    global scheduler
    scheduler = Scheduler(5, call_listen)

    flask_env = os.environ.get('FLASK_ENV')
    if flask_env is not None and flask_env.lower() == 'production':
        serve(app, host='127.0.0.1', port=5000, threads=6)
    else:
        app.run(debug=True)

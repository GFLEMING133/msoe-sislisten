import io
import pyaudio
import requests
import color_map_2d
import numpy
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from translator import translate_coordinates_to_color
from communicator import communicate_color_to_table

input_stream = None
executor = ThreadPoolExecutor(5)

# def pipeline(audio_sample, ai_service, table_service):
#     response = call_mood_lighting_ai_service(audio_sample, ai_service)
#     communicate_color_to_table(response["result"], table_service)


def call_mood_lighting_ai_service(audio_sample, ai_service):
    """
    Helper method for the read_from_input_device task which
     is used for calling the AI service
    """
    request_headers = { 'Content-Type': 'application/octet-stream' }
    data = { 'audioSample': audio_sample }
    response = requests.post(ai_service, data=data)
    if response.status_code == requests.codes.ok:
        response = response.json()
    else:
        print(f'Error in AI Service call - code: {response.status_code}')
        response = 'ERR'
    return response


def listen(sampling_rate, record_seconds, ai_service, table_service):
    """
    Task which reads in audio samples and starts off threads
     to handle the responses
    """
    global input_stream, executor
    buffer_size = sampling_rate * record_seconds
    print('buffer size ' + str(buffer_size))

    if not input_stream:
        pa = pyaudio.PyAudio()
        print(sampling_rate)
        print(record_seconds)
        input_stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sampling_rate,
            input=True,
            frames_per_buffer=buffer_size
        )

    data_bytes = input_stream.read(buffer_size)
    audio_sample = io.BytesIO(data_bytes)
    print("Got Color!")
    response = call_mood_lighting_ai_service(audio_sample, ai_service)
    if response != 'ERR':
        communicate_color_to_table(response["result"], table_service)


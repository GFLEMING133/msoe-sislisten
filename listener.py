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


def call_mood_lighting_ai_service(audio_sample, ai_service):
    """
    Helper method for the read_from_input_device task which
     is used for calling the AI service
    """
    request_headers = { 'Content-Type': 'application/octet-stream' }
    data = { 'audioSample': audio_sample }
    response = requests.post(ai_service, data=data)
    # Raise an error if the response returns an error
    response.raise_for_status()
    response = response.json()
    color = translate_coordinates_to_color(response)
    communicate_color_to_table(color)

def listen(sampling_rate, record_seconds):
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
    data_stream = io.BytesIO(data_bytes)

    executor.submit(call_mood_lighting_ai_service, audio_sample)


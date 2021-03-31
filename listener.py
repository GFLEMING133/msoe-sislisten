import io
import pyaudio
import requests
import color_map_2d
import numpy
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from translator import translate_coordinates_to_color
from communicator import communicate_color_to_table
import datetime

input_stream = None
executor = ThreadPoolExecutor(5)

def pipeline(data_stream, ai_service, table_service):
    """
    This method serves as the main pipeline for a single thread from the thread pool
    """
    request_headers = { 'Content-Type': 'application/octet-stream' }
    request_data = data_stream
    pre_request = datetime.datetime.now()
    print(f'Sending request @ {pre_request}')
    ai_response = requests.post(
        ai_service,
        headers=request_headers,
        data=request_data
    )

    if ai_response.status_code != requests.codes.ok:
        print(f'Error in sending AI request - code: {ai_response.status_code}')
        print(ai_response.text)
    else:
        print(f'Recieved response @ {datetime.datetime.now()}')
        rgb = ai_response.json()['result']
        print(ai_response.json())
        led_info = { "led_primary_color": rgb }
        wrapper = { 'data': { 'data' : led_info } }
        table_response = requests.post(table_service, json=wrapper)
        if table_response.status_code == requests.codes.ok:
            print(f'Successfully updated color to {rgb}')
        else:
            print(
                f'Error in table request - code: {table_response.status_code}'
            )

def call_mood_lighting_ai_service(audio_sample, ai_service):
    """
    Helper method for the read_from_input_device task which
     is used for calling the AI service
    """
    request_headers = { 'Content-Type': 'application/octet-stream' }
    data = { 'audioSample': audio_sample }
    response = requests.post(ai_service, headers=request_headers, data=data)
    if response.status_code != requests.codes.ok:
        print(f'Error in sending AI request - code: {response.status_code}')
        print(response.text)
        return -1
    else:
        print(response)
        return response.json()


def listen(sampling_rate, record_seconds, ai_service, table_service):
    """
    Task which reads in audio samples and starts off threads
     to handle the responses
    """
    #global input_stream, executor
    buffer_size = sampling_rate * record_seconds
    print('buffer size ' + str(buffer_size))

    pa = pyaudio.PyAudio()
    input_stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sampling_rate,
        input=True,
        frames_per_buffer=buffer_size
    )
    data_bytes = input_stream.read(buffer_size)
    data_stream = io.BytesIO(data_bytes)
    #pipeline(data_stream, ai_service, table_service)
    executor.submit(pipeline, data_stream, ai_service, table_service)
    

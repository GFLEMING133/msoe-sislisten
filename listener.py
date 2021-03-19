import io
import pyaudio
import requests
import color_map_2d
import numpy

input_stream = None


def call_mood_lighting_ai_service(audio_sample, ai_service):
    """
    Helper method for the read_from_input_device task which is used for calling the AI service
    """
    request_headers = { 'Content-Type': 'application/octet-stream' }
    data = { 'audioSample': audio_sample }
    response = requests.post(ai_service, data=data)
    # Raise an error if the response returns an error
    response.raise_for_status()
    return response.json()


def read_from_input_device(sampling_rate, record_seconds, color_coordinate_queue):
    """
    Periodic task which reads in audio samples and adds them to the sample queue
    """
    global input_stream
    buffer_size = sampling_rate * record_seconds
    if not input_stream:
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
    ai_service_response = call_mood_lighting_ai_service(audio_sample)
    return ai_service_response

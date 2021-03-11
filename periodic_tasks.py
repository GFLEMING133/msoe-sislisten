import requests
import io
from queue import Queue
import pyaudio

audio_sample_queue = Queue()
input_stream = None

def call_mood_lighting_ai_service(audio_sample, ai_service):
    request_headers = { 'Content-Type': 'application/octet-stream' }
    data = { 'audioSample': audio_sample }
    response = requests.post(ai_service, data=data)
    # Raise an error if the response returns an error
    response.raise_for_status()
    return response.json()

def translate_audio_to_color(ai_service):
    """
    Periodic task which takes audio samples off of the queue and translates the audio to a color.
    """
    global audio_sample_queue
    if not audio_sample_queue.empty():
        audio_sample = audio_sample_queue.get()
        ai_service_response = call_mood_lighting_ai_service(audio_sample)
        # TODO: Using the info in the response translate the response into a color and call the sisbot endpoint to change the color.

def read_from_input_device(sampling_rate, record_seconds):
    """
    Periodic task which reads in audio samples and adds them to the sample queue
    """
    global audio_sample_queue, input_stream
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
    audio_sample_queue.put(data_stream)

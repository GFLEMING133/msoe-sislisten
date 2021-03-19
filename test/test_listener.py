import pytest
from listener import call_mood_lighting_ai_service
from assertpy import assert_that
import wave

@pytest.fixture
def ai_service():
    return 'https://sisyphus-mood-lighting-server.herokuapp.com/get_mood_color_from_audio_stream'

@pytest.fixture
def audio_sample():
    with wave.open('test/count.wav', 'r') as audio_file:
        return audio_file.readframes(audio_file.getnframes())

class TestListener:

    def test_ai_service_should_returns_valid_responses_when_requests_are_sent_to_the_service(self, ai_service, audio_sample):
        # Act
        response = call_mood_lighting_ai_service(audio_sample, ai_service)

        # Assert
        assert_that(response).is_not_none
        assert_that(response).is_type_of(dict)
        assert_that(response).contains_key('result')
        assert_that(response['result']).is_type_of(str)
import pytest
import server
from color_settings import Color_Settings
import json
from assertpy import assert_that

@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as test_client:
        yield test_client

class TestServer:
    INVALID_SETTINGS_TYPE_DATA = [
        (1),
        ([1, 2, 3])
    ]
    INVALID_COLOR_DATA = [
        (1),
        ({'1': 1}),
        ([1, 1]),
        (['0', 0, 0]),
        ([-1, 0, 0]),
        ([257, 0, 0]),
        ([0, '0', 0]),
        ([0, -1, 0]),
        ([0, 257, 0]),
        ([0, 0, '0']),
        ([0, 0, -1]),
        ([0, 0, 257])
    ]
    INCOMPLETE_SETTINGS_DATA = [
        ({
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "neutral": [0, 0, 0]
        }),
        ({
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
        })
    ]

    def test_get_settings_should_return_not_set_message_when_settings_are_not_set(self, client):
        # Act
        response = client.get('/mood_lighting_settings')
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(200)
        assert_that(json_response['message']).is_equal_to('Settings not set')

    def test_get_settings_should_return_settings_from_object_when_endpoint_is_called(self, client):
        # Arrange
        settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(settings)

        # Act
        response = client.get('/mood_lighting_settings')
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(200)
        assert_that(json_response['settings']).is_equal_to(settings)
    
    def test_update_settings_should_update_settings_in_object_when_setting_values_are_valid(self, client):
        # Arrange
        old_settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [123, 234, 123],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(old_settings)

        settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }

        # Act
        response = client.post('/mood_lighting_settings', json={'settings': settings})
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(200)
        assert_that(json_response['message']).is_equal_to('Settings applied!')
        assert_that(Color_Settings().color_dictionary).is_equal_to(settings)

    def test_update_settings_should_return_error_when_settings_key_is_not_found_on_request(self, client):
        # Arrange
        old_settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [123, 234, 123],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(old_settings)

        settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [0, 0, 0],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }

        # Act
        response = client.post('/mood_lighting_settings', json=settings)
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(400)
        assert_that(json_response['error']).is_equal_to('No settings were found on the request')
        assert_that(Color_Settings().color_dictionary).is_equal_to(old_settings)

    @pytest.mark.parametrize("settings_data", INVALID_SETTINGS_TYPE_DATA)
    def test_update_settings_should_return_error_when_settings_object_is_a_invalid_type(self, client, settings_data):
        # Arrange
        old_settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [123, 234, 123],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(old_settings)

        # Act
        response = client.post('/mood_lighting_settings', json={'settings': 1})
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(400)
        assert_that(json_response['error']).is_equal_to('Settings request object is not a valid type')
        assert_that(Color_Settings().color_dictionary).is_equal_to(old_settings)

    @pytest.mark.parametrize("color_value", INVALID_COLOR_DATA)
    def test_update_settings_should_return_error_when_color_value_is_invalid(self, client, color_value):
        # Arrange
        old_settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [123, 234, 123],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(old_settings)

        # Act
        response = client.post('/mood_lighting_settings', json={'settings': {'disgust': color_value}})
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(400)
        assert_that(json_response['error']).is_equal_to(f'The emotion disgust has the invalid color value {color_value}')
        assert_that(Color_Settings().color_dictionary).is_equal_to(old_settings)

    @pytest.mark.parametrize("settings_value", INCOMPLETE_SETTINGS_DATA)
    def test_update_settings_should_return_error_when_not_all_emotions_are_provided(self, client, settings_value):
        # Arrange
        old_settings = {
            "disgust" : [255, 165, 0],
            "anger": [0, 0, 0],
            "alert": [0, 0, 0],
            "happy": [123, 234, 123],
            "calm": [0, 0, 0],
            "relaxed": [0, 0, 0],
            "sad": [0, 0, 0],
            "neutral": [0, 0, 0]
        }
        Color_Settings(old_settings)

        # Act
        response = client.post('/mood_lighting_settings', json={'settings': settings_value})
        json_response = json.loads(response.get_data(as_text=True))

        # Assert
        assert_that(response.status_code).is_equal_to(400)
        assert_that(json_response['error']).is_equal_to('Incomplete settings. Need emotions disgust, anger, alert, happy, calm, relaxed, sad and neutral.')
        assert_that(Color_Settings().color_dictionary).is_equal_to(old_settings)

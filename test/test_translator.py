import pytest
from translator import translate_coordinates_to_color, are_valid_coordinates
from assertpy import assert_that
from color_settings import Color_Settings
import wave

@pytest.fixture
def color_settings_default():
    settings = {
        "disgust" : [128, 0, 128],
        "angry": [255, 0, 0],
        "alert": [255, 165, 0],
        "happy": [255, 255, 0],
        "calm": [0, 205, 0],
        "relaxed": [0, 165, 255],
        "sad": [0, 0, 255],
        "neutral": [255, 241, 224]
    }

    Color_Settings(settings)

@pytest.fixture
def color_settings_flipped():
    settings = {
        "neutral" : [255, 165, 0],
        "sad": [0, 0, 255],
        "relaxed": [0, 165, 255],
        "calm": [0, 255, 0],
        "happy": [255, 0, 0],
        "alert": [255, 255, 0],
        "angry": [128, 0, 128],
        "disgust": [255, 241, 224]
    }

    Color_Settings(settings)

class TestTranslator:
    VALID_COORDINATES = [
        ([-1, -1, '00']),
        ([1, 1, 'FF'])
    ]
    INVALID_COORDINATES = [
        ([-1.01, 0, '00']),
        ([1.01, 0, '00']),
        (['1.01', 0, '00']),
        ([{'a': 1.01}, 0, '00']),
        ([None, 0, '00']),
        ([0, -1.01, '00']),
        ([0, 1.01, '00']),
        ([0, '1.01', '00']),
        ([0, {'a': 1.01}, '00']),
        ([0, None, '00']),
        ([0, 0, '-1']),
        ([0, 0, '100']),
        ([0, 0, 0]),
        ([0, 0, {'a': 1.01}]),
        ([0, 0, None]),
    ]
    def test_translate_cords_to_color_without_settings(self):
        # Arrange
        response = {"valence": 0.5, "energy": 0.81, "alpha" : 'FF'}

        # Act
        color = translate_coordinates_to_color(**response)

        # Assert
        assert_that(color).is_not_none()
        assert_that(color).is_type_of(str)
        assert_that(len(color)).is_equal_to(9)
        assert_that(color[:1]).is_equal_to('#')
    
    @pytest.mark.usefixtures("color_settings_default")
    def test_translate_cords_to_color_with_settings(self):
        # Arrange
        response = {"valence": 0.5, "energy": 0.81, "alpha" : 'FF'}

        # Act
        color_from_settings = translate_coordinates_to_color(**response)

        Color_Settings().reset()
        color_no_settings = translate_coordinates_to_color(**response)

        # Assert - first that responses are valid
        assert_that(color_from_settings).is_not_none()
        assert_that(color_from_settings).is_type_of(str)
        assert_that(len(color_from_settings)).is_equal_to(9)
        assert_that(color_from_settings[:1]).is_equal_to('#')

        assert_that(color_no_settings).is_not_none()
        assert_that(color_no_settings).is_type_of(str)
        assert_that(len(color_no_settings)).is_equal_to(9)
        assert_that(color_no_settings[:1]).is_equal_to('#')

        # and then assert that the color matches the result when no settings are applied
        assert_that(color_from_settings).is_equal_to(color_no_settings)

    @pytest.mark.usefixtures("color_settings_flipped")
    def test_translate_cords_to_color_with_flipped_settings(self):
        # Arrange
        response = {"valence": 0.5, "energy": 0.81, "alpha" : 'FF'}

        # Act
        color_from_settings = translate_coordinates_to_color(**response)

        Color_Settings().reset()
        color_no_settings = translate_coordinates_to_color(**response)

        # Assert - first that responses are valid
        assert_that(color_from_settings).is_not_none()
        assert_that(color_from_settings).is_type_of(str)
        assert_that(len(color_from_settings)).is_equal_to(9)
        assert_that(color_from_settings[:1]).is_equal_to('#')

        assert_that(color_no_settings).is_not_none()
        assert_that(color_no_settings).is_type_of(str)
        assert_that(len(color_no_settings)).is_equal_to(9)
        assert_that(color_no_settings[:1]).is_equal_to('#')

        # and then assert that the color does not match the result when no settings are applied
        assert_that(color_from_settings).is_not_equal_to(color_no_settings)

    @pytest.mark.parametrize('coords', VALID_COORDINATES)
    def test_are_coordinates_valid_valid_result(self, coords):
        # act
        is_valid = are_valid_coordinates(coords)
        
        # assert
        assert_that(is_valid).is_true()

    @pytest.mark.parametrize('coords', INVALID_COORDINATES)
    def test_are_coordinates_valid_valid_result(self, coords):
        # act
        is_valid = are_valid_coordinates(coords)
        
        # assert
        assert_that(is_valid).is_false()


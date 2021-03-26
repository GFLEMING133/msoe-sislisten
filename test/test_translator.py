import pytest
from translator import translate_coordinates_to_color
from assertpy import assert_that
import wave

class TestTranslator:
    def test_translate_cords_to_color(self):

        # Arrange
        response = {"valence": 0.5, "energy": 0.81, "alpha" : 1.0}

        # Act
        color = translate_coordinates_to_color(response)

        # Assert
        assert_that(color).is_not_none()
        assert_that(color).is_type_of(str)
        assert_that(len(color)).is_equal_to(9)
        assert_that(color[:1]).is_equal_to('#')
import color_map_2d
import numpy
from color_settings import Color_Settings

def translate_coordinates_to_color(valence, energy, alpha):
    """
    Takes mood coordinates and translates the coordinates to a color.
    """
    grid = (622, 622, 0)

    settings = Color_Settings().color_dictionary
    disgust_pos = [-0.9, 0]
    angry_pos = [-0.5, 0.5]
    alert_pos = [0, 0.6]
    happy_pos = [0.5, 0.5]
    calm_pos = [0.4, -0.4]
    relaxed_pos = [0, -0.6]
    sad_pos = [-0.5, -0.5]
    neu_pos = [0.0, 0.0]

    if not settings:
        colors = {
                "orange": [255, 165, 0],
                "blue": [0, 0, 255],
                "bluegreen": [0, 165, 255],
                "green": [0, 205, 0],
                "red": [255, 0, 0],
                "yellow": [255, 255, 0],
                "purple": [128, 0, 128],
                "neutral": [255, 241, 224]
        }

        emo_map = color_map_2d.create_2d_color_map(
            [disgust_pos,
            angry_pos,
            alert_pos,
            happy_pos,
            calm_pos,
            relaxed_pos,
            sad_pos,
            neu_pos],
            [colors["purple"],
            colors["red"],
            colors["orange"],
            colors["yellow"],
            colors["green"],
            colors["bluegreen"],
            colors["blue"],
            colors["neutral"]],
            grid[0], grid[1])
    else:
        emo_map = color_map_2d.create_2d_color_map(
            [disgust_pos,
            angry_pos,
            alert_pos,
            happy_pos,
            calm_pos,
            relaxed_pos,
            sad_pos,
            neu_pos],
            [settings["disgust"],
            settings["angry"],
            settings["alert"],
            settings["happy"],
            settings["calm"],
            settings["relaxed"],
            settings["sad"],
            settings["neutral"]],
            grid[0], grid[1])

    h, w, _ = grid
    y_center, x_center = int(h / 2), int(w / 2)
    x = x_center + int((w/2) * valence)
    y = y_center - int((h/2) * energy)

    color = numpy.median(emo_map[y-2:y+2, x-2:x+2], axis=0).mean(axis=0)
    response = "#" + format(int(color[0]), '02x') + format(int(color[1]), '02x') + format(int(color[2]), '02x') + '00'
    print(response)
    return response

def are_valid_coordinates(coordinates):
    """
    Validates alpha, valence, and energy for length, type and range
    """
    if len(coordinates) == 3:
        valence = coordinates[0]
        energy = coordinates[1]
        alpha = coordinates[2]

        valence_is_number = type(valence) is int or type(valence) is float
        energy_is_number = type(energy) is int or type(energy) is float
        alpha_is_string = type(alpha) is str
        if alpha_is_string and valence_is_number and energy_is_number:
            alpha_in_dec = int(alpha, 16)
            alpha_is_valid = 0 <= alpha_in_dec <= 255

            return alpha_is_valid and valence >= -1 and valence <= 1 and energy >= -1 and energy <= 1
    print(coordinates)
    return False


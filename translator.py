import color_map_2d
import numpy

def translate_coordinates_to_color(response, settings=None):
    """
    Takes mood coordinates and translates the coordinates to a color.
    """
    if (settings is not None):
        # TODO once user settings are being returned from the server
        print("User settings found!")

    soft_valence = response["valence"]
    soft_energy = response["energy"]
    alpha = response["alpha"]  # will come from volume of audio

    grid = (622, 622, 0)
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

    disgust_pos = [-0.9, 0]
    angry_pos = [-0.5, 0.5]
    alert_pos = [0, 0.6]
    happy_pos = [0.5, 0.5]
    calm_pos = [0.4, -0.4]
    relaxed_pos = [0, -0.6]
    sad_pos = [-0.5, -0.5]
    neu_pos = [0.0, 0.0]

    emo_map = color_map_2d.create_2d_color_map([disgust_pos,
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

    h, w, _ = grid
    y_center, x_center = int(h / 2), int(w / 2)
    x = x_center + int((w/2) * soft_valence)
    y = y_center - int((h/2) * soft_energy)

    color = numpy.median(emo_map[y-2:y+2, x-2:x+2], axis=0).mean(axis=0)
    response = "#" + format(int(color[2]), '02x') + format(int(color[1]), '02x') + format(int(color[0]), '02x') + format(int(alpha), '02x')
    print(response)
    return response
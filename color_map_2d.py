import numpy as np
import scipy.spatial
import operator
import math

def calculate_distance_between_points(first_point, second_point):
    return math.sqrt( ((first_point[0]-second_point[0])**2)+((first_point[1]-second_point[1])**2) )

def is_valid_center_point(point_coords):
    return -0.1 < point_coords[0] < 0.1 and -0.1 < point_coords[1] < 0.1

# Note this method was rewritten from the original implementation to make the colors stand out more on the sisyphus table.
# It's gets the color based on the shortest distance from the mood center and it only uses the colors specificed for the given moods
# instead of interoplating between the colors.

# If for any reason the original implementation is needed it can be viewed here: https://github.com/tyiannak/color_your_music_mood/blob/master/color_map_2d.py
def get_color_for_point(point_cords, list_of_point_centers, list_of_colors):
    if is_valid_center_point(point_cords):
        color_index = list_of_point_centers.index([0.0, 0.0])
        return list_of_colors[color_index]
    distances = []
    for i in range(len(list_of_point_centers)):
        point_center = list_of_point_centers[i]
        is_point_at_origin = point_center[0] == 0.0 and point_center[1] == 0.0
        if not is_point_at_origin:
            distances.append((i, calculate_distance_between_points(point_cords, point_center)))
    min_distance_tuple = min(distances, key=operator.itemgetter(1))
    return list_of_colors[min_distance_tuple[0]]

def create_2d_color_map(list_of_points, list_of_colors, height, width):
    """
    create_2d_color_map() creates a colormap by interpolating RGB color values,
    given a list of colors to be defined on particular points of the 2D
    plane.
    :param list_of_points: list of point coodinates
    [[x1, y1], ..., [xN, yN] of the of the aforementioned colors
    :param list_of_colors: list of RGB color values [[R1, G1, B1], ...,
    [RN, GN, BN]] for the N points in the 2D plane (see prev atribute)
    :param height: output image height
    :param width:  output image weight
    :return: estimated color image
    """
    rgb = np.zeros((height, width, 3)).astype("uint8")
    c_x = int(width / 2)
    c_y = int(height / 2)
    step = 5
    win_size = int((step-1) / 2)
    for i in range(len(list_of_points)):
        rgb[c_y - int(list_of_points[i][1] * height / 2),
            c_x + int(list_of_points[i][0] * width / 2)] = list_of_colors[i]
    for y in range(win_size, height - win_size, step):
        for x in range(win_size, width - win_size, step):
            x_real = (x - width / 2) / (width / 2)
            y_real = (height / 2 - y ) / (height / 2)
            color = get_color_for_point([x_real, y_real], list_of_points,
                                        list_of_colors)
            rgb[y - win_size - 1 : y + win_size + 1,
                x - win_size - 1 : x + win_size + 1] = color
    bgr = rgb
    return bgr


if __name__ == "__main__":
    colors = {"coral": [255,127,80],
              "pink": [255, 192, 203],
              "orange": [255, 165, 0],
              "blue": [0, 0, 205],
              "green": [0, 205, 0],
              "red": [205, 0, 0],
              "yellow": [204, 204, 0]}
    angry_pos = [-0.8, 0.5]
    fear_pos = [-0.3, 0.8]
    happy_pos = [0.6, 0.6]
    calm_pos = [0.4, -0.5]
    sad_pos = [-0.6, -0.4]
    bgr = create_2d_color_map([angry_pos, fear_pos, happy_pos,
                               calm_pos, sad_pos],
                              [colors["red"],  colors["yellow"],
                               colors["orange"], colors["green"],
                               colors["blue"]], 200, 200)

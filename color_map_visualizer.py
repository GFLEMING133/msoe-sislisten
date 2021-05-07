"""
This tool is a development tool used for visualizing the color map used for mood lighting.
Note you will need opncv installed in order for this to work. We don't have this in the requirements.txt
file since opencv is a big install and we don't use it anywhere except for this development tool.
"""
import cv2
import color_map_2d

if __name__ == '__main__':
    grid = (622, 622, 0)
    disgust_pos = [-0.9, 0]
    angry_pos = [-0.5, 0.5]
    alert_pos = [0, 0.6]
    happy_pos = [0.5, 0.5]
    calm_pos = [0.4, -0.4]
    relaxed_pos = [0, -0.6]
    sad_pos = [-0.5, -0.5]
    neu_pos = [0.0, 0.0]

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

    img = cv2.cvtColor(cv2.imread("music_color_mood.png"), cv2.COLOR_BGR2RGB)
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
    emo_map_img = cv2.cvtColor(emo_map, cv2.COLOR_BGR2RGB)
    cv2.imshow('Emotion Color Map', emo_map_img)
    cv2.waitKey()

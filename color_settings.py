import color_map_2d
import numpy

class Color_Settings(object):
    """ This is a singleton object for user settings """
    
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Color_Settings.__instance:
            Color_Settings.__instance = object.__new__(cls)
            Color_Settings.__instance.color_dictionary = None
        return Color_Settings.__instance

    def __init__(self, settings_dictionary=None):
        if settings_dictionary != None:
            self.color_dictionary = settings_dictionary

    def reset(self):
        self.color_dictionary = None

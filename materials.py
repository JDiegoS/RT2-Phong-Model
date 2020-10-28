from lib import color

class Material(object):
    def __init__(self, diffuse):
        self.diffuse = diffuse

ivory = Material(diffuse=color(100, 100, 80))
black = Material(diffuse=color(0, 0, 0))
white = Material(diffuse=color(255, 255, 255))
orange = Material(diffuse=color(255, 128, 0))
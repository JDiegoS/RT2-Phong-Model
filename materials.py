from lib import color

class Material(object):
    def __init__(self, diffuse):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec

#albedo (color base, especular)
#spec = Intensidad con la que baja la luz
ivory = Material(diffuse=color(100, 100, 80), albedo=(0.6, 0.4), spec=50)
black = Material(diffuse=color(0, 0, 0), albedo=(0, 0), spec=0)
white = Material(diffuse=color(255, 255, 255), albedo=(0, 0), spec=0)
orange = Material(diffuse=color(255, 128, 0), albedo=(0.2, 0.8), spec=10)

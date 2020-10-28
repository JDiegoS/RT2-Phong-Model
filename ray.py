#Juan Diego Solorzano 18151
#RT2: Phong Model

import random
from math import tan, pi
from sphere import Sphere
from lib import *
from materials import *

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clearC = black
        self.current_color = white
        self.scene = []
        self.light = None
        self.clear()

    def glInit(self, width, height):
        return

    #Area para pintar
    def glViewPort(self, x, y, width, height):
        self.xw = x
        self.yw = y
        self.widthw = width
        self.heightw = height

    #Pintar imagen   
    def clear(self):
        self.framebuffer = [
            [black for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [[-float('inf') for x in range(self.width)] for y in range(self.height)]

    #Crear archivo de la imagen
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def display(self, filename='out.bmp'):
        """
        Displays the image, a external library (wand) is used, but only for convenience during development
        """
        self.render()
        self.write(filename)

        try:
            from wand.image import Image
            from wand.display import display

            with Image(filename=filename) as image:
                display(image)
        except ImportError:
            pass  # do nothing if no wand is installed

    #Pintar punto
    def point(self, x, y, color = None):
        try:
            self.framebuffer[y][x] = color or self.current_color
        except:
            pass
    
    #Ver si hay objeto y donde
    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, direction)
            if hit is None: 
                if hit.distance < zbuffer:
                    zbiffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect
    
    #Renderizar con material
    def cast_ray(self, orig, direction):
        impacted_material, intersect = self.scene_intersect(orig, direction)
        if impacted_material is None:
            return self.clearC

        light_dir = norm(sub(self.light.position, intersect.point))
        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal))

        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
        max(0, -dot(reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        return diffuse + specular


    def render(self):
      #field of view
      fov = int(pi/2)

      for y in range(self.height):
        for x in range(self.width):
          i = (2 * (x + 0.5)/self.width - 1) * self.width/self.height * tan(fov/2)
          j = (1 - 2 * (y + 0.5)/self.height) * tan(fov/2)

          direction = norm(V3(i, j, -1))
          self.framebuffer[y][x] = self.cast_ray(V3(0, 0, 0), direction)
r = Raytracer(1000, 1000)
r.scene = [
    #Face
    Sphere(V3(0, -3, -10), 0.2, orange),
    Sphere(V3(0.5, -3.5, -10), 0.1, black),
    Sphere(V3(-0.5, -3.5, -10), 0.1, black),
    #Smile
    Sphere(V3(-0.5, -2.5, -10), 0.1, black),
    Sphere(V3(-0.2, -2.4, -10), 0.1, black),
    Sphere(V3(0.2, -2.4, -10), 0.1, black),
    Sphere(V3(0.5, -2.5, -10), 0.1, black),
    #Buttons
    Sphere(V3(0, 0, -10), 0.3, black),
    Sphere(V3(0, 1.5, -10), 0.3, black),
    Sphere(V3(0, 3, -10), 0.3, black),
    #Body
    Sphere(V3(0, 3, -10), 2.5, white),
    Sphere(V3(0, 0, -10), 2, white),
    Sphere(V3(0, -3, -10), 1.5, white)

    
]
r.display()
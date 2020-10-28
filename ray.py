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
        light_distance = length(sub(self.light.position, intersect.point))

        #Offset para que no choque con si mismo
        offset_normal = mul(intersect.normal, 1.1)

        if dot(light_dir, intersect.normal) < 0:
            shadow_orig = sub(intersect.point, offset_normal)
        else:
            shadow_orig = sum(intersect.point, offset_normal)
        
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        shadow_intensity = 0

        if shadow_intersect and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
            #esta en la sombra
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)
        
        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (max(0, dot(reflection, direction))**impacted_material.spec)

        diffuse = impacted_material.diffuse * intensity * impacted_material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * impacted_material.albedo[1]
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

r.light = Light(
    color = color(255, 255, 255),
    position = V3(-20, 20, 20),
    intensity = 1.5
)
r.scene = [
    #Face
    Sphere(V3(0, -1.5, -10), 0.2, orange),
    Sphere(V3(1, -1, -12), 0.1, ivory),
    Sphere(V3(-2, 2, -10), 0.1, black),
]
r.display()
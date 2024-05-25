"""
display a single object, inert, at (100, 100)
"""

import math

import arcade

BACKGROUND = arcade.color.ALMOND
IMAGE = "media/arrow-resized.png"
WIDTH, HEIGHT = 800, 800

class Boid(arcade.Sprite):

    def __init__(self):
        super().__init__(IMAGE)
        self.center_x, self.center_y = 100, 100
        self.angle = -135
        self.speed = 100  # in pixels / second

    def on_update(self, delta_time):
        self.center_x += self.speed * delta_time * math.cos(math.radians(self.angle))
        self.center_y += self.speed * delta_time * math.sin(math.radians(self.angle))

        self.center_x %= WIDTH
        self.center_y %= HEIGHT


class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "My first boid")
        arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.boids = None

    def setup(self):
        boid = Boid()
        self.boids = arcade.SpriteList()
        self.boids.append(boid)

    def on_draw(self):
        arcade.start_render()
        self.boids.draw()

    def on_update(self, delta_time):
        self.boids.on_update(delta_time)

window = Window()
window.setup()
arcade.run()

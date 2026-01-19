"""
simplest possible starting code with one motionless boid
display a single object, inert, at (100, 100)
with arcade-3.x this is the starter step, and
Window has a self.boids instead of a single self.boid
"""

import arcade

BACKGROUND = arcade.color.ALMOND
IMAGE = "media/arrow-resized.png"

class Window(arcade.Window):

    def __init__(self):
        super().__init__(800, 800, "My first boid")
        arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.boids = None

    def setup(self):
        boid = arcade.Sprite(IMAGE)
        boid.center_x = 100
        boid.center_y = 100
        self.boids = arcade.SpriteList()
        self.boids.append(boid)

    def on_draw(self):
        self.clear()
        self.boids.draw()

    def on_update(self, delta_time):
        self.boids.update()

window = Window()
window.setup()
arcade.run()

"""
display a single object, inert, at (100, 100)
"""

import arcade

BACKGROUND = arcade.color.ALMOND
IMAGE = "media/arrow-resized.png"

class Window(arcade.Window):

    def __init__(self):
        super().__init__(800, 800, "My first boid")
        arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.boid = None

    def setup(self):
        boid = arcade.Sprite(IMAGE)
        boid.center_x = 100
        boid.center_y = 100
        self.boid = boid

    def on_draw(self):
        arcade.start_render()
        self.boid.draw()

    def on_update(self, delta_time):
        self.boid.update()

window = Window()
window.setup()
arcade.run()

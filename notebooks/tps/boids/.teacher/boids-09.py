"""
display a single object, inert, at (100, 100)
"""

import math
import random

import arcade

BACKGROUND = arcade.color.ALMOND
IMAGE = "media/arrow-resized.png"
WIDTH, HEIGHT = 800, 800

NOISE_ANGLE = 1     # in degrees

# obstacles
OBSTACLE_IMAGE = "media/obstacle-resized.png"
# add 10 x 10 obstacles
OBSTACLE_GRID = 10

OBSTACLE_RADIUS = 20

class Obstacle(arcade.Sprite):

    def __init__(self, cx, cy):
        super().__init__(OBSTACLE_IMAGE)
        self.center_x, self.center_y = cx, cy


class Boid(arcade.Sprite):

    def __init__(self, obstacles):
        super().__init__(IMAGE)
        self.center_x, self.center_y = 100, 100
        self.angle = -135
        self.speed = 100  # in pixels / second
        self.steer = 0
        self.obstacles = obstacles

    def on_update(self, delta_time):

        for o in self.obstacles:
            if math.dist((self.center_x, self.center_y),
                         (o.center_x, o.center_y)) <= OBSTACLE_RADIUS:
                         self.alpha = 100
                         break
        else:
            self.alpha = 255

        self.angle += self.steer

        self.angle += (1 - 2*random.random()) * NOISE_ANGLE

        self.center_x += self.speed * delta_time * math.cos(math.radians(self.angle))
        self.center_y += self.speed * delta_time * math.sin(math.radians(self.angle))

        self.center_x %= WIDTH
        self.center_y %= HEIGHT

    def left(self):
        self.steer = 1
    def right(self):
        self.steer = -1
    def steer_neutral(self):
        self.steer = 0


class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "My first boid")
        arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.boids = None
        self.obstacles = None

    def setup(self):
        self.boids = arcade.SpriteList()
        self.obstacles = arcade.SpriteList()
        boid = Boid(self.obstacles)
        self.boids.append(boid)
        for i in range(OBSTACLE_GRID):
            for j in range(OBSTACLE_GRID):
                ox = int((i+0.5) * WIDTH/OBSTACLE_GRID)
                oy = int((j+0.5) * HEIGHT/OBSTACLE_GRID)
                self.obstacles.append(Obstacle(ox, oy))

    def on_draw(self):
        arcade.start_render()
        self.boids.draw()
        self.obstacles.draw()

    def on_update(self, delta_time):
        self.boids.on_update(delta_time)
        self.obstacles.on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.boids[0].left()
        elif symbol == arcade.key.RIGHT:
            self.boids[0].right()
        else:
            return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.boids[0].steer_neutral()


window = Window()
window.setup()
arcade.run()

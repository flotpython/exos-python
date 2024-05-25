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

# the max. impact of avoidance on angle
MAX_ANGLE_CHANGE = 3


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


    def avoid_move(self) -> tuple[float, float]:
        """
        movement to avoid obstacles
        """
        move_x, move_y = 0., 0.
        for o in self.obstacles:
            d = math.dist((self.center_x, self.center_y),
                         (o.center_x, o.center_y))
            if d <= OBSTACLE_RADIUS:
                # implement repel function
                # alpha is between 0 (for d == OBSTACLE_RADIUS)
                # and 1/2 (for d == 0)
                alpha = (OBSTACLE_RADIUS-d)/(2*d)
                move_x += alpha*(self.center_x-o.center_x)
                move_y += alpha*(self.center_y-o.center_y)
        return move_x, move_y

    def on_update(self, delta_time):
        # convenience: do a atan2 but in degrees
        # and with args in the natural order X Y
        def angle_from_move(move_x, move_y):
            return 180/math.pi*math.atan2(move_y, move_x)

        # accumulate the move
        move_x, move_y = 0., 0.

        self.angle += self.steer
        self.angle += (1 - 2*random.random()) * NOISE_ANGLE

        # add our own speed
        move_x += self.speed * delta_time * math.cos(math.radians(self.angle))
        move_y += self.speed * delta_time * math.sin(math.radians(self.angle))

        avoid_x, avoid_y = self.avoid_move()
        move_x += avoid_x
        move_y += avoid_y

        # apply the move
        self.center_x += move_x
        self.center_y += move_y

        # compute new angle, with a cap on the impact this has on our angle
        # otherwise we get too sharp turns as this happens quite often
        new_angle = angle_from_move(move_x, move_y)
        self.angle = max(self.angle-MAX_ANGLE_CHANGE,
                         min(self.angle+MAX_ANGLE_CHANGE, new_angle))

        # wrap around the edges
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

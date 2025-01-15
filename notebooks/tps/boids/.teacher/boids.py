"""
the boids with all 3 rules
as a convenience, one can
* click to add obstacles
* shift-click to remove obstacles
"""

import math
import random
import itertools
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import arcade
from arcade.sprite_list.sprite_list import SpriteList

from vector import Vector, distance_1, distance_2

## constants
# pylint: disable=global-statement
BACKGROUND = arcade.color.ALMOND

FONT_SIZE = 12
FONT_COLOR = arcade.color.BLACK

WIDTH, HEIGHT = 800, 800

# how many boids
NB_BOIDS = 50
BOID_SPEED = 3

# one boid
# arrow-resized:
# if you only have the resized version just use that with scale 1
BOID_IMAGE = "media/arrow-resized.png"
#BOID_SCALE = 0.12

### what is proximity
# close_flock is computed once per loop, with distance_1 (abs)
# should be larger than the largest radius * 1.4
CLOSE_RADIUS1 = 200

SEPARATION_RADIUS = 25
ALIGNMENT_RADIUS = 80
COHESION_RADIUS = 100
COHESION_RATIO = 0.02

# add to speed a noise vector picked randomly in a circle with this radius
NOISE_RADIUS = 0.05

# obstacles
OBSTACLE_IMAGE = "media/obstacle-resized.png"
#OBSTACLE_SCALE = 0.15

OBSTACLES_RADIUS = WIDTH / 2.8
NB_OBSTACLES = 30

# best if width - 2*gap
# and  if height - 2*gap
# are a  multiple of step
#OBSTACLE_GAP = 0
#OBSTACLE_STEP = 30
#WIDTH, HEIGHT = 30*OBSTACLE_STEP+2*OBSTACLE_GAP, 20*OBSTACLE_STEP+2*OBSTACLE_GAP

# enable or not the 3 rules
APPLY_SEPARATION = True
APPLY_ALIGNMENT = True
APPLY_COHESION = True
APPLY_NOISE = True

# slow down and print messages
DEBUG = False
SLOW = False

class Boid(arcade.Sprite):
    """
    each individual boid is represented by one instance of Boid
    """
    def __init__(self,
                 flock: SpriteList,
                 obstacles: SpriteList,
                 x=None, y=None, angle=None):
        """
        Parameters:
          flock, obstacles: references to the complete collection
            of boids and obstacles, respectively
          x, y: initial position, picked randomly if not set
          angle: initial angle, picked randomly if not set
        """
        super().__init__(BOID_IMAGE) #, BOID_SCALE)
        self.flock = flock
        self.obstacles = obstacles
        self.center_x = x if x is not None else random.random()*WIDTH
        self.center_y = y if y is not None else random.random()*HEIGHT
        self.angle = angle if angle is not None else 360 * random.random()
        # the boid's speed, exposed to other boids for the alignment rule
        self.move_x = BOID_SPEED*math.cos(math.radians(self.angle))
        self.move_y = BOID_SPEED*math.sin(math.radians(self.angle))
        # a cache of the entities that are close-by
        # will be computed at each update
        self.close_flock = None
        self.close_obstacles = None


    def __repr__(self):
        # just a simple way to identify each boid
        # based on its rank in the flock
        return f"boid #{self.flock.index(self)}"

    # 2 distances
    def distance_1(self, other: arcade.Sprite):
        """
        the distance to another Sprite using norm1
        """
        return distance_1((self.center_x, self.center_y),
                          (other.center_x, other.center_y))
    def distance_2(self, other):
        """
        the distance to another Sprite using norm2
        """
        return distance_2((self.center_x, self.center_y),
                          (other.center_x, other.center_y))

    def _close_by_distance(self, dist_method, sprites: SpriteList, radius):
        """
        iterator on neighbours in that list of sprites
        using the provided distance and a radius
        """
        for sprite in sprites:
            if dist_method(self, sprite) <= radius:
                yield sprite


    def close_by_1(self, sprites, radius):
        """
        an iterator on the sprites that are close-by using norm1
        """
        return self._close_by_distance(Boid.distance_1, sprites, radius)

    def close_by_2(self, sprites, radius):
        """
        an iterator on the sprites that are close-by using norm2
        """
        return self._close_by_distance(Boid.distance_2, sprites, radius)


    def separation_speed(self) -> Vector:
        """
        computes the impact on position (i.e. a dx, dy)
        resulting from the separation rule
        """
        move = Vector()
        # take into account both friend boids and obstacles
        for sprite in itertools.chain(self.close_flock, self.close_obstacles):
            # ignore self
            if sprite is self:
                continue
            dist = self.distance_2(sprite)
            # ignore boids that are too far
            if dist >= SEPARATION_RADIUS:
                continue
            repel = (  Vector(self.center_x, self.center_y)
                     - Vector(sprite.center_x, sprite.center_y))
            repel *= (1-dist/SEPARATION_RADIUS)/2
            # add all the repel forces
            move += repel
        return move


    def alignment_speed(self) -> Vector:
        """
        same for the alignment rule
        """
        move = Vector()
        count = 0
        # consider only other boids
        for friend in self.close_by_2(self.close_flock, ALIGNMENT_RADIUS):
            # ignore self
            if friend is self:
                continue
            move += Vector(friend.move_x, friend.move_y)
            count += 1
        # do not divide by zero
        return move if not count else move / count


    def cohesion_speed(self) -> Vector:
        """
        same for the cohesion rule
        """
        my_position = Vector(self.center_x, self.center_y)
        accumulated_position = Vector()
        count = 0
        # consider only other boids
        for friend in self.close_by_2(self.close_flock, COHESION_RADIUS):
            if friend is self:
                continue
            accumulated_position += Vector(friend.center_x, friend.center_y)
            count += 1
        mass_center = my_position if not count else accumulated_position / count
        return (mass_center - my_position) * COHESION_RATIO


    def noised_speed(self, speed) -> Vector:
        """
        the speed dx, dy obtained by the rule
        that adds a random noise to the current angle
        """
        # use a comple to compute the rotation
        angle = ( 1 +   NOISE_RADIUS*(1 - 2*random.random())
                + 1j * (NOISE_RADIUS*(1 - 2*random.random())))
        noised = (speed.x + 1j*speed.y) * angle
        return Vector(noised.real, noised.imag)


    def speed_limit(self, speed: Vector, limit) -> Vector:
        """
        given a speed vector, normalize it if necessary
        to comply with a speed limit
        """
        norm = speed.norm_2()
        if norm <= limit:
            return speed
        else:
            return speed * limit / norm


    def update(self):
        # compute the subset of the flock that is within CLOSE_RADIUS1
        # using norm_1 which is less cpu-consuming
        # using a list instead of a set could probably cut it too
        self.close_flock = set(self.close_by_1(self.flock, CLOSE_RADIUS1))
        # same for obstacles
        self.close_obstacles = set(self.close_by_1(self.obstacles, CLOSE_RADIUS1))

        # always apply own speed (inertia)
        move = Vector(self.move_x, self.move_y)

        # apply selected rules
        if APPLY_ALIGNMENT:
            move += self.alignment_speed()
        if APPLY_SEPARATION:
            move += self.separation_speed()
        if APPLY_COHESION:
            move += self.cohesion_speed()
        # add noise if selected
        if APPLY_NOISE:
            move = self.noised_speed(move)

        # align icon with actual move
        self.angle = move.degrees()
        if DEBUG:
            print(f"SUMMARY {self}: {move=} {self.angle=}")

        # speed limit
        move = self.speed_limit(move, 2 * BOID_SPEED)

        # record speed for next run
        self.move_x = move.x
        self.move_y = move.y

        # apply move
        self.center_x += move.x
        self.center_y += move.y

        # wrap into window
        self.center_x %= WIDTH
        self.center_y %= HEIGHT


class Obstacle(arcade.Sprite):
    """
    one per obstacle
    """
    def __init__(self, cx, cy):
        super().__init__(OBSTACLE_IMAGE) #, OBSTACLE_SCALE)
        self.center_x, self.center_y = cx, cy

    def is_close_to(self, pos_x, pos_y) -> bool:
        """
        is it close to a position ?
        used for removing obstacles with the mouse
        """
        return distance_1((self.center_x, self.center_y), (pos_x, pos_y)) <= 10


class Window(arcade.Window):
    """
    the game
    """
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
# we keep a visible mouse as we can use it to insert obstacles
#        self.set_mouse_visible(False)
        arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.boids = None
        self.obstacles = None
        self.freeze = False
        self.adapt_slowness()

    def setup(self):
        self.boids = SpriteList()
        self.obstacles = SpriteList()
        self.populate_obstacles()
        self.populate_boids()

    def populate_boids(self):
        self.boids.extend([ Boid(self.boids, self.obstacles) for _ in range(NB_BOIDS) ])

    def populate_obstacles(self):
        """
        put obstacles along the window border
        actually works best with OBSTACLE_GAP=0 to avoid building
        corridors where boids get trapped
        """
        for index in range(NB_OBSTACLES):
            angle = index * math.tau/NB_OBSTACLES
            pos_x, pos_y = OBSTACLES_RADIUS * math.cos(angle), OBSTACLES_RADIUS * math.sin(angle)
            self.obstacles.append(Obstacle(WIDTH//2+pos_x, HEIGHT//2+pos_y))

    def remove_obstacles(self):
        """
        remove all obstacles
        """
        self.obstacles = SpriteList()

    def on_draw(self):
        arcade.start_render()
        self.boids.draw()
        self.obstacles.draw()

    def on_update(self, delta_time):
        if self.freeze:
            return
        self.boids.update()


    def display_current_settings(self):
        print(30*'=')
        print(f"{APPLY_SEPARATION=} {APPLY_ALIGNMENT=} {APPLY_COHESION=} {APPLY_NOISE=}")
        print(f"FREEZE={self.freeze} {SLOW=} {DEBUG=}")

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.S:
            global APPLY_SEPARATION
            APPLY_SEPARATION = not APPLY_SEPARATION
            self.display_current_settings()
        elif symbol == arcade.key.A:
            global APPLY_ALIGNMENT
            APPLY_ALIGNMENT = not APPLY_ALIGNMENT
            self.display_current_settings()
        elif symbol == arcade.key.C:
            global APPLY_COHESION
            APPLY_COHESION = not APPLY_COHESION
            self.display_current_settings()
        elif symbol == arcade.key.N:
            global APPLY_NOISE
            APPLY_NOISE = not APPLY_NOISE
            self.display_current_settings()
        elif symbol in (arcade.key.EQUAL, arcade.key.NUM_EQUAL):
            self.display_current_settings()

        elif symbol == arcade.key.SPACE:
            self.freeze = not self.freeze
            self.display_current_settings()
        elif symbol == arcade.key.F:
            global SLOW
            SLOW = not SLOW
            self.adapt_slowness()
            self.display_current_settings()
        elif symbol == arcade.key.D:
            global DEBUG
            DEBUG = not DEBUG
            self.display_current_settings()
        elif symbol == arcade.key.KEY_0:
            self.remove_obstacles()
        elif symbol == arcade.key.KEY_1:
            self.populate_obstacles()
        else:
            return super().on_key_release(symbol, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # SHIFT LEFT click
            if modifiers & arcade.key.MOD_SHIFT:
                # print('shift left click')
                for obstacle in self.obstacles[:]:
                    if obstacle.is_close_to(x, y):
                        self.obstacles.remove(obstacle)
            # LEFT click
            else:
                # print('left click')
                self.obstacles.append(Obstacle(x, y))

        return super().on_mouse_press(x, y, button, modifiers)

    def adapt_slowness(self):
        # useful when troubleshooting so that the print flow slows down
        self.set_update_rate(1/6 if SLOW else 1/30)



def main():
    global NB_BOIDS, BOID_SPEED, CLOSE_RADIUS1
    global ALIGNMENT_RADIUS, SEPARATION_RADIUS, COHESION_RADIUS, NOISE_RADIUS
    global DEBUG
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--nb-boids", type=int, help="set number of boids",
                        default=NB_BOIDS)
    parser.add_argument("-s", "--boid-speed", type=int, help="set boid speed",
                        default=BOID_SPEED)
    parser.add_argument("-c", "--close-radius", type=int, help="set 'close' radius",
                        default=CLOSE_RADIUS1)
    parser.add_argument("--alignment-radius", type=int, default=ALIGNMENT_RADIUS)
    parser.add_argument("--separation-radius", type=int, default=SEPARATION_RADIUS)
    parser.add_argument("--cohesion-radius", type=int, default=COHESION_RADIUS)
    parser.add_argument("--noise-radius", type=float, default=NOISE_RADIUS)
    parser.add_argument("-d", "--debug", action='store_true', default=False, help="set debug on")

    args = parser.parse_args()
    NB_BOIDS = args.nb_boids
    BOID_SPEED = args.boid_speed
    CLOSE_RADIUS1 = args.close_radius
    ALIGNMENT_RADIUS = args.alignment_radius
    SEPARATION_RADIUS = args.separation_radius
    COHESION_RADIUS = args.cohesion_radius
    NOISE_RADIUS = args.noise_radius
    DEBUG = args.debug

    window = Window()
    window.setup()
    arcade.run()

HOWTO ="""
use any of the following keyboard keys
* s to toggle separation
* a to toggle alignment
* c to toggle cohesion
* n to toggle noise
* = to display current settings
* SPACE to suspend/resume
* f to slow down/speed up frame rate
* d to toggle debugging
* 0 remove all obstacles
* 1 reinstate obstacles

this version no longer has support for controlling the (first) boid

use the following mouse events
* right-click to add obstacle
* shift-right-click to remove obstacle
"""[1:-1]

if __name__ == '__main__':
    print(HOWTO)
    main()

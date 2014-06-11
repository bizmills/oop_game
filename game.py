import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"

class Character(GameElement):
    IMAGE = "Horns"
####   End class definitions    ####

def keyboard_handler():
    if KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    elif KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        next_y = PLAYER.y -1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("Turn down for whaaat")
        next_y = PLAYER.y +1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("everybody turn to the left, left")
        next_x = PLAYER.x -1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("Right thurr, right thurr")
        next_x = PLAYER.x +1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)

def initialize():
    """Put game initialization code here"""
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER 

    rock_positions = [
    (2, 1),
    (1, 2),
    (3, 2),
    (2, 3),
    (1, 1),
    (3, 1)
    ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    # rock1 = Rock()
    # GAME_BOARD.register(rock1)
    # GAME_BOARD.set_el(1, 1, rock1)

    # # Initialize and register rock 2
    # rock2 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(2, 2, rock2)

    # rock3 = Rock()
    # GAME_BOARD.register(rock3)
    # GAME_BOARD.set_el(2,2, rock3)

    # print "The first rock is at", (rock1.x, rock1.y)
    # print "The second rock is at", (rock2.x, rock2.y)
    # print "The third rock is at", (rock3.x, rock3.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE
    # print "Rock 3 image", rock3.IMAGE
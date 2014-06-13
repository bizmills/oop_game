import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
from random import random
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Outcome():
    lose = False

class Shiv(GameElement):
    IMAGE = "Shiv"
    SOLID = False

    def __repr__(self):
        return "shiv"

    def interact(self, player):
        player.inventory["shiv"] = player.inventory.get("shiv", 0) + 1
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d items!"%("shiv", len(player.inventory)))
        print player.inventory

class Food(GameElement):
    IMAGE = "Chocolate"
    SOLID = False

    def interact(self, player):
        player.HP += 50
        GAME_BOARD.draw_msg("You just acquired %s! You have %d Health" % ("food", player.HP))

class Grave(GameElement):
    IMAGE = "Tombstone"
    SOLID = False

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        player.Smarts -= 50
        GAME_BOARD.draw_msg("You hit your head on the rock. That ain't smart. You lose %d smarts and you have %s intelligence left." % (50, player.Smarts))

        if player.Smarts <= 0:
            GAME_BOARD.draw_msg("You have lost all your smarts. You have severe brain damage. You are dead.")
            grave = Grave()
            GAME_BOARD.register(grave)
            GAME_BOARD.set_el(player.x, player.y, grave)
            Outcome.lose = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Character(GameElement):
    IMAGE = "Ghost"
    HP = 100
    Strength = int(random() * 100)
    Smarts = int(random() *10)

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

class Christian(GameElement):
    IMAGE = "Christian"
    SOLID = False

    def interact(self, player):
        player.inventory["christian"] = player.inventory.get("christian", 0) + 1
        print player.inventory

        added_smarts = int(random() * 100)
        player.Smarts += added_smarts

        if all (instructors in player.inventory for instructors in ("christian", "nick", "cynthia")):
            GAME_BOARD.draw_msg("You win Hackbright! Congratulations!")

        elif player.Smarts >= 200:
            GAME_BOARD.draw_msg("You win! You have all the Smarts!")
        else:
            GAME_BOARD.draw_msg("You just acquired %d smarts and %s! You have %d intelligence. You need more instructor help! Keep asking questions!" % (added_smarts, "Christian", player.Smarts))

class Cynthia(GameElement):
    IMAGE = "Cynthia"
    SOLID = False
    def interact(self, player):
        player.inventory["cynthia"] = player.inventory.get("cynthia", 0) + 1
        print player.inventory

        added_smarts = int(random() * 100)
        player.Smarts += added_smarts

        if all (instructors in player.inventory for instructors in ("christian", "nick", "cynthia")):
            GAME_BOARD.draw_msg("You win Hackbright! Congratulations!")

        elif player.Smarts >= 200:
            GAME_BOARD.draw_msg("You win! You have all the Smarts!")
        else:
            GAME_BOARD.draw_msg("You just acquired %d smarts and %s! You have %d intelligence. You need more instructor help! Keep asking questions!" % (added_smarts, "Cynthia", player.Smarts))


class Nick(GameElement):
    IMAGE = "Nick"
    SOLID = False
    def interact(self, player):
        player.inventory["nick"] = player.inventory.get("nick", 0) + 1
        print player.inventory

        added_smarts = int(random() * 100)
        player.Smarts += added_smarts

        if all (instructors in player.inventory for instructors in ("christian", "nick", "cynthia")):
            GAME_BOARD.draw_msg("You win Hackbright! Congratulations!")

        elif player.Smarts >= 200:
            GAME_BOARD.draw_msg("You win! You have all the Smarts!")
        else:
            GAME_BOARD.draw_msg("You just acquired %d smarts and %s! You have %d intelligence. You need more instructor help! Keep asking questions!" % (added_smarts, "Nick", player.Smarts))


class Monster(GameElement):
    IMAGE = "Princess"
    SOLID = True
    HP = 100
    Strength = int(random() * 50)

    #position
    monster_x = int(random()*GAME_WIDTH)
    monster_y = int(random()*GAME_WIDTH)

    def interact(self, player):
        if "shiv" in player.inventory:
            damage_to_monster = player.Strength
            damage_to_player = self.Strength
            self.HP -= damage_to_monster
            player.HP -= damage_to_player
            GAME_BOARD.draw_msg("You did %d damage and the monster did %d damage! The monster has %d and you have %d health remaining." % (damage_to_monster, damage_to_player, self.HP, player.HP))

            if player.HP <= 0:
                GAME_BOARD.draw_msg("You died.")
                # GAME_BOARD.del_el(player.x, player.y)
                grave = Grave()
                GAME_BOARD.register(grave)
                GAME_BOARD.set_el(player.x, player.y, grave)
                Outcome.lose = True

            if self.HP <= 0:
                GAME_BOARD.draw_msg("You killed it! Here's some $$$...just kidding")
                GAME_BOARD.del_el(Monster.monster_x, Monster.monster_y)
                grave = Grave()
                GAME_BOARD.register(grave)
                GAME_BOARD.set_el(Monster.monster_x, Monster.monster_y, grave)
        else:
            GAME_BOARD.draw_msg("The monster laughs at your lack of a weapon.")


#This may work eventually to delay an image
            # time.sleep(10)
            # GAME_BOARD.del_el(4,4)
            # rock = Rock()
            # GAME_BOARD.register(rock)
            # GAME_BOARD.set_el(4,4, rock)

####   End class definitions    ####

def keyboard_handler():
    if Outcome.lose == True:
        return

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if 0 > next_x:
            next_x = 0
        elif next_x >= GAME_WIDTH:
            next_x = 9
        elif 0 > next_y: 
            next_y = 0
        elif next_y >= GAME_HEIGHT:
            next_y = 9

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

def initialize():
    """Put game initialization code here"""
    GAME_BOARD.draw_msg("Choose your path: Increase your Smarts or Shank the Princess.")

    shiv = Shiv()
    GAME_BOARD.register(shiv)
    GAME_BOARD.set_el(3,1, shiv)

    food = Food()
    GAME_BOARD.register(food)
    GAME_BOARD.set_el(8,1, food)
    
    christian = Christian()
    GAME_BOARD.register(christian)
    GAME_BOARD.set_el(2,6, christian)

    cynthia = Cynthia()
    GAME_BOARD.register(cynthia)
    GAME_BOARD.set_el(5,3, cynthia)

    nick = Nick()
    GAME_BOARD.register(nick)
    GAME_BOARD.set_el(7,7, nick)
    
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER 

    rock_positions = [
    (1, 1),
    (2, 1),
    (1, 2),
    (3, 2),
    (4, 3),
    (5, 7),
    (1, 2),
    (2, 4),
    (7, 1),
    (7, 5)
    ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # wall_positions = [
    # #left wall
    # (0, 0),
    # (0, 1),
    # (0, 2),
    # (0, 3),
    # (0, 4),
    # (0, 5),
    # (0, 6),
    # (0, 7),
    # (0, 8),
    # (0, 9),
    # #right wall
    # (9, 0),
    # (9, 1),
    # (9, 2),
    # (9, 3),
    # (9, 4),
    # (9, 5),
    # (9, 6),
    # (9, 7),
    # (9, 8),
    # (9, 9),
    # #top wall
    # (1, 0),
    # (2, 0),
    # (3, 0),
    # (4, 0),
    # (5, 0),
    # (6, 0),
    # (7, 0),
    # (8, 0),
    # #bottom wall
    # (1, 9),
    # (2, 9),
    # (3, 9),
    # (4, 9),
    # (5, 9),
    # (6, 9),
    # (7, 9),
    # (8, 9)
    # ]

    # walls = []
    # for pos in wall_positions:
    #     wall = Wall()
    #     GAME_BOARD.register(wall)
    #     GAME_BOARD.set_el(pos[0], pos[1], wall)
    #     walls.append(wall)

    princess = Monster()
    GAME_BOARD.register(princess)

    existing_el = GAME_BOARD.get_el(Monster.monster_x, Monster.monster_y)
    while existing_el != None:
        Monster.monster_x = int(random()*GAME_WIDTH)
        Monster.monster_y = int(random()*GAME_HEIGHT)
        existing_el = GAME_BOARD.get_el(Monster.monster_x, Monster.monster_y)
    if existing_el is None:
        GAME_BOARD.set_el(Monster.monster_x, Monster.monster_y, princess)
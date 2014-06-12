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
    IMAGE = "Star"
    SOLID = False

    def interact(self, player):
        player.HP += 50
        GAME_BOARD.draw_msg("You just acquired %s! You have %d Health" % ("food", player.HP))

class Grave(GameElement):
    IMAGE = "Heart" # To be replaced by grave stone image
    SOLID = False

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        player.Smarts -= 50
        GAME_BOARD.draw_msg("You hit your head on the rock. That ain't smart. You lose %d smarts and you have %s intelligence left." % (50, player.Smarts))

        if player.Smarts <= 0:
            GAME_BOARD.draw_msg("You have lost all your smarts. You have severe brain damage. You are dead.")
            # make player die

class Character(GameElement):
    IMAGE = "Ghost"
    HP = 100
    Strength = int(random() * 100)
    Smarts = int(random() *100)

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

        added_smarts = int(random() * 1000)
        player.Smarts += added_smarts

        if player.Smarts >= 2000:
            GAME_BOARD.draw_msg("You win! You have all the Smarts!")
        else:
            GAME_BOARD.draw_msg("You just acquired %d smarts and %s! You have %d intelligence. You need more instructor help! Keep asking questions!" % (added_smarts, "Christian", player.Smarts))

class Cynthia(GameElement):
    IMAGE = "Cynthia"
    SOLID = False
    def interact(self, player):
        player.inventory["cynthia"] = player.inventory.get("cynthia", 0) + 1
        print player.inventory

        added_smarts = int(random() * 1000)
        player.Smarts += added_smarts

        if player.Smarts >= 2000:
            GAME_BOARD.draw_msg("You win! You have all the Smarts!")
        else:
            GAME_BOARD.draw_msg("You just acquired %d smarts and %s! You have %d intelligence. You need more instructor help! Keep asking questions!" % (added_smarts, "Cynthia", player.Smarts))


class Nick(GameElement):
    IMAGE = "Nick"
    SOLID = False
    def interact(self, player):
        player.inventory["nick"] = player.inventory.get("nick", 0) + 1
        print player.inventory

        added_smarts = int(random() * 1000)
        player.Smarts += added_smarts

        if player.Smarts >= 2000:
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
    monster_y = int(random()*GAME_HEIGHT)

    # existing_el = GAME_BOARD.get_el(monster_x, monster_y)

    # if existing_el:
    #     monster_x = int(random()*GAME_WIDTH)
    #     monster_y = int(random()*GAME_HEIGHT)

    # if existing_el is None:
    #     pass

    def interact(self, player):
        if "shiv" in player.inventory:
            damage_to_monster = player.Strength
            damage_to_player = self.Strength
            self.HP -= damage_to_monster
            player.HP -= damage_to_player
            GAME_BOARD.draw_msg("You did %d damage and the monster did %d damage! The monster has %d and you have %d health remaining." % (damage_to_monster, damage_to_player, self.HP, player.HP))

            if player.HP <= 0:
                GAME_BOARD.draw_msg("You died.")
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

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

def initialize():
    """Put game initialization code here"""
    GAME_BOARD.draw_msg("Linna and Biz made this:)")

    shiv = Shiv()
    GAME_BOARD.register(shiv)
    GAME_BOARD.set_el(3,1, shiv)

    food = Food()
    GAME_BOARD.register(food)
    GAME_BOARD.set_el(6,4, food)

    princess = Monster()
    GAME_BOARD.register(princess)
    GAME_BOARD.set_el(Monster.monster_x, Monster.monster_y, princess)
    
    christian = Christian()
    GAME_BOARD.register(christian)
    GAME_BOARD.set_el(5,5, christian)

    cynthia = Cynthia()
    GAME_BOARD.register(cynthia)
    GAME_BOARD.set_el(7,3, cynthia)

    nick = Nick()
    GAME_BOARD.register(nick)
    GAME_BOARD.set_el(8,2, nick)
    
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER 

    rock_positions = [
    (2, 1),
    (1, 2),
    (3, 2),
    (1, 1)
    ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
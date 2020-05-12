import pygame as pg
from settings import *
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pg.sprite.Sprite.__init__(self)
        self.images = {
            # IDLE
            "idle-up": pg.image.load(path.join(PLAYER_PATH, "link_up1.png")),
            "idle-down": pg.image.load(path.join(PLAYER_PATH, "link_down1.png")),
            "idle-left": pg.image.load(path.join(PLAYER_PATH, "link_left1.png")),
            "idle-right": pg.image.load(path.join(PLAYER_PATH, "link_right1.png")),
            # WALK
            "walk-up": pg.image.load(path.join(PLAYER_PATH, "link_up2.png")),
            "walk-down": pg.image.load(path.join(PLAYER_PATH, "link_down2.png")),
            "walk-left": pg.image.load(path.join(PLAYER_PATH, "link_left2.png")),
            "walk-right": pg.image.load(path.join(PLAYER_PATH, "link_right2.png")),
            # ATTACK
            "attack-up": pg.image.load(path.join(PLAYER_PATH, "attack_up.png")),
            "attack-down": pg.image.load(path.join(PLAYER_PATH, "attack_down.png")),
            "attack-left": pg.image.load(path.join(PLAYER_PATH, "attack_left.png")),
            "attack-right": pg.image.load(path.join(PLAYER_PATH, "attack_right.png")),
        }
        self.image=self.images["idle-up"]
        self.animations={
            "walk-up": [self.images["idle-up"], self.images["walk-up"]],
            "walk-down": [self.images["idle-down"], self.images["walk-down"]],
            "walk-left": [self.images["idle-left"], self.images["walk-left"]],
            "walk-right": [self.images["idle-right"], self.images["walk-right"]],
        }
        self.ticker=0
        self.current_frame=0
        self.rect=self.images["idle-up"].get_rect()
        self.rect.x=start_x
        self.rect.y=start_y
        self.can_move=True
        self.direction='up'
        self.action="attacking"
        self.enter_door=False
        # items
        self.keys=None
        self.has_sword=False
        self.sounds={
            "sword": pg.mixer.Sound(AUDIO_SWORD)
        }
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed=False, False, False, False
        self.up, self.down, self.left, self.right="up down left right".split(
            " ")

    def update(self):
        if self.up_pressed:
            self.rect.y -= 5
            self.image=self.animations["walk-up"][self.current_frame]

        if self.down_pressed:
            self.rect.y += 5
            self.image=self.animations["walk-down"][self.current_frame]

        if self.left_pressed:
            self.rect.x -= 5
            self.image=self.animations["walk-left"][self.current_frame]

        if self.right_pressed:
            self.rect.x += 5
            self.image=self.animations["walk-right"][self.current_frame]

        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame=(self.current_frame + 1) % 2

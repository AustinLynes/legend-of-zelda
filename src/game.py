import pygame as pg
from settings import *
from player import Player
import sys
from os import path
vec2 = pg.math.Vector2

"""
    - SCREENS
        [ TITLE => GAME ]
"""


def align_right(str):
    return (85 - len(str) * " ") + str


class Game:
    running = True

    def __init__(self, width=800, height=600):
        #  initalize pygame
        pg.init()
        # screen setup
        self.dimensions = vec2()
        self.dimensions[:] = width, height
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((width, height))
        # create internal clock
        self.clock = pg.time.Clock()

        self.player = Player(50, 50)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        # sets the current screen to the title-screen
        self.current_screen = "title"

    def main_loop(self):
        pg.mixer.music.load(MAIN_THEME)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.2)

        while self.running:
            if(self.current_screen == "game"):
                self.handle_events()
                self.draw()
                self.all_sprites.update()
            elif(self.current_screen == "title"):
                self.handle_title_events()
                self.draw_title()

            self.clock.tick(60)
            pg.display.set_caption(
                f"{TITLE}  --  FPS:  {self.clock.get_fps():.1f}")
        pg.quit()

    def draw(self):
        # add check for dungeon here
        self.screen.fill(CLEAR_COLOR)
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def draw_title(self):
        self.screen.fill((40, 40, 40))
        logo = pg.image.load(path.join(UI_PATH, "title.png"))
        credit = pg.image.load(path.join(UI_PATH, "credits.png"))
        self.screen.blit(logo, (220, 200))
        self.screen.blit(credit, (300, 443))
        pg.display.flip()

    def handle_events(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN and self.player.can_move == True:
                # UP
                if e.key == pg.K_w:
                    self.player.up_pressed = True
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.up
                # DOWN
                if e.key == pg.K_s:
                    self.player.down_pressed = True
                    self.player.up_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.down
                # LEFT
                if e.key == pg.K_a:
                    self.player.left_pressed = True
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.left
                # RIGHT
                if e.key == pg.K_d:
                    self.player.right_pressed = True
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.direction = self.player.right
                if e.key == pg.K_SPACE and self.player.has_sword:
                    self.player.attack_pressed = True
                    self.player.can_move = False
                    self.player.sounds["sword"].play()
                    if self.player.direction == self.player.up:
                        # play attack anim.
                        self.player.image = self.player.images["attack-up"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.y -= 30
                    if self.player.direction == self.player.down:
                        # play attack anim.
                        self.player.image = self.player.images["attack-down"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x
                        self.player.rect.y = oldrect.y + 15

                    if self.player.direction == self.player.left:
                        # play attack anim.
                        self.player.image = self.player.images["attack-left"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x - 30
                        self.player.rect.y = oldrect.y

                    if self.player.direction == self.player.right:
                        # play attack anim.
                        self.player.image = self.player.images["attack-right"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x + 15
                        self.player.rect.y = oldrect.y
                    
                    self.player.action = "attacking"

            if e.type == pg.KEYUP:
                if e.key == pg.K_w:
                    self.player.up_pressed = False
                if e.key == pg.K_s:
                    self.player.down_pressed = False
                if e.key == pg.K_a:
                    self.player.left_pressed = False
                if e.key == pg.K_d:
                    self.player.right_pressed = False
                if e.key == pg.K_SPACE and self.player.has_sword:
                    self.player.can_move = True
                    self.player.attack_pressed = False
                    if self.player.direction == self.player.up:
                        # play attack anim.
                        self.player.image = self.player.images["idle-up"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.y += 30
                    if self.player.direction == self.player.down:
                        # play attack anim.
                        self.player.image = self.player.images["idle-down"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x
                        self.player.rect.y = oldrect.y - 15

                    if self.player.direction == self.player.left:
                        # play attack anim.
                        self.player.image = self.player.images["idle-left"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.x += 30

                    if self.player.direction == self.player.right:
                        # play attack anim.
                        self.player.image = self.player.images["idle-right"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x - 15
                        self.player.rect.y = oldrect.y

    def handle_title_events(self):
        events = pg.event.get()
        for e in events:
            # if the main event is quit.. then force quit the game
            if e.type == pg.QUIT:
                self.running = False
            # check for key evenets on this page
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.current_screen = "game"


"""
   220       220
 | --  [360] -- |
    800 - 360 = 440
    440 / 2 = 220
"""
